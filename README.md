# Metashade glTF Demo

This demo uses the third-party [pygltflib](https://pypi.org/project/pygltflib/) to parse glTF assets and generate HLSL shaders that can be rendered with [a fork of the Cauldron glTFSample](https://github.com/metashade/glTFSample/tree/metashade_demo).
The goal is to demonstrate that [Metashade](https://github.com/metashade/metashade) can generate sufficiently complex renderable shaders and that it can be integrated with other Python libraries and content production pipelines.

## Getting started

First, clone the repo, recursing into submodules:

```bash
git clone --recurse-submodules https://github.com/metashade/metashade-glTFSample.git
cd metashade-glTFSample
```

### Dependencies

This project uses pinned dependencies for reproducible builds:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install exact dependency versions
pip install -r requirements.txt

# Install project in development mode
pip install -e .
```

**Alternative (may get newer dependency versions):**
```bash
pip install -e .
```

The demo uses the following directory structure:

   * [glTFSample](https://github.com/metashade/glTFSample/tree/metashade_demo) - submodule pointing at https://github.com/metashade/glTFSample/tree/metashade_demo, which is a fork of https://github.com/GPUOpen-LibrariesAndSDKs/glTFSample - a C++ host app, originally developed by AMD to demo the rendering of glTF assets in DX12 and Vulkan.
      * [build](https://github.com/metashade/glTFSample/tree/metashade_demo/build) - the build directory for the above repo.
         * [DX12](glTFSample/build/DX12) - this directory will be created later by the [glTFSample](https://github.com/metashade/glTFSample/tree/metashade_demo) build and will contain the DX12-specific Visual Studio solution generated with CMake. It's added to [.gitignore](https://github.com/metashade/glTFSample/tree/metashade_demo/.gitignore).
            * [metashade-out](glTFSample/build/DX12/metashade-out) - this is where the Metashade demo will generate the HLSL shaders.
      * [libs/cauldron](https://github.com/metashade/Cauldron/tree/metashade_demo) - submodule pointing at https://github.com/metashade/Cauldron/tree/metashade_demo, a fork of https://github.com/GPUOpen-LibrariesAndSDKs/Cauldron, AMD's demo rendering framework.
      * [media/Cauldron-Media](https://github.com/metashade/Cauldron-Media) - submodule pointing at https://github.com/metashade/Cauldron-Media, cloned from https://github.com/GPUOpen-LibrariesAndSDKs/Cauldron-Media, which contains the glTF assets used in the demo.
   * [metashade](https://github.com/metashade/metashade) - submodule pointing at https://github.com/metashade/metashade
   * [src](src) - the demo code generating shaders with [metashade](https://github.com/metashade/metashade) for rendering with [glTFSample](https://github.com/metashade/glTFSample/tree/metashade_demo).

## Building glTFSample (C++ Host Application)

### Prerequisites

- [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/)
- [CMake 3.21](https://cmake.org/download/) or newer
- [Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk) (typically installed with Visual Studio)
- [Vulkan SDK 1.3.283](https://www.lunarg.com/vulkan-sdk/) or newer (required for Vulkan build and shader compilation tools)

### Build Steps

1. Initialize VCPKG (only needed once):
   ```bash
   ./vcpkg/bootstrap-vcpkg.bat
   ```

2. Configure and build:
   ```bash
   cmake --preset default
   cmake --build build
   ```
   
   Or open `build/metashade-glTFSample.sln` in Visual Studio 2022.

## Generating the shaders

The Python implementation of the demo requires [pygltflib](https://pypi.org/project/pygltflib/) to be installed:

```
pip install pygltflib
```

### [src/generate.py](src/generate.py) usage

```
--gltf-dir  Path to the source glTF assets
--out-dir   Path to the output directory
```

The script processes all glTF asset files it finds under the directory specified by `--gltf-dir` and writes the generated shader files to the directory specified by `--out-dir`.

The Visual Studio Code launch configurations in [.vscode/launch.json](.vscode/launch.json) execute the above script with the command-line arguments set to the appropriate paths in the demo's directory structure.

## Rendering with the generated shaders

In order to use the generated shaders with [glTFSample](https://github.com/metashade/glTFSample/tree/metashade_demo), their parent directory needs to be passed to the executable via a [command-line argument](https://github.com/metashade/glTFSample/blob/metashade_demo/readme.md#command-line-interface):

```
cd ..\build\bin\
GLTFSample_DX12.exe --metashade-out-dir=..\DX12\metashade-out
```

The names of the generated shader files are derived from the names of glTF meshes and primitives. [glTFSample](https://github.com/metashade/glTFSample/tree/metashade_demo) uses the same naming convention to find the right shaders at runtime and use them for rendering.

## Troubleshooting

### DXIL Signing (DX12)

When compiling HLSL shaders to DXIL using DXC, the `dxil.dll` library must be present in the same directory as `dxc.exe` for the shaders to be **signed**.

**Symptoms of unsigned shaders:**
- D3D12 error: "Input Signature in bytecode could not be parsed"
- `E_INVALIDARG` when creating graphics pipeline
- Warning during compilation: "DXIL signing library (dxil.dll) not found"

**Why this matters:**
- Unsigned DXIL may work on machines with Windows **Developer Mode** enabled
- Unsigned DXIL will **fail on end-user machines** without Developer Mode
- Even with Developer Mode, unsigned DXIL can cause validation layer crashes

**Solution:**
The VS Code launch configurations for shader generation include Cauldron's DXC (which has `dxil.dll`) in the PATH. When running shader generation from the command line, ensure a DXC with `dxil.dll` is in your PATH, or download the official [DirectXShaderCompiler release](https://github.com/microsoft/DirectXShaderCompiler/releases) which includes it.

