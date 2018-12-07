from conans import ConanFile, CMake, tools
import os

class CNatsConan(ConanFile):
    name = "CNats"
    version = "1.8.0"
    author = "Ralph-Gordon Paul (gordon@rgpaul.com)"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "android_ndk": "ANY", "android_stl_type":["c++_static", "c++_shared"]}
    default_options = "shared=False", "android_ndk=None", "android_stl_type=c++_static"
    description = "A C-Client Library for NATS"
    url = "https://github.com/Manromen/conan-cnats-scripts"
    license = "Apache-2.0"
    exports_sources = "cmake-modules/*"
    generators = "cmake"

    # download sources
    def source(self):
        url = "https://github.com/nats-io/cnats/archive/v%s.tar.gz" % self.version
        tools.get(url)

        tools.replace_in_file("%s/cnats-%s/CMakeLists.txt" % (self.source_folder, self.version),
            "project(cnats)",
            """project(cnats)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup() """)

    # compile using cmake
    def build(self):
        cmake = CMake(self)
        cmake.verbose = True

        cmake.definitions["NATS_BUILD_WITH_TLS"] = "ON"

        if self.settings.os == "Macos":
            cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = tools.to_apple_arch(self.settings.arch)

        library_folder = "%s/cnats-%s" % (self.source_folder, self.version)

        cmake.configure(source_folder=library_folder)
        cmake.build()
        cmake.install()

        lib_dir = os.path.join(self.package_folder,"lib")

        if self.settings.os == "Macos":
            # delete shared artifacts for static builds and the static library for shared builds
            if self.options.shared == False:
                for f in os.listdir(lib_dir):
                    if f.endswith(".dylib"):
                        os.remove(os.path.join(lib_dir,f))
                    elif f.endswith("libnats_static.a"):
                        os.rename(os.path.join(lib_dir,f), os.path.join(lib_dir,"libnats.a"))
            else:
                for f in os.listdir(lib_dir):
                    if f.endswith(".a"):
                        os.remove(os.path.join(lib_dir,f))

    def requirements(self):
        self.requires("LibreSSL/2.8.2@rgpaul/stable")

#    def package(self):
#        self.copy("*", dst="include", src='include')
#        self.copy("*.lib", dst="lib", src='lib', keep_path=False)
#        self.copy("*.dll", dst="bin", src='bin', keep_path=False)
#        self.copy("*.so", dst="lib", src='lib', keep_path=False)
#        self.copy("*.dylib", dst="lib", src='lib', keep_path=False)
#        self.copy("*.a", dst="lib", src='lib', keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ['include']

    def config_options(self):
        # remove android specific option for all other platforms
        if self.settings.os != "Android":
            del self.options.android_ndk
            del self.options.android_stl_type
