import sys
import re
import subprocess
from pathlib import Path
import argparse

write_output = print
CURRENT = Path(__file__).resolve().parent
log = CURRENT.parent.joinpath("log.txt")


def get_branches():
    output = subprocess.getoutput("git br -vv")
    ret = []

    for line in output.split("\n"):
        line = line[1:].strip()  # remove '*' before branch name
        name = line.split(" ")[0]
        ret.append(name)

    return ret


def get_git_files(command):
    r = subprocess.getoutput(f"git ls-files {command}")
    r = r.strip().split("\n")
    r = filter(lambda x: x.strip() != "", r)
    return list(r)


def get_checkout_commands():
    result = ["checkout"]
    r2 = re.findall(r"alias\.(.*)=checkout", subprocess.getoutput("git config list"))
    result.extend(r2)
    return result


def is_checkout_command(c):
    c = c[4:].lstrip()
    for i in get_checkout_commands():
        if c.startswith(i):
            return True


def get_branch_commands():
    result = ["branch"]
    r2 = re.findall(r"alias\.(.*)=branch", subprocess.getoutput("git config list"))
    result.extend(r2)
    return result


def is_branch_command(c):
    c = c[4:].lstrip()
    for i in get_branch_commands():
        if c.startswith(i):
            return True
    return False


def get_git_commands():
    r = subprocess.getoutput("git --help")
    return re.findall(r"   ([a-z]+)", r)


def main():
    log.write_text(str(sys.argv), encoding="utf8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--complete", "-C", type=str, help="commands to complete")
    args = parser.parse_args()

    command: str = args.complete

    supported_commands = []
    for i in get_git_commands():
        supported_commands.append([i])
    for i in get_checkout_commands():
        branches = get_branches()
        for branch in branches:
            supported_commands.append([i, branch])

    files = get_git_files("--exclude-standard --others")
    files.extend(get_git_files("--modified"))
    for f in files:
        supported_commands.append(["add", f])

    normalized_command = re.sub(r" +", "|", command).split("|")
    nc = normalized_command[1:]  # remove 'git' prefix
    nc_len_1 = len(nc) - 1
    supported_commands = list(
        filter(
            lambda x: len(x) >= len(nc)
            and x[:nc_len_1] == nc[:-1]
            and x[nc_len_1].startswith(nc[nc_len_1]),
            supported_commands,
        )
    )
    supported_commands.sort(key=lambda x: len(x))
    for s in supported_commands:
        write_output(" ".join(s[nc_len_1:]))


if __name__ == "__main__":
    main()
