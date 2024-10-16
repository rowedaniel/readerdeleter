cmake_minimum_required(VERSION 3.4)
project(dafsa)

set(CMAKE_PREFIX_PATH "/Users/rowedaniel/Documents/school/scrabble/.venv/lib/python3.12/site-packages/pybind11" ${CMAKE_PREFIX_PATH})

find_package(pybind11 REQUIRED)

pybind11_add_module(dafsa cpp/dafsa.cpp)
pybind11_add_module(boardsearch cpp/boardsearch.cpp)

