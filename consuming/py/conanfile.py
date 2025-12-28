import os
from conan import ConanFile
from conan.tools.cmake import cmake_layout,CMake
from conan.tools.files import copy

class CompressorRecipe(ConanFile):
    settings = "os","compiler","build_type","arch"
    generators = "CMakeToolchain","CMakeDeps"

    def requirements(self):
        self.requires("zlib/1.3.1")
        if self.settings.os == "Windows":
            self.requires("base64/0.4.0")
    
    def build_requirements(self):
        if self.settings.os != "Windows":
            self.tool_requires("cmake/3.27.9")

    def layout(self):
        # cmake_layout(self)
        multi = True if self.settings.get_safe("compiler")=="msvc" else False
        if multi:
            self.folders.generators=os.path.join("build","generators")
            self.folders.build="build"
        else:
            self.folders.generators=os.path.join("build",str(self.settings.build_type),"generators")
            self.folders.build=os.path.join("build",str(self.settings.build_type))

    def generate(self):
        # Copy all resources from the dependency's resource directory
        # to the "assets" folder in the source directory of your project
        # dep = self.dependencies["dep_name"]
        # copy(self, "*", dep.cpp_info.resdirs[0], os.path.join(self.source_folder, "assets"))
        pass

    def build(self):
        cmake=CMake(self)
        cmake.configure()
        cmake.build()