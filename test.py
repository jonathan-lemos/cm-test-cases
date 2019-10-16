#!/usr/bin/python

import os
import sys
import re
import subprocess

base = os.path.dirname(os.path.abspath( __file__ ))

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} [path of program] {list(sorted(x for x in os.listdir(base) if os.path.isdir(os.path.join(base, x)) and not x.startswith('.')))}")
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
    print(f"no type of program '{sys.argv[2]}'. must be one of {str([x for x in os.listdir(base) if os.path.isdir(x) and not x.startswith('.') and not x.startswith('__')])}")
    sys.exit(1)

if not os.path.isdir(f"{basedir}/accept"):
    print(f"accept dir {basedir}/accept does not exist")
    sys.exit(1)

if not os.path.isdir(f"{basedir}/reject"):
    print(f"reject dir {basedir}/reject does not exist")
    sys.exit(1)

failed_accept = []
failed_reject = []
len_total = 0
abspath = os.path.abspath(sys.argv[1])
for test_case in os.listdir(f"{basedir}/accept"):
    len_total += 1
    try:
        s = subprocess.check_output([abspath, f"{basedir}/accept/{test_case}"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        s = e.output
    if type(s) == bytes:
        s = s.decode().strip()
    else:
        s = str(s).strip()
    if s != "ACCEPT":
        failed_accept.append((test_case, s))

for test_case in os.listdir(f"{basedir}/reject"):
    len_total += 1
    try:
        s = subprocess.check_output([abspath, f"{basedir}/reject/{test_case}"], stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError as e:
        s = e.output
    if type(s) == bytes:
        s = s.decode().strip()
    else:
        s = str(s).strip()
    if s != "REJECT":
        failed_reject.append((test_case, s))

for fname, output in failed_accept:
    print(f"Failed case '{fname}'")
    print(">>>\033[32m")
    print(open(f"{basedir}/accept/{fname}", "r").read())
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
    print(open(f"{basedir}/reject/{fname}", "r").read())
    print("\033[m>>>")
    print("Expected: REJECT")
    print("Actual")
    print(">>>\033[32m")
    print(output)
    print("\033[m>>>")
    print()

print(f"Failed \033[32m{str(len(failed_accept) + len(failed_reject))}\033[m out of \033[32m{str(len_total)}\033[m cases")

