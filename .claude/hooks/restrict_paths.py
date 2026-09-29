# =============================================================================
# restrict_paths.py — PreToolUse hook: deny any tool call that reads or writes
# outside the project folder.
#
# File tools (Read, Write, Edit, Glob, Grep, NotebookEdit, Artifact, ...) are
# checked exactly via their path arguments. Shell commands (Bash, PowerShell)
# are checked heuristically: absolute paths, `..` escapes, and home/temp
# shortcuts in the command text are resolved and must stay inside the project.
# =============================================================================

import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(os.environ.get('CLAUDE_PROJECT_DIR') or Path(__file__).resolve().parents[2]).resolve()

PATH_KEYS = ('file_path', 'notebook_path', 'path', 'out_dir', 'root')
LIST_PATH_KEYS = ('file_paths', 'paths')
SHELL_TOOLS = ('Bash', 'PowerShell')

# Device paths that are harmless to reference from shell commands.
ALLOWED_SHELL_PATHS = {'/dev/null', '/dev/stdout', '/dev/stderr', 'nul', '$null'}

# Shortcuts that always point outside the project.
OUTSIDE_SHORTCUTS = re.compile(
    r'(?i)(\$env:(temp|tmp|userprofile|appdata|localappdata|homepath|programdata|windir|systemroot)\b'
    r'|%(temp|tmp|userprofile|appdata|localappdata|homepath|programdata|windir|systemroot)%'
    r'|\$\{?(home|tmpdir|temp|tmp)\b'
    r'|(^|[\s"\'=(])~(?=[\\/\s"\']|$))'
)

QUOTED = re.compile(r'"([^"]*)"|\'([^\']*)\'')
WIN_ABS = re.compile(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s"\'|;&<>()]*')
POSIX_ABS = re.compile(r'(?:(?<=^)|(?<=[\s=>(]))/[^\s"\'|;&<>()]*')
DOTDOT = re.compile(r'(?:(?<=^)|(?<=[\s=>("\']))[^\s"\'|;&<>()]*\.\.(?:[\\/][^\s"\'|;&<>()]*)?')


def to_path(raw, cwd):
    raw = raw.strip()
    m = re.match(r'^/([A-Za-z])(/.*)?$', raw)  # Git Bash style /c/Users/...
    if m:
        raw = f'{m.group(1)}:{m.group(2) or "/"}'
    p = Path(raw)
    if not p.is_absolute():
        p = Path(cwd) / p
    return p.resolve()


def is_inside(p):
    try:
        root = os.path.normcase(str(PROJECT_ROOT))
        return os.path.commonpath([root, os.path.normcase(str(p))]) == root
    except ValueError:  # different drives
        return False


def shell_candidates(command):
    found = []
    for m in QUOTED.finditer(command):
        s = m.group(1) if m.group(1) is not None else m.group(2)
        if re.match(r'[A-Za-z]:[\\/]', s) or s.startswith('/') or '..' in s:
            found.append(s)
    unquoted = QUOTED.sub(' ', command)
    for rx in (WIN_ABS, POSIX_ABS, DOTDOT):
        found.extend(m.group(0) for m in rx.finditer(unquoted))
    return found


def deny(reason):
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': reason,
        }
    }))
    sys.exit(0)


def main():
    data = json.load(sys.stdin)
    tool = data.get('tool_name', '')
    tool_input = data.get('tool_input') or {}
    cwd = data.get('cwd') or str(PROJECT_ROOT)

    if not is_inside(Path(cwd).resolve()) and tool in SHELL_TOOLS:
        deny(f'Blocked: the shell working directory ({cwd}) is outside the project folder {PROJECT_ROOT}.')

    raw_paths = [tool_input[k] for k in PATH_KEYS if isinstance(tool_input.get(k), str)]
    for k in LIST_PATH_KEYS:
        if isinstance(tool_input.get(k), list):
            raw_paths.extend(p for p in tool_input[k] if isinstance(p, str))
    if tool == 'Glob' and isinstance(tool_input.get('pattern'), str):
        raw_paths.append(tool_input['pattern'].split('*')[0] or '.')

    for raw in raw_paths:
        if raw and not is_inside(to_path(raw, cwd)):
            deny(f'Blocked: {tool} targets {raw}, which is outside the project folder {PROJECT_ROOT}.')

    if tool in SHELL_TOOLS:
        command = tool_input.get('command') or ''
        if OUTSIDE_SHORTCUTS.search(command):
            deny(f'Blocked: the command references a home or temp location outside the project folder {PROJECT_ROOT}.')
        for raw in shell_candidates(command):
            if raw.lower() in ALLOWED_SHELL_PATHS or raw.lower().startswith('/dev/'):
                continue
            if not is_inside(to_path(raw, cwd)):
                deny(f'Blocked: the command references {raw}, which is outside the project folder {PROJECT_ROOT}.')

    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:  # fail closed: a crash must not let the call through
        deny(f'Blocked: restrict_paths hook could not check this call ({type(e).__name__}: {e}).')
