#include <iostream>
#include <cstdio>
#include <cassert>
#include <vector>

#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>

// This is used to export the meshes into vertex and index array
// Model is given by assimp

struct Vertex {
    // position
    float Position[3];
    // normal
    float Normal[3];
    // texCoords
    float TexCoords[2];
};

struct BlobHeader {
        uint32_t numVertices;
        uint32_t numIndices;
};

std::vector<Vertex> vertices;
std::vector<unsigned int> indices;

void processMesh(aiMesh *mesh, const aiScene *scene) {
    bool exportUV = true;
    if (mesh->mTextureCoords[0] == nullptr) {
        fprintf(stderr, "Warning: expected texture coordinates! Skipping UV export\n");
        exportUV = false;
    }

    // index: offset, ..., offset + mNumVertices - 1
    unsigned int offset = vertices.size();
    for (unsigned int i = 0; i < mesh->mNumVertices; i++) {
        struct Vertex vert;
        vert.Position[0] = mesh->mVertices[i].x;
        vert.Position[1] = mesh->mVertices[i].y;
        vert.Position[2] = mesh->mVertices[i].z;

        vert.Normal[0] = mesh->mNormals[i].x;
        vert.Normal[1] = mesh->mNormals[i].y;
        vert.Normal[2] = mesh->mNormals[i].z;

        // Only use the first set of texture coordinates
        if (exportUV) {
            vert.TexCoords[0] = mesh->mTextureCoords[0]->x;
            vert.TexCoords[1] = mesh->mTextureCoords[0]->y;
        } else {
            vert.TexCoords[0] = 0;
            vert.TexCoords[1] = 0;
        }

        vertices.push_back(vert);
    }

    for (unsigned int i = 0; i < mesh->mNumFaces; i++) {
        assert(mesh->mFaces[i].mNumIndices == 3);
        indices.push_back(offset + mesh->mFaces[i].mIndices[0]);
        indices.push_back(offset + mesh->mFaces[i].mIndices[1]);
        indices.push_back(offset + mesh->mFaces[i].mIndices[2]);
    }
}

void processNode(aiNode *node, const aiScene *scene) {
    for (unsigned int i = 0; i < node->mNumMeshes; i++) {
        std::cout << "Processing mesh..." << std::endl;
        aiMesh* mesh = scene->mMeshes[node->mMeshes[i]];
        processMesh(mesh, scene);
    }
    
    for (unsigned int i = 0; i < node->mNumChildren; i++) {
        processNode(node->mChildren[i], scene);
    }
}

int loadModel(const char *filePath) {
    Assimp::Importer importer;
    const aiScene* scene = importer.ReadFile(filePath, 
        aiProcess_Triangulate | aiProcess_GenSmoothNormals | 
        aiProcess_FlipUVs | aiProcess_CalcTangentSpace |
        aiProcess_JoinIdenticalVertices | aiProcess_PreTransformVertices);

    if(!scene || scene->mFlags & AI_SCENE_FLAGS_INCOMPLETE || !scene->mRootNode) // if is Not Zero
    {
        std::cout << "ERROR::ASSIMP:: " << importer.GetErrorString() << std::endl;
        return -1;
    }
    processNode(scene->mRootNode, scene);

    return 0;
}

int writeModel(const char *filePath) {
    // output as a plain blob
    FILE *fp = fopen(filePath, "wb");
    if (!fp) {
        fprintf(stderr, "ERROR: Can't open %s for writing, abort.\n", filePath);
        return -1;
    }
    
    struct BlobHeader bhdr;
    bhdr.numVertices = vertices.size();
    bhdr.numIndices = indices.size();

    int ret = fwrite(&bhdr, sizeof(bhdr), 1, fp);
    if (ret != 1) {
        fprintf(stderr, "ERROR: Writing header failed, abort. (ret=%d)\n", ret);
        return -1;
    }

    ret = fwrite(vertices.data(), sizeof(Vertex), vertices.size(), fp);
    if (ret != vertices.size()) {
        fprintf(stderr, "ERROR: Writing vertices failed, abort.\n");
        return -1;
    }

    ret = fwrite(indices.data(), sizeof(unsigned int), indices.size(), fp);
    if (ret != indices.size()) {
        fprintf(stderr, "ERROR: Writing indices failed, abort.\n");
        return -1;
    }

    fclose(fp);
    printf("Model writing successful.\n");
    return 0;
}

int main(int argc, char *argv[]) {
    assert(sizeof(Vertex) == 8 * sizeof(float));
    if (argc != 3) {
        fprintf(stderr, "Usage: %s model-path blob-name-to-be-exported\n", argv[0]);
        return 1;
    }

    if (loadModel(argv[1]) < 0) {
        fprintf(stderr, "Model loading failed. Abort.\n");
        return 1;
    }

    assert(indices.size() % 3 == 0);
    printf("Model loaded. Vertices: %d, Indices: %d (Faces: %d)\n", vertices.size(), indices.size(), indices.size() / 3);

    if (writeModel(argv[2]) < 0) {
        fprintf(stderr, "Model writing failed. Abort.\n");
        return 1;
    }

    return 0;
}