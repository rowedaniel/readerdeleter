cmake_minimum_required(VERSION 3.5)
project(dafsa)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_CXX_FLAGS "-Wall -Wextra")
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-Ofast")

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_PREFIX_PATH "/Users/rowedaniel/Documents/school/scrabble/.venv/lib/python3.11/site-packages/pybind11" ${CMAKE_PREFIX_PATH})

find_package(pybind11 REQUIRED)

pybind11_add_module(dafsa cpp/dafsa.cpp)
pybind11_add_module(boardsearch cpp/boardsearch.cpp)

