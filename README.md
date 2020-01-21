# C- Test Cases
A list of test cases for Eggen's C- project.
Includes an [automatic test running script](#testpy-test-runner) and [a tool that builds an Eggen-style shar for you](#mkshar-shar-builder).

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
* coreutils (grep, script, sed)
* turnin (only needed to determine the due date)

## Getting the project
Most of the time, the project is already on the Osprey, which you can access using:
```shell
$ /tmp/just_do_it # only needed the first time you use mkshar/test.py
```

Once you have done the above, you can use:
```shell
$ test.py
```
or
```shell
$ mkshar
```

Since the `/tmp` folder on Osprey gets wiped periodically, you might want to keep a local copy.

The easiest way to download the project is using git:
```shell
$ git clone https://github.com/jonathan-lemos/cm-test-cases.git
```
I recommend you run the above command on the Osprey, as the Osprey has all of the required dependencies.

## `test.py` (test runner)
This script automatically runs a series of test cases on your project, similar to Eggen's grading script, telling you which ones failed.

Similar to Eggen's grading script, you must use `test.py` with a p-script generated from [mkshar](#mkshar-shar-builder) or one that you wrote yourself.

### Usage
If you are using the Osprey's copy of `test.py` (see [Getting the project](#getting-the-project)), you run it as follows:
```shell
$ test.py [p-script] [parser|lex_yacc|semantic_analyzer]
```
Note that the interpreter must be changed to `#!/usr/bin/python3.6` on Osprey if not already done so or the script will not work.

If you are not using the Osprey's copy of `mkshar`, `cd` to the project's directory and run the following:
```shell
$ ./test.py [p-script] [parser|lex_yacc|semantic_analyzer] [flags...]?
```

#### Example
```shell
$ test.py p2 parser
```
tests the project using the `p2` p-script in the current directory on the parser test cases.

#### `[p-script]`
This is a path to your p-script.

Your p-script must take a single command line argument and run a program that prints `ACCEPT` or `REJECT` to the screen on its own line.

#### `[parser|lex_yacc|semantic_analyzer]`
* `parser` - Runs the parser test cases.
* `lex_yacc` - Runs the lex/yacc test cases. *This is not the lexer*.
* `semantic_analyzer` - Runs the semantic analyzer test cases.

#### `[flags...]?`
* `--help` - Prints a help message.
* `--single-threaded` - Runs a single test case at a time instead of multiple. Use this if your project creates intermediate files.

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
	* The p-script is a script that runs your project with a single argument if it is invoked like `./p1 filename.txt`
	* **This means your project must accept a filename as its first command-line argument.**
		* Python projects should `import sys` and then use `sys.argv[1]` to access this argument.
		* Java projects should use `args[0]` from `public static void main(String[] args)`
		* C projects should use `argv[1]` from `int main(int argc, char** argv)`
* documentation file (you will be required to fill in some details)

The script will always generate the following:
* typescript
* the output shar (called `out_fn`)

### Usage
If you are using the Osprey's copy of `mkshar` (see [Getting the project](#getting-the-project)), you run it as follows:
```shell
$ mkshar [directory] [project number] [main executable/class] [test file] [turnin code]?
```

If you are not using the Osprey's copy of `mkshar`, `cd` to the project's directory and run the following:
```shell
$ ./mkshar [directory] [project number] [main executable/class] [test file] [turnin code]?
```

The outputted shar will be in your project directory and called `out_fn`.
`mkshar` will give instructions on how to test the created shar and how to turn it in if it creates the shar successfully.

#### Example
```shell
$ mkshar . 2 main.py testcase.cm ree4620_2
```
makes a shar out of a parser in the current directory, running from `main.py` and being tested with `testcase.cm`.

#### `[directory]`
This is the directory that contains all of your project's files and a single test case to demo the project with.

On Linux, `.` refers to the current directory, so if you are in your project's directory, you can just pass `.` as the argument.

#### `[project number]`
This is `1` for the lexer, `2` for the parser, etc.

This is needed to make sure the p-script gets called `p1`, `p2` etc.

#### `[main executable/class]`
This is the executable/class that contains your `main()` function/method.

For Python projects, this is your main `.py` file.

For Java projects, this is your `MainClass`.

For C projects, this can be whatever you want, e.g. (`a.out`), as long as it isn't the name of an existing file in your project.

#### `[test file]`
This is a file to demo your project with.

This file will be fed to your program to make a typescript that shows your project working.

The given path can either be an absolute path, or a path relative to your project's directory.

#### `[turnin code]?`
This is the `turnin` code for the project.

It is only needed to determine the due date for the project if your documentation file does not exist.

**`mkshar` does not turn in the project for you.**

If you know the due date for the project, or you already have a documentation file, you do not have to give this argument.

