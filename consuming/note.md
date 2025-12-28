## conan 笔记

### 命令

```sh
# 检测本机环境，生成profile
conan profile detect --force

# 安装库并生成相关文件
conan install . \ 
    --output-folder=build \
    --build=missing

# 使用--settings可以修改profile中的设定，如build_type=Debug可以改定build_type
conan install . \
    --output-folder=build \
    --build=missing \
    --settings=build_type=Debug

# 使用--options可以修改包级别的选项
conan install . \
    --output-folder=build \
    --build=missing \
    --options=zlib/1.3.1:shared=True

# 使用--build可以需要从源码构建的包
onan install . \
    --output-folder=build \
    --build=zlib* \
    --options=zlib/1.3.1:shared=True

# 如果使用cmake
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake -DCMAKE_TYPE=Release
cmake --build .
```

### 构建流程

1. 写配置
   ```py
   import os
   # 导入ConanFile类
   from conan import ConanFile
   # 导入Conan的CMake工具，cmake_layout可以指定项目的结构，如generators目录，build目录，CMake可用来集成CMake的构建流程
   from conan.tools.cmake import cmake_layout,CMake
   from conan.tools.files import copy
   
   # 继承ConanFile类
   class CompressorRecipe(ConanFile):
       # settings 类属性定义了项目范围内的变量，例如编译器、其版本或操作系统本身，这些变量可能会在我们构建项目时发生变化。
       settings = "os","compiler","build_type","arch"
       # generators 类属性指定在调用 conan install 命令时将运行哪些 Conan 生成器。
       generators = "CMakeToolchain","CMakeDeps"
       
       # 声明依赖
       def requirements(self):
           self.requires("zlib/1.3.1")
           if self.settings.os == "Windows":
               self.requires("base64/0.4.0")
       # 声明构建环境
       def build_requirements(self):
           if self.settings.os != "Windows":
               self.tool_requires("cmake/3.27.9")
   
       # 定义项目结构
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
   
       # 集成cmake构建
       def build(self):
           cmake=CMake(self)
           cmake.configure()
           cmake.build()
   ```
2. 使用`conan install . --output-folder=build `安装依赖和环境
3. 在build目录下有`conanbuild.sh`,使用`source conanbuild.sh`读取编译所需环境变量。
4. 按照cmake编译流程编译

- 有定义`build()`函数时可以直接在`conanfile.py`所在目录下运行`conan build .`编译项目，并且`--settings选项仍能生效`，如使用`conan build . --settings=build_type=Realse`可以指定`BUILD_TYPE`。
