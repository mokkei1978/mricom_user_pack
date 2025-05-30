cmake_minimum_required(VERSION 3.25.1)

enable_language(Fortran)

project(test Fortran)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

set(CMAKE_Fortran_COMPILER gfortran)

find_package(NetCDF MODULE REQUIRED COMPONENTS C)
find_package(wgrib2)

add_executable(main src/main.F90)

target_link_libraries(main PUBLIC wgrib2::wgrib2_ftn_api)
