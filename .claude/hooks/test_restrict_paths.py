# =============================================================================
# test_restrict_paths.py — Feeds sample tool calls to restrict_paths.py and
# checks each is allowed or denied as expected. Run: python .claude/hooks/test_restrict_paths.py
# =============================================================================

import json
import subprocess
import sys
from pathlib import Path

HOOK = Path(__file__).with_name('restrict_paths.py')
ROOT = str(Path(__file__).resolve().parents[2])

CASES = [
    # (label, tool_name, tool_input, expected)
    ('Read file inside (absolute)',     'Read',       {'file_path': ROOT + r'\utils.py'},                    'allow'),
    ('Edit file inside (relative)',     'Edit',       {'file_path': 'pages/1_Stories.py'},                  'allow'),
    ('Grep with no path',               'Grep',       {'pattern': 'x'},                                     'allow'),
    ('Glob relative pattern',           'Glob',       {'pattern': '**/*.py'},                               'allow'),
    ('Agent call (no paths)',           'Agent',      {'prompt': 'hi'},                                     'allow'),
    ('Bash compile in project',         'Bash',       {'command': 'python -m py_compile utils.py 2>/dev/null'}, 'allow'),
    ('PS quoted inside path w/ spaces', 'PowerShell', {'command': f'python -m streamlit run "{ROOT}\\Home.py"'}, 'allow'),
    ('PS request to localhost URL',     'PowerShell', {'command': 'Invoke-WebRequest http://localhost:8501/_stcore/health'}, 'allow'),
    ('Read C:\\Windows\\win.ini',        'Read',       {'file_path': r'C:\Windows\win.ini'},                  'deny'),
    ('Write ..\\escape.txt',            'Write',      {'file_path': r'..\escape.txt'},                       'deny'),
    ('Write to sibling folder prefix',  'Write',      {'file_path': ROOT + r'2\x.py'},                       'deny'),
    ('Glob absolute outside',           'Glob',       {'pattern': 'C:/Users/**/*.py'},                      'deny'),
    ('Grep path outside',               'Grep',       {'pattern': 'x', 'path': 'C:/Users/someone'},         'deny'),
    ('Artifact file outside',           'Artifact',   {'file_path': r'C:\Users\someone\AppData\Local\Temp\a.html'}, 'deny'),
    ('Bash cat /c/Users/... file',      'Bash',       {'command': 'cat /c/Users/someone/.bashrc'},          'deny'),
    ('Bash cat /tmp/x',                 'Bash',       {'command': 'cat /tmp/x'},                            'deny'),
    ('Bash cd .. && ls',                'Bash',       {'command': 'cd .. && ls'},                           'deny'),
    ('Bash cat ~/.ssh/id_rsa',          'Bash',       {'command': 'cat ~/.ssh/id_rsa'},                     'deny'),
    ('PS Set-Location $env:TEMP',       'PowerShell', {'command': 'Set-Location $env:TEMP; ls'},            'deny'),
    ('PS quoted outside path',          'PowerShell', {'command': 'Get-Content "C:\\Program Files\\x.txt"'}, 'deny'),
]


def run(tool, tool_input, cwd=ROOT, raw=None):
    payload = raw if raw is not None else json.dumps({'tool_name': tool, 'cwd': cwd, 'tool_input': tool_input})
    out = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True)
    if out.returncode != 0:
        return f'error(exit {out.returncode})'
    return 'deny' if '"deny"' in out.stdout else 'allow'


failures = 0
for label, tool, tool_input, expected in CASES:
    got = run(tool, tool_input)
    ok = got == expected
    failures += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {label:36} expected={expected:5} got={got}")

got = run(None, None, raw='not json')
ok = got == 'deny'
failures += not ok
print(f"{'PASS' if ok else 'FAIL'}  {'Malformed input fails closed':36} expected=deny  got={got}")

print(f'\n{failures} failure(s)')
sys.exit(1 if failures else 0)
