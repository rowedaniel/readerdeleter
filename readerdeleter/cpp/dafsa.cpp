/**
 * Implements a DAFSA
 * based on this paper: https://aclanthology.org/J00-1002.pdf
 */

#include <iostream>
#include <list>
#include <map>
#include <pybind11/pybind11.h>
#include <string>

class DAFSAnode {
public:
  bool terminal = false;
  // TODO: change from using std::map to something more suited
  // (see
  // https://martin.ankerl.com/2022/08/27/hashmap-bench-01/#access--find-benchmarks)
  // Perhaps the right way is simply an array of pointers length of alphabet?
  std::map<char, DAFSAnode *> children;
};

class DAFSA {

private:
  std::string previous_word = "";
  std::list<DAFSAnode *> rep_reg_cache = {};
  DAFSAnode *root = new DAFSAnode();

  std::string get_prefix(std::string word) {
    /** Get common prefix between word and previous word
     *
     * Note: this is slightly different than the epynomous function from the
     * paper. Its behavior should be equivalent, though (I hope).
     */
    int prefix;
    for (prefix = 0; prefix < word.length(); ++prefix) {
      if (word[prefix] != previous_word[prefix])
        break;
    }
    return word.substr(0, prefix);
  }

  DAFSAnode *traverse(DAFSAnode *state, std::string word) {
    /** This is equivalent to delta* in the paper.
     * It is used here as a helper function
     */
    if (word.length() == 0)
      return state;

    auto c = word[0];
    if (state->children.find(c) == state->children.end()) {
      return NULL;
    }

    return traverse(state->children[c], word.substr(1));
  }

  void add_suffix(DAFSAnode *state, std::string word) {
    // naively add the word, as if in a trie
    auto node = state;
    for (auto c : word) {
      if (node->children.find(c) == node->children.end()) {
        // character not found
        auto newNode = new DAFSAnode();
        node->children[c] = newNode;
        node = newNode;
        std::cout << "creating new node: " << c << "(" << node << ")"
                  << std::endl;
      } else {
        // character found
        node = node->children[c];
      }
    }
    node->terminal = true;
  }

  char last_child_key(DAFSAnode *state) {
    return state->children.rbegin()->first;
  }

  bool equiv(DAFSAnode *a, DAFSAnode *b) {
    std::cout << "testing equivalence of " << a << " and " << b << std::endl;
    if (a->terminal != b->terminal) {
      std::cout << "don't agree on terminality :(  a->terminal: " << a->terminal
                << ", and b->terminal: " << b->terminal << std::endl;
      return false;
    }

    // transitions are the same
    for (auto t = a->children.begin(); t != a->children.end(); ++t) {
      if (b->children.find(t->first) == b->children.end() ||
          b->children[t->first] != t->second) {
        std::cout << "no agreement on " << t->first << std::endl;
        return false;
      }
    }
    for (auto t = b->children.begin(); t != b->children.end(); ++t) {
      if (a->children.find(t->first) == a->children.end() ||
          a->children[t->first] != t->second) {
        std::cout << "no agreement on " << t->first << std::endl;
        return false;
      }
    }

    return true;
  }

  void replace_or_register(DAFSAnode *state) {
    auto child_key = last_child_key(state);
    auto child = state->children[child_key];

    if (!child->children.empty())
      replace_or_register(child);

    for (auto q : rep_reg_cache) {
      if (equiv(q, child)) {
        std::cout << "Redundant node found for child '" << child_key
                  << "'. Deleting" << std::endl;
        state->children[child_key] = q;
        delete child;
        return;
      }
    }

    // no equivalent state exists
    rep_reg_cache.push_back(child);
  }

public:
  void add_word(std::string word) {
    /** Add word to the DAFSA structure **/

    // assume words are added in order
    if (word < previous_word) {
      std::cout << "attempted to add words out of order" << std::endl;
    }

    std::cout << "Getting prefix: ";
    auto prefix = get_prefix(word);
    std::cout << prefix << std::endl;

    std::cout << "Getting last state: ";
    auto last_state = traverse(root, prefix);
    std::cout << last_state << std::endl;

    std::cout << "Getting current suffix: ";
    auto current_suffix = word.substr(prefix.length());
    std::cout << current_suffix << std::endl;

    if (!last_state->children.empty()) {
      std::cout << "replacing or registering " << std::endl;
      replace_or_register(last_state);
    }

    std::cout << "Adding suffix" << std::endl;
    add_suffix(last_state, current_suffix);

    previous_word = word;

    std::cout << "Register presently looks like: [";
    for (auto it : rep_reg_cache) {
      std::cout << it << ", ";
    }
    std::cout << "]" << std::endl;
  }

  void finish() { replace_or_register(root); }

  bool is_word(std::string word) {
    auto node = traverse(root, word);
    return node != NULL && node->terminal;
  }
};

int add(int a, int b) { return a + b; }

namespace py = pybind11;

PYBIND11_MODULE(dafsa, m) {
  m.doc() = "Implementation of a DAFSA in C++"; // Optional module docstring
                                                //
  py::class_<DAFSA>(m, "DAFSA")
      .def(py::init<>())
      .def("add_word", &DAFSA::add_word)
      .def("is_word", &DAFSA::is_word)
      .def("finish", &DAFSA::finish);
}
