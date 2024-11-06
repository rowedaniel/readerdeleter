cmake_minimum_required(VERSION 3.5)
project(dafsa)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_PREFIX_PATH "/Users/rowedaniel/Documents/school/scrabble/.venv/lib/python3.13/site-packages/pybind11" ${CMAKE_PREFIX_PATH})

find_package(pybind11 REQUIRED)

pybind11_add_module(dafsa cpp/dafsa.cpp)
# pybind11_add_module(boardsearch cpp/boardsearch.cpp)

