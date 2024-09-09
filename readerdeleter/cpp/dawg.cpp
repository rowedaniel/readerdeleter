#include <string>
#include <pybind11/pybind11.h>
#include <map>
#include <iostream>

class DAWGnode {
    public:
        bool terminal = true;
        std::map<char, DAWGnode*> children;
};

class DAWG {
    DAWGnode * root = new DAWGnode();

    public:
        void add_word(std::string word) {
            auto node = root;
            for(auto c : word) {
                if(node->children.find(c) == node->children.end()) {
                    // character not found
                    auto newNode =  new DAWGnode();
                    node->children[c] = newNode;
                    node->terminal = false;
                    node = newNode;
                    std::cout << "creating new node: " << c << std::endl;
                } else {
                    // character found
                    node = node->children[c];
                }
            }
        }

        bool is_word(std::string word) {
            auto node = root;
            for(auto c : word) {
                if(node->children.find(c) == node->children.end()) {
                    std::cout << "letter not found: " << c << std::endl;
                    return false;
                }
                std::cout << "letter found: " << c << ", and node terminality is " << node->terminal << std::endl;
                node = node->children[c];
            }
            std::cout << "node terminality is " << node->terminal << std::endl;
            if(node->terminal) {
                return true;
            }
            return false;
        }
};

int add(int a, int b) {return a+b;}


namespace py = pybind11;

PYBIND11_MODULE(dawg, m) {
    m.doc() = "Implementation of a DAWG in C++"; // Optional module docstring
                                                 //
    py::class_<DAWG>(m, "DAWG")
        .def(py::init<>())
        .def("add_word", &DAWG::add_word)
        .def("is_word", &DAWG::is_word);

}
