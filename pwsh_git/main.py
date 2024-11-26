import sys
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


def main():
    log.write_text(str(sys.argv), encoding="utf8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--complete", "-C", type=str, help="commands to complete")
    args = parser.parse_args()
    if args.complete.startswith("git co"):
        branches = get_branches()
        filter = args.complete[len("git co") :].strip()
        if len(filter) > 0:
            for branch in branches:
                if branch.startswith(filter):
                    write_output(branch)
        else:
            for branch in branches:
                write_output(branch)
    elif args.complete.startswith("git add"):
        files = (
            subprocess.getoutput("git ls-files --exclude-standard --others")
            .strip()
            .split("\n")
        )
        files.extend(
            subprocess.getoutput("git ls-files --modified").strip().split("\n")
        )
        filter = args.complete[len("git add") :].strip()
        for line in files:
            if line.strip() == "":
                continue
            if len(filter) > 0:
                if not line.startswith(filter):
                    continue
            print(line)
    else:
        sys.stderr.write("command not begins with 'git co'\n")


if __name__ == "__main__":
    main()
