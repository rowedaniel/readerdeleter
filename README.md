# Installation

## Python requirements
See pyproject.toml for the full list of requirements.
For running, you should need:
- pybind11
- numpy
- scipy
- matplotlib
- networkx
- torch (probably not necessary)
Install via pip (presumably in a venv):
```sh
python3 -m venv myEnv
source .venv/bin/activate
pip install pybind11 numpy scipy matplotlib networkx
```

## Building the c++
Next, you need to build the cpp part of the project. Apologies for the bad architecture here,
I'm not so familiar with c++/cmake projects.

Steps:
1. Change the path in `readerdeleter/CMakeLists.txt` to the python virtual environment path.
   For example, this could be
   ```cmake
    set(CMAKE_PREFIX_PATH "/path/to/project/.venv/lib/python3.13/site-packages/pybind11" ${CMAKE_PREFIX_PATH})
   ```

   You can find the correct directory by running
   ```sh
   python -m pybind11 --cmakedir
   ```
   in your virtual environment. It should print the correct path.

2. make a `build` directory under `readerdeleter/`
3. run
   ```sh
   cd build/
   cmake ..
   make
   ```

# Usage

