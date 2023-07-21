import sys
import re

ERROR_R = re.compile(r'((.*): ((?:error|warning|line)):(.*\n))')
GTEST_R = re.compile(
    r'\[ RUN      \](.*)\n(.*): Failure([\s\S]*?)(?=\n.*?=|\[ RUN      \])')
ANSI_SCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


class CLIFormat:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BACKSPACE = '\x08'

    @staticmethod
    def colored(str: str, color: str) -> str:
        return color + str + CLIFormat.ENDC


output = ""
for line in sys.stdin:
    print(line.replace("\n", "").replace("\t", "    "))
    output += ANSI_SCAPE.sub('', line)


def pprint(loc, errors):
    print(CLIFormat.colored(loc, CLIFormat.OKGREEN + CLIFormat.BOLD))
    for err in errors:
        color = CLIFormat.FAIL if "error" in err["type"] else CLIFormat.WARNING
        print(f"\t{CLIFormat.colored('->', color)} {err['msg']}")


def build_errors(output: str):
    errors = dict()
    events = re.findall(ERROR_R, output)
    events.reverse()
    for err in set(events):
        k = ":".join(err[1].split(":")[:-1]).split("/")[-1]
        if k not in errors.keys():
            errors[k] = []

        errors[k].append(dict(type=err[2], msg=err[3][1:].replace("\n", "")))
    return errors


def build_gtest(output: str):
    errors = dict()
    events = re.findall(GTEST_R, output)
    events.reverse()
    for err in set(events):
        k = err[0].split(".")[-1]
        if k not in errors.keys():
            errors[k] = [dict(type=err[1], msg=err[2][1:])]
    return errors


errors = build_errors(output)
gtest = build_gtest(output)

for k, v in errors.items():
    pprint(k, v)

for k, v in gtest.items():
    pprint(k, v)
