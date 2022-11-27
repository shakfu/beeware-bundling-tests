# beeware-bundling-tests

A bunch of experiments using the amazing [beeware](https://github.com/beeware) toolkit


## Do this first:

Run the following to download Python3.10 release from Beeware's github repo (change version as required)

```bash
./setup.sh
```


## Status of Tests / Experiments

- [x] [test-xcode](test-xcode): bundling python apps using [this](https://github.com/beeware/briefcase-macOS-Xcode-template) [beeware](https://github.com/beeware) and xcode.

	This standard, albeit manual, method works as expected and is the reference in these experiments. The quickest method is to the use the beeware [briefcase](https://github.com/beeware/briefcase) tool.

- [ ] [test-cmake-objc](test-cmake-objc): using `cmake` as the build mechanism but the same objc (`main.m`) entry point as `text-xcode`.

	Proof-of-concept is working, need to develop corresponding [briefcase-plugin](briefcase-plugin/cmake.py) and create a cookiecutter template.

- [ ] [test-cmake-c](test-cmake-c): using `cmake` as the build mechanism but with entry point written in c (`main.c`).

	Not working yet.

