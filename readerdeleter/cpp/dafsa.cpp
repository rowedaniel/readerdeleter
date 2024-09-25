#include <string>
#include <pybind11/pybind11.h>
#include <map>
#include <iostream>

class DAFSAnode {
    public:
        bool terminal = false;
        std::map<char, DAFSAnode*> children;
};

class DAFSA {
    DAFSAnode * root = new DAFSAnode();
    std::string previous_word = "";

    private:
        int get_prefix(std::string word) {
            int prefix;
            for(prefix=0; prefix<word.length(); ++prefix) {
                if(word[prefix] != previous_word[prefix])
                    break;
            }
            return prefix;
        }

    public:
        void add_word(std::string word) {
            // assume words are added in order
            if(word < previous_word) {
                std::cout << "attempted to add words out of order" << std::endl;
            }

            int prefix = get_prefix(word);

            // naively add the word, as if in a trie
            auto node = root;
            for(auto c : word) {
                if(node->children.find(c) == node->children.end()) {
                    // character not found
                    auto newNode =  new DAFSAnode();
                    node->children[c] = newNode;
                    node = newNode;
                    std::cout << "creating new node: " << c << std::endl;
                } else {
                    // character found
                    node = node->children[c];
                }
            }
            node->terminal = true;
            previous_word = word;
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

PYBIND11_MODULE(dafsa, m) {
    m.doc() = "Implementation of a DAFSA in C++"; // Optional module docstring
                                                 //
    py::class_<DAFSA>(m, "DAFSA")
        .def(py::init<>())
        .def("add_word", &DAFSA::add_word)
        .def("is_word", &DAFSA::is_word);

}
