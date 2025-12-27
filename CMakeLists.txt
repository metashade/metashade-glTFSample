cmake_minimum_required(VERSION 3.15)
project(metashade-glTFSample)

# glTFSample uses CMAKE_HOME_DIRECTORY to locate its bin directory.
# Override it to ${CMAKE_BINARY_DIR} so the submodule writes binaries to build/bin
# (the build tree) instead of the project root source directory.
set(CMAKE_HOME_DIRECTORY ${CMAKE_BINARY_DIR})

# Force the 'INSTALL' target to run as part of the default build in Visual Studio.
# This ensures that 'glTFSample/bin' is automatically updated when you build/launch (F5).
set(CMAKE_VS_INCLUDE_INSTALL_TO_DEFAULT_BUILD 1)

# Add the glTFSample submodule.
add_subdirectory(glTFSample)

# Use standard CMake install functionality to place artifacts in glTFSample/bin.
# This ensures a clean source tree (building in build/) while satisfying asset path requirements.
install(TARGETS GLTFSample_DX12 GLTFSample_VK
    RUNTIME DESTINATION bin
)

# Install required DLLs (use Boost imported target to get the correct DLL)
install(FILES $<TARGET_FILE:Boost::program_options>
    DESTINATION bin
)

# Install assets that the submodule generates/copies to the build directory
# Since the submodule doesn't have its own install rules, we pick them up from the build output.
install(FILES "${CMAKE_BINARY_DIR}/bin/GLTFSample.json"
              "${CMAKE_BINARY_DIR}/bin/brdfLut.dds"
              "${CMAKE_BINARY_DIR}/bin/WinPixEventRuntime.dll"
              "${CMAKE_BINARY_DIR}/bin/amd_ags_x64.dll"
              "${CMAKE_BINARY_DIR}/bin/dxcompiler.dll"
              "${CMAKE_BINARY_DIR}/bin/dxil.dll"
    DESTINATION bin
)

install(DIRECTORY "${CMAKE_BINARY_DIR}/bin/ShaderLibDX"
        "${CMAKE_BINARY_DIR}/bin/ShaderLibVK"
    DESTINATION bin
)

# Install PDBs for debugging (CMake doesn't install them by default on Windows)
if(MSVC)
    install(FILES $<TARGET_PDB_FILE:GLTFSample_DX12> DESTINATION bin OPTIONAL)
    install(FILES $<TARGET_PDB_FILE:GLTFSample_VK> DESTINATION bin OPTIONAL)
endif()

find_package(Boost REQUIRED COMPONENTS program_options format)

if(TARGET GLTFSample_DX12)
    target_link_libraries(GLTFSample_DX12 PRIVATE Boost::program_options Boost::format)
    set_target_properties(GLTFSample_DX12 PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
    
    # Configure Visual Studio to debug the INSTALLED executable (in glTFSample/bin)
    set_target_properties(GLTFSample_DX12 PROPERTIES 
        VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/glTFSample/bin"
        VS_DEBUGGER_COMMAND "${CMAKE_SOURCE_DIR}/glTFSample/bin/$<TARGET_FILE_NAME:GLTFSample_DX12>"
    )

    foreach( CHANGE_CONFIG ${CMAKE_CONFIGURATION_TYPES} )
        string( TOUPPER ${CHANGE_CONFIG} CHANGE_CONFIG )
        set_target_properties(GLTFSample_DX12 PROPERTIES RUNTIME_OUTPUT_DIRECTORY_${CHANGE_CONFIG} "${CMAKE_BINARY_DIR}/bin")
    endforeach()
endif()

if(TARGET GLTFSample_VK)
    target_link_libraries(GLTFSample_VK PRIVATE Boost::program_options Boost::format)
    set_target_properties(GLTFSample_VK PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")

    # Configure Visual Studio to debug the INSTALLED executable
    set_target_properties(GLTFSample_VK PROPERTIES 
        VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/glTFSample/bin"
        VS_DEBUGGER_COMMAND "${CMAKE_SOURCE_DIR}/glTFSample/bin/$<TARGET_FILE_NAME:GLTFSample_VK>"
    )

    foreach( CHANGE_CONFIG ${CMAKE_CONFIGURATION_TYPES} )
        string( TOUPPER ${CHANGE_CONFIG} CHANGE_CONFIG )
        set_target_properties(GLTFSample_VK PROPERTIES RUNTIME_OUTPUT_DIRECTORY_${CHANGE_CONFIG} "${CMAKE_BINARY_DIR}/bin")
    endforeach()
endif()

