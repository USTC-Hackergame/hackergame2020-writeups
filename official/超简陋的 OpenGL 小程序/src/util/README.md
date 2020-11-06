# Converter for model data

This is used to convert from `.fbx` to plain binary.

The resulting data will be
```c++
struct Vertex {
    // position
    float Position[3];
    // normal
    float Normal[3];
    // texCoords
    float TexCoords[2];
};
```

and
```c++
std::vector<uint32_t> indices;
```

respectively.

## Compiling
This requires assimp 5.0.1 to build.

Linux:
```bash
g++ converter.cpp -o converter -lassimp
```