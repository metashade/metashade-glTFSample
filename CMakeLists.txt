cmake_minimum_required(VERSION 3.15)
project(metashade-glTFSample)

# glTFSample uses CMAKE_HOME_DIRECTORY to locate the bin directory. 
# We override it here to redirect output to build/bin without modifying the submodule.
# This prevents the submodule from polluting the root directory.
set(CMAKE_HOME_DIRECTORY ${CMAKE_BINARY_DIR})

add_subdirectory(glTFSample)

find_package(Boost REQUIRED COMPONENTS program_options format)

if(TARGET GLTFSample_DX12)
    target_link_libraries(GLTFSample_DX12 PRIVATE Boost::program_options Boost::format)
    set_target_properties(GLTFSample_DX12 PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
    foreach( CHANGE_CONFIG ${CMAKE_CONFIGURATION_TYPES} )
        string( TOUPPER ${CHANGE_CONFIG} CHANGE_CONFIG )
        set_target_properties(GLTFSample_DX12 PROPERTIES RUNTIME_OUTPUT_DIRECTORY_${CHANGE_CONFIG} "${CMAKE_BINARY_DIR}/bin")
    endforeach()
endif()

if(TARGET GLTFSample_VK)
    target_link_libraries(GLTFSample_VK PRIVATE Boost::program_options Boost::format)
    set_target_properties(GLTFSample_VK PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
    foreach( CHANGE_CONFIG ${CMAKE_CONFIGURATION_TYPES} )
        string( TOUPPER ${CHANGE_CONFIG} CHANGE_CONFIG )
        set_target_properties(GLTFSample_VK PROPERTIES RUNTIME_OUTPUT_DIRECTORY_${CHANGE_CONFIG} "${CMAKE_BINARY_DIR}/bin")
    endforeach()
endif()
