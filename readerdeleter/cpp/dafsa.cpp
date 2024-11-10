/**
 * Implements a DAFSA
 * based on this paper: https://aclanthology.org/J00-1002.pdf
 */

#include <iostream>
#include <list>
#include <unordered_map>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

#include "alphabet.h"

class DAFSAnode {
public:
  bool terminal = false;
  DAFSAnode* children[alphabet_plus_len];

  DAFSAnode() {
    for(int i=0; i<alphabet_plus_len; ++i)
      children[i] = NULL;
  }

  bool is_null_child(char c) {
    return children[get_char_plus_num(c)] == NULL;
  }

  bool is_empty() {
    for(int i=0; i<alphabet_plus_len; ++i) {
      if(children[i] != NULL)
        return false;
    }
    return true;
  }

  friend bool operator==(const DAFSAnode& a, const DAFSAnode& b) {
    if (a.terminal != b.terminal) {
      return false;
    }

    // transitions are the same
    for (int i=0; i<alphabet_plus_len; ++i) {
      if(b.children[i] != a.children[i])
        return false;
    }

    return true;
  }

};

template <>
struct std::hash<DAFSAnode> {
  size_t operator()(const DAFSAnode& n) const noexcept {
    size_t hash = std::hash<bool>{}(n.terminal);
    for(int i = 0; i<alphabet_plus_len; ++i) {
      // combine hash with hash of (i, ith child)
      hash ^= std::hash<size_t>{}(std::hash<DAFSAnode*>{}(n.children[i])*i);
    }
    return hash;
  }
};

class DAFSA {

private:
  std::string previous_word = "";
  /*std::list<DAFSAnode *> rep_reg_cache = {};*/
  std::unordered_map<DAFSAnode, DAFSAnode*> rep_reg_cache;

  std::string get_prefix(std::string word) {
    /** Get common prefix between word and previous word
     *
     * Note: this is slightly different than the epynomous function from the
     * paper. Its behavior should be equivalent, though (I hope).
     */
    int prefix;
    for (prefix = 0; prefix < (int)word.length(); ++prefix) {
      if (word[prefix] != previous_word[prefix])
        break;
    }
    return word.substr(0, prefix);
  }

  DAFSAnode *traverse(DAFSAnode *state, std::string word) {
    /** This is equivalent to delta* in the paper.
     * It is used here as a helper function
     */
    auto node = state;
    for(auto c : word) {
      if(node == NULL)
        return NULL;
      node = node->children[get_char_plus_num(c)];
    }
    return node;
  }

  void add_suffix(DAFSAnode *state, std::string word) {
    // naively add the word, as if in a trie
    auto node = state;
    for (auto c : word) {
      if (node->is_null_child(c)) {
        // character not found
        auto newNode = new DAFSAnode();
        node->children[get_char_plus_num(c)] = newNode;
        node = newNode;
      } else {
        // character found
        node = node->children[get_char_plus_num(c)];
      }
    }
    node->terminal = true;
  }

  int last_child_key(DAFSAnode *state) {
    for(int i=alphabet_plus_len-1; i>=0; --i) {
      if(state->children[i] != NULL)
        return i;
    }
    return -1;
  }


  void replace_or_register(DAFSAnode *state) {
    // exit condition---should only trigger if finish() is called with no words
    // having been passed in
    if (state->is_empty())
      return;

    int child_key = last_child_key(state);
    auto child = state->children[child_key];

    if (!child->is_empty())
      replace_or_register(child);

    // check equivalency
    if(rep_reg_cache.find(*child) != rep_reg_cache.end()) {
      DAFSAnode* prev_node = rep_reg_cache[*child];
      state->children[child_key] = prev_node;
      delete child;
      return;
    }

    // no equivalent state exists, add to cache
    rep_reg_cache[*child] = child;
  }

public:
  DAFSAnode *root = new DAFSAnode();

  void add_word(std::string word) {
    /** Add word to the DAFSA structure **/

    // assume words are added in order
    if (word < previous_word) {
      exit(1);
    }

    auto prefix = get_prefix(word);
    auto last_state = traverse(root, prefix);
    auto current_suffix = word.substr(prefix.length());
    if (!last_state->is_empty())
      replace_or_register(last_state);
    add_suffix(last_state, current_suffix);

    previous_word = word;
  }

  void add_words(std::list<std::string> words) {
    int i=0;
    for(std::string word : words) {
      add_word(word);
      if(++i % 1000 == 0)
        std::cout << i << ": " << word << std::endl;
    }
  }

  void finish() { replace_or_register(root); }

  bool is_word(std::string word) {
    auto node = traverse(root, word);
    return node != NULL && node->terminal;
  }

  std::map<char, int> next_characters(std::string word) {
    auto node = traverse(root, word);
    if (node == NULL)
      return {};

    std::map<char, int> node_arrows;
    for (int i=0; i<alphabet_plus_len; ++i) {
      if(node->children[i] == NULL)
        continue;
      node_arrows[alphabet_plus[i]] = (long int)node->children[i];
    }
    return node_arrows;
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
      .def("add_words", &DAFSA::add_words)
      .def("is_word", &DAFSA::is_word)
      .def("next_characters", &DAFSA::next_characters)
      .def("finish", &DAFSA::finish);
}
