# Conan NATS C-Client

This repository contains the conan receipe that is used to build the CNats packages at [rgpaul bintray](https://bintray.com/manromen/rgpaul).

For Infos about the NATS C-Client library please visit [Github](https://github.com/nats-io/cnats).
The library is licensed under the [Apache 2.0 License](https://github.com/nats-io/cnats/blob/master/LICENSE).
This repository is licensed under the [MIT License](LICENSE).

## macOS

To create a package for macOS you can run the conan command like this:

`conan create . cnats/1.7.6@rgpaul/stable -s os=Macos -s os.version=10.14 -s arch=x86_64 -s build_type=Release -o shared=False`

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Xcode](https://developer.apple.com/xcode/)
