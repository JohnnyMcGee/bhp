import argparse
import getpass
from typing import Any

def _get_parser(prog: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    prog=prog,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    class SplitTarget(argparse.Action):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __call__(self, parser, namespace, value: str, option_string=None):
            try:
                user, host = value.split('@')
                delattr(namespace,"target")
                setattr(namespace, "user", user)
                setattr(namespace, "host", host)
            except Exception as e:
                print("Error parsing argument: 'target'")
                print(e)
    
    parser.add_argument('target', action=SplitTarget, metavar="user@hostname", help="For example root@127.0.0.1")
    parser.add_argument('command', nargs='?', default="id", help="Command to execute on remote host")
    parser.add_argument('-p', '--port', default=22, dest="port", help="Port to connect to on remote host")
    return parser

def ssh_parse(args: "list[str] | None" = ..., program_name: str = "ssh.py") -> "argparse.Namespace | None":
    '''Parse ssh command line options and prompt user for password as needed'''
    parser = _get_parser(prog=program_name)
    try:
        ns = parser.parse_args(args=args)
        password = getpass.getpass(prompt=f"enter password for {ns.user}: ")
        setattr(ns, "password", password)
        return ns

    except Exception as e:
        print(e)