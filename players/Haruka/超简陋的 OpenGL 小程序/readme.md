# 超简陋的 OpenGL 小程序

（我真的完全不会图形学（但我竟然拿了一血 yay

下载下来发现是个 exe，并且我手头的多个 wine 版本都无法正常打开这个文件，于是只能点开瘟逗死虚拟机来跑这个程序了。

打开文件发现有一堵墙完全挡住了 flag 内容，但是 fragment shader 和 vertex shader 是明文存在一起的。

研究了一下 data.bin 但发现似乎是某种私有格式，.exe 拖 ida 也没有太看明白是怎么读的模型内容。（毕竟我不会这玩意

于是硬着头皮打开 shader 看了看，发现整个模型的位置是直接在 vertex shader 里通过 `gl_Position` 变量算出来的。于是自然想到，如果我让整个模型转个圈，不就能看到 flag 的内容了么？

于是快速在网上搜到了一段矩阵旋转的代码（我真的不会图形学）：

```c
mat4 rotationMatrix(vec3 axis, float angle)
{
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;

    return mat4(oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0,
                oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0,
                oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0,
                0.0,                                0.0,                                0.0,                                1.0);
}
```

然后把 `gl_Position` 乘上旋转矩阵：

```c
    mat4 rotated = rotationMatrix(vec3(0.0, 1.0, 0.0), 3.2);
    gl_Position = projection * view * vec4(FragPos, 0.7) * rotated;
```

通过多次尝试加上略微改一下 fragment shader 里的光照强度（`ambientStrength`），最终终于看清了整个 flag 的内容（

（看了一眼题解，感觉但凡有一点图形学基础就知道大概思路，然而我感觉我完全是 cheese 过去的（（