#!/usr/bin/env python
"""Git 操作脚本：add / status / commit / push
用法：
  python .claude/scripts/git_ops.py add                # git add .
  python .claude/scripts/git_ops.py status             # git status --short
  python .claude/scripts/git_ops.py commit "消息"      # git commit -m "消息"
  python .claude/scripts/git_ops.py push               # git push
  python .claude/scripts/git_ops.py all "消息"         # add + commit + push
"""

import subprocess, sys, os

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            print(f'STDERR: {r.stderr[:500]}')
        return r.stdout.strip()
    except Exception as e:
        return f'ERROR: {e}'

def main():
    if len(sys.argv) < 2:
        print('用法: python git_ops.py add|status|commit|push|all')
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'add':
        out = run(['git', 'add', '.'])
        status = run(['git', 'status', '--short'])
        print(status if status else '(无变更)')

    elif cmd == 'status':
        status = run(['git', 'status', '--short'])
        print(status if status else '(工作区干净)')

    elif cmd == 'commit':
        msg = sys.argv[2] if len(sys.argv) > 2 else 'update'
        out = run(['git', 'commit', '-m', msg])
        print(out)

    elif cmd == 'push':
        out = run(['git', 'push'])
        print(out)

    elif cmd == 'all':
        msg = sys.argv[2] if len(sys.argv) > 2 else 'update'
        run(['git', 'add', '.'])
        r = run(['git', 'commit', '-m', msg])
        if 'nothing to commit' in r.lower() or 'no changes' in r.lower():
            print('无变更')
        else:
            print(r)
        p = run(['git', 'push'])
        print(p)

    else:
        print(f'未知命令: {cmd}')

if __name__ == '__main__':
    main()
