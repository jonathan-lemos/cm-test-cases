#!/usr/bin/python

import os
import sys
import re
import subprocess
import concurrent.futures


def test(executable, filename, expected_output, timeout_seconds=5):
    with subprocess.Popen(" ".join([executable, filename]), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True) as proc:
        try:
            s = (proc.communicate(timeout=timeout_seconds)[0]).decode()
        except subprocess.CalledProcessError as e:
            s = e.output
        except subprocess.TimeoutExpired as e:
            proc.kill()
            if e.output is not None:
                s = e.output.decode()
            else:
                s = ""
            s += f"\n\nTimed out after {timeout_seconds} seconds"
        proc.kill()

    if type(s) == bytes:
        s = s.decode().strip()
    else:
        s = str(s).strip()

    if s != expected_output:
        return False, filename, s
    else:
        return True, filename


# the directory of test.py
base = os.path.dirname(os.path.abspath( __file__ ))
# the directories within test.py, excluding those that start with '.' or '__'
dirs = list(sorted(x for x in os.listdir(base) if os.path.isdir(os.path.join(base, x)) and not (x.startswith('.') or x.startswith('__'))))


def print_help():
    print(f"{sys.argv[0]} v 1.4")
    print(f"Runs test cases on your shit code")
    print()
    print(f"USAGE:")
    print(f"\t{sys.argv[0]} [options] [path of p-script] {dirs}")
    print(f"\tThe script should be able to be executed on the command-line as './p-script filename.txt'")
    print()
    print(f"FLAGS:")
    print("\t-h, --help             Prints this screen")
    print("\t-s, --single-threaded  Run only one case at a time. Use this if your code writes to files.")


if len(sys.argv) == 1:
    print_help()
    sys.exit(0)


max_threads = max(5, os.cpu_count() * 3)
p_script = None
test_cases = None

# process command-line arguments
for arg in sys.argv[1:]:
    if arg.startswith("-"):
        if arg[1:] == "h" or arg[2:] == "help":
            print_help()
            exit(0)
        elif arg[1:] == "s" or arg[2:] == "single-threaded":
            max_threads = 1
        else:
            print_help()
            print()
            print(f"Unrecognized argument '{arg}'")
            sys.exit(1)
    else:
        if p_script is None:
            p_script = arg
        elif test_cases is None:
            test_cases = arg
        else:
            print_help()
            print()
            print(f"Got an extra argument '{arg}'.")
            sys.exit(1)


if p_script is None:
    print_help()
    print()
    print("Expected a p-script, didn't get one.")
    sys.exit(1)

if test_cases is None:
    print_help()
    print()
    print(f"Expected a test suite within {dirs}, didn't get one.")
    sys.exit(1)

if not os.path.exists(p_script):
    print(f"The given p-script at '{p_script}' does not exist.")
    sys.exit(1)

if not os.path.isfile(p_script):
    print(f"The given p-script at '{p_script}' is a directory.")
    sys.exit(1)

if not os.access(p_script, os.X_OK):
    print(f"The given p-script at '{p_script}' is not executable. Run 'chmod a+x {p_script}' and try again.")
    sys.exit(1)

if not os.path.isdir(base):
    print(f"base dir {base} does not exist. fatal fuckin error")
    sys.exit(1)

basedir = f"{base}/{test_cases}"
if not os.path.isdir(basedir):
    print(f"Invalid set of cases '{test_cases}'. Must be one of {dirs}.")
    sys.exit(1)

if not os.path.isdir(f"{basedir}/accept"):
    print(f"The given set of cases is missing '{basedir}/accept'.")
    sys.exit(1)

if not os.path.isdir(f"{basedir}/reject"):
    print(f"The given set of cases is missing '{basedir}/reject'.")
    sys.exit(1)


threads = []
threads = []
failed_accept = []
failed_reject = []
len_total = 0
abspath = os.path.abspath(sys.argv[1])


with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    accept_jobs = []
    reject_jobs = []

    for test_case in os.listdir(f"{basedir}/accept"):
        len_total += 1
        accept_jobs.append(executor.submit(
            test,
            abspath,
            f"{basedir}/accept/{test_case}",
            "ACCEPT",
            2,
        ))

    for test_case in os.listdir(f"{basedir}/reject"):
        len_total += 1
        reject_jobs.append(executor.submit(
            test,
            abspath,
            f"{basedir}/reject/{test_case}",
            "REJECT",
            2,
        ))

    for aj in concurrent.futures.as_completed(accept_jobs):
        res = aj.result()
        if not res[0]:
            failed_accept.append((res[1], res[2]))

    for rj in concurrent.futures.as_completed(reject_jobs):
        res = rj.result()
        if not res[0]:
            failed_reject.append((res[1], res[2]))


for fname, output in failed_accept:
    print(f"Failed case '{fname}'")
    print(">>>\033[32m")
    print(open(fname, "r").read())
    print("\033[m>>>")
    print("Expected: \033[32mACCEPT\033[m")
    print("Actual")
    print(">>>\033[32m")
    print(output)
    print("\033[m>>>")
    print()

for fname, output in failed_reject:
    print(f"Failed case '{fname}'")
    print(">>>\033[32m")
    print(open(fname, "r").read())
    print("\033[m>>>")
    print("Expected: \033[32mREJECT\033[m")
    print("Actual")
    print(">>>\033[32m")
    print(output)
    print("\033[m>>>")
    print()

print(f"Failed \033[32m{str(len(failed_accept) + len(failed_reject))}\033[m out of \033[32m{str(len_total)}\033[m cases")

