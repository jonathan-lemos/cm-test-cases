# C- Test Cases
A list of test cases for Eggen's C- project. Includes an automatic test running script and a tool that builds an Eggen-style shar for you.

## Dependencies
The Osprey has all of the required dependencies.
The below only apply if you're trying to do this on your own machine.

To use the included testing tool `test.py`, you will need:
* Linux, OSX, or Windows Subsystem for Linux.
* Python >=3.3

To use the included shar builder `mkshar`, you will need:
* Linux, OSX, or Windows Subsystem for Linux
* bash
* shar
* turnin
* coreutils (grep, script, sed)

## Getting the project
Most of the time, the project is already on the Osprey, which you can access using:
```shell
$ /tmp/just_do_it # only needed the first time you use mkshar
$ mkshar
```

Since the `/tmp` folder on Osprey gets wiped periodically, you might want to keep a local copy.

The easiest way to download the project is using git:
```shell
$ git clone https://github.com/jonathan-lemos/cm-test-cases.git
```
I recommend you run the above command on the Osprey, as the Osprey has all of the required dependencies.

## `mkshar` (shar builder)
This script automatically builds a shar the way Eggen wants it if you're too lazy to do so.

You must give it:
* All files required to run your project.
* A single test file to demonstrate your project's usage.

Do not give it:
* Intermediate build files (such as .class files)

The script will generate the following *if they do not exist*:
* Makefile (if your project is in C, Java, or Python)
* p-script (if your project is in C, Java, or Python)
* documentation file (you will be required to fill in some details)

The script will always generate the following:
* typescript
* the output shar (called `out_fn`)

### Usage
todo
