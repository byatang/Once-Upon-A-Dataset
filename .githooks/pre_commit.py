# =============================================================================
# pre_commit.py — Git pre-commit check: blocks commits that stage large files,
# data/credential file types, or content that looks like a secret.
#
# Enabled per clone with:  git config core.hooksPath .githooks
# Bypass (not recommended): git commit --no-verify
# =============================================================================

import re
import subprocess
import sys

MAX_MB = 10  # GitHub warns above 50 MB and rejects above 100 MB

BLOCKED_NAMES = [
    (re.compile(r'\.parquet$', re.I),                            'data file (HMDA data must stay out of the repo)'),
    (re.compile(r'(^|/)\.env(\..+)?$', re.I),                    'environment file'),
    (re.compile(r'\.(pem|key|p12|pfx|keystore|jks)$', re.I),     'key/certificate file'),
    (re.compile(r'(^|/)id_(rsa|dsa|ecdsa|ed25519)(\.pub)?$', re.I), 'SSH key'),
    (re.compile(r'(^|/)(credentials|secrets?)(\.[a-z]+)?$', re.I), 'credentials file'),
    (re.compile(r'(^|/)\.streamlit/secrets\.toml$', re.I),       'Streamlit secrets file'),
]

SECRET_PATTERNS = [
    (re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),           'private key'),
    (re.compile(r'\bAKIA[0-9A-Z]{16}\b'),                         'AWS access key ID'),
    (re.compile(r'\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}'),       'API secret key (sk-...)'),
    (re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36,}\b'),               'GitHub token'),
    (re.compile(r'\bxox[abprs]-[A-Za-z0-9-]{10,}'),               'Slack token'),
    (re.compile(r'\bAIza[0-9A-Za-z_-]{35}\b'),                    'Google API key'),
    (re.compile(r'(?i)\b(api[_-]?key|secret|token|passw(or)?d)\b\s*[:=]\s*[\'"][^\'"\s]{8,}[\'"]'),
                                                                  'hard-coded credential'),
]


def git(*args):
    return subprocess.run(['git', *args], capture_output=True, check=True).stdout


def main():
    staged = git('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').decode('utf-8').split('\0')
    problems = []
    for path in filter(None, staged):
        for rx, why in BLOCKED_NAMES:
            if rx.search(path):
                problems.append(f'{path}: {why}')
                break
        size = int(git('cat-file', '-s', f':{path}'))
        if size > MAX_MB * 1024 * 1024:
            problems.append(f'{path}: {size / 1024 / 1024:.1f} MB exceeds the {MAX_MB} MB limit')
            continue
        text = git('show', f':{path}').decode('utf-8', errors='ignore')
        for rx, why in SECRET_PATTERNS:
            m = rx.search(text)
            if m:
                line = text.count('\n', 0, m.start()) + 1
                problems.append(f'{path}:{line}: looks like a {why}')

    if problems:
        print('pre-commit: commit blocked.\n', file=sys.stderr)
        for p in problems:
            print(f'  - {p}', file=sys.stderr)
        print('\nUnstage with `git restore --staged <file>`, or remove the secret and re-stage.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
