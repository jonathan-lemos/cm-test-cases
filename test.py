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


base = os.path.dirname(os.path.abspath( __file__ ))
dirs = list(sorted(x for x in os.listdir(base) if os.path.isdir(os.path.join(base, x)) and not x.startswith('.')))

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} [path of p-script] {dirs}")
    print()
    print("The script should be able to be executed as './p-script filename.txt'")
    sys.exit(0)

if not os.path.exists(sys.argv[1]):
    print(f"{sys.argv[1]} does not exist")
    sys.exit(1)

if not os.path.isfile(sys.argv[1]):
    print(f"{sys.argv[1]} is a directory")
    sys.exit(1)

if not os.access(sys.argv[1], os.X_OK):
    print(f"{sys.argv[1]} cannot be executed")
    sys.exit(1)

if not os.path.isdir(base):
    print(f"base dir {base} does not exist. fatal fuckin error")
    sys.exit(1)

basedir = f"{base}/{sys.argv[2]}"
if not os.path.isdir(basedir):
    print(f"no type of program '{sys.argv[2]}'. must be one of {dirs}")
    sys.exit(1)

if not os.path.isdir(f"{basedir}/accept"):
    print(f"accept dir {basedir}/accept does not exist")
    sys.exit(1)

if not os.path.isdir(f"{basedir}/reject"):
    print(f"reject dir {basedir}/reject does not exist")
    sys.exit(1)

threads = []
threads = []
failed_accept = []
failed_reject = []
len_total = 0
abspath = os.path.abspath(sys.argv[1])


with concurrent.futures.ThreadPoolExecutor() as executor:
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
    print("Expected: ACCEPT")
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
    print("Expected: REJECT")
    print("Actual")
    print(">>>\033[32m")
    print(output)
    print("\033[m>>>")
    print()

print(f"Failed \033[32m{str(len(failed_accept) + len(failed_reject))}\033[m out of \033[32m{str(len_total)}\033[m cases")

