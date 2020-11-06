# Source code for glHackergame

基本上就是 LearnOpenGL 的 2.1 basic_lighting 代码魔改。

util/converter.cpp 用于生成 data.bin，简单粗暴。

只在 Windows + Visual Studio 2019 上面测试过可用，不过用到的库都是跨平台的，理论上不会出什么问题。

> .blend 用 blender 打开后，选择生成 fbx，然后才会被使用 assimp 的 converter 识别。