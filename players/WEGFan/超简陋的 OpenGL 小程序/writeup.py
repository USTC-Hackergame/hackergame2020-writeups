# -*- coding: utf-8 -*-
import struct

import matplotlib.pyplot as plt
import numpy as np
from more_itertools import chunked

with open('./data.bin', 'rb') as f:
    data = f.read()

(vertices_count, face_indecies_count) = struct.unpack_from('< i i', data, 0)
(vertices_raw, face_indecies_raw) = struct.unpack_from(f'{vertices_count * 4 * 8}s {face_indecies_count * 4}s', data, 8)

vertices = list(chunked(struct.unpack(f'< {len(vertices_raw) // 4}f', vertices_raw), 8))
face_indecies = list(chunked(struct.unpack(f'< {len(face_indecies_raw) // 4}i', face_indecies_raw), 3))

with open('./model.obj', 'w', encoding='utf-8') as f:
    for vertex in vertices:
        (pos_x, pos_y, pos_z) = vertex[:3]
        f.write(f'v {pos_x} {pos_y} {pos_z}\n')
        (normal_x, normal_y, normal_z) = vertex[3:6]
        f.write(f'vn {normal_x} {normal_y} {normal_z}\n')
    for face in face_indecies:
        (x, y, z) = face
        f.write(f'f {x + 1}//{x + 1} {y + 1}//{y + 1} {z + 1}//{z + 1}\n')

positions = [vertex[:3] for vertex in vertices]
(xs, ys, zs) = np.array(positions).transpose(1, 0)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))
ax.scatter(xs, ys, zs, s=0.1)

plt.show()
