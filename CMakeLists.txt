cmake_minimum_required(VERSION 3.15)
project(MetashadeSuperRepo)

add_subdirectory(glTFSample)

find_package(Boost REQUIRED COMPONENTS program_options format)

if(TARGET GLTFSample_DX12)
    target_link_libraries(GLTFSample_DX12 PRIVATE Boost::program_options Boost::format)
endif()

if(TARGET GLTFSample_VK)
    target_link_libraries(GLTFSample_VK PRIVATE Boost::program_options Boost::format)
endif()
