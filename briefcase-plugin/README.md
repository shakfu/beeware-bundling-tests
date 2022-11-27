# What is this

Beginnings of a [briefcase](https://github.com/beeware/briefcase) plugin for cmake


## Requirements

As per Russell Keith-Magee's [advice](https://github.com/beeware/briefcase-macOS-Xcode-template/issues/16): 

> A standalone plugin would involve:

> "A GitHub repo acting as a cookiecutter template for a project. This is the analog of this project (briefcase-macOS-Xcode-template), except generating a Cmake project.
A Python module that registers a briefcase.formats.macOS entry point, exposing
a variable matching each of the supported commands (create, build, run etc).

> You should be able to use an existing backend (e.g.,
https://github.com/beeware/briefcase/blob/main/src/briefcase/platforms/macOS/xcode.py)
as a model for what is needed here. The key pieces you need to implement are
the paths to the key pieces (such as the location of the binary that is
generated), and the specific command needed to build the project."




