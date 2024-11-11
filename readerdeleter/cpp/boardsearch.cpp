/**
 * Creates a model of the board
 * based on
 * https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
 */
#include <cmath>
#include <cstdint>
#include <iostream>
#include <list>
#include <map>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

#include "dafsa.cpp"

using namespace std;

typedef char board_t[board_size][board_size];

class BoardSearch {
private:
  DAFSA tree;
  // count of every tile, plus blank tiles
  int rack_count[alphabet_len + 1] = {0};
  string rack_letters;
  uint32_t board_hori_mask[board_size][board_size];
  uint32_t board_vert_mask[board_size][board_size];

  board_t board_hori;
  board_t board_vert;

  bool is_anchor(board_t board, int row, int col) {
    return board[row][col] == ' ' &&
           ((row - 1 >= 0 && board[row - 1][col] != ' ') ||
            (col - 1 >= 0 && board[row][col - 1] != ' ') ||
            (row + 1 < board_size && board[row + 1][col] != ' ') ||
            (col + 1 < board_size && board[row][col + 1] != ' '));
  }

  bool is_vert_anchor(board_t board, int row, int col) {
    return ((row - 1 >= 0 && board[row - 1][col] != ' ') ||
            (row + 1 < board_size && board[row + 1][col] != ' '));
  }

  bool is_anchor_in_row(char board_row[board_size], int col) {
    return ((col - 1 >= 0 && board_row[col] != ' ') ||
            (col + 1 < board_size && board_row[col] != ' '));
  }

  void cross_checks(uint32_t mask[board_size][board_size], board_t board) {
    /**
     * for all spaces adjacent to other spaces, find all legal characters with
     * down words for that space
     */

    for (int row = 0; row < board_size; ++row) {
      for (int col = 0; col < board_size; ++col) {
        if (board[row][col] != ' ') {
          // occupied, mask has to be 0
          mask[row][col] = 0;
          continue;
        }
        if (!is_vert_anchor(board, row,
                            col)) // nothing above/below to connect to
          continue;

        // default to nothing allowed
        mask[row][col] = 0;

        // check every character here
        for (int i = 0; i < alphabet_len; ++i) {
          // get this character
          auto node = tree.root;
          if (node->children[i] == NULL)
            continue;
          node = node->children[i];

          int j = 1;
          // go up
          while (row - j >= 0 && board[row - j][col] != ' ') {
            if (node->is_null_child(board[row - j][col])) {
              break;
            }
            node = node->children[get_char_num(board[row - j][col])];
            ++j;
          }
          if (row - j >= 0 && board[row - j][col] != ' ') {
            // couldn't find a valid word before beginning of prefix
            continue;
          }

          // check pivot character
          if (node->is_null_child(delim))
            continue;
          node = node->children[get_char_num(delim)];

          // go down
          j = 1;
          while (row + j >= 0 && board[row + j][col] != ' ') {
            if (node->is_null_child(board[row + j][col])) {
              break;
            }
            node = node->children[get_char_num(board[row + j][col])];
            ++j;
          }
          if (board[row + j][col] != ' ') {
            // couldn't find a valid word before end of suffix
            continue;
          }

          // mark this letter as valid in this space
          mask[row][col] |= 1 << i;
        }
      }
    }
  }

  list<tuple<DAFSAnode *, string>> get_word_prefixes_in_row(uint32_t board_mask_row[board_size],
                                        char board_row[board_size], int col,
                                        DAFSAnode *node) {
    list<tuple<DAFSAnode*, string>> out = {};

    if (col < 0) {
      if (!node->is_null_child(delim))
        return {make_tuple(node->children[get_char_num(delim)], "")};
      return {};
    }
    if (board_row[col] != ' ') {
      if (node->is_null_child(board_row[col]))
        return {};
      DAFSAnode *child = node->children[get_char_num(board_row[col])];
      auto prefixes =
          get_word_prefixes_in_row(board_mask_row, board_row, col - 1, child);
      for (auto [n, prefix] : prefixes) 
        out.push_back(make_tuple(n, prefix + board_row[col]));
      return out;
    }

    if (!node->is_null_child(delim)) {
      // reached end of prefix
      out.push_back(make_tuple(node->children[get_char_num(delim)], ""));
    }

    for (char c : rack_letters) {
      int char_num = get_char_num(c);
      if (rack_count[char_num] == 0)
        continue;
      if (!((board_mask_row[col] >> char_num) & 0x1))
        continue;
      if (node->is_null_child(c))
        continue;
      DAFSAnode *child = node->children[get_char_num(c)];

      // using this character, remove it from the list of allowed characters
      --rack_count[char_num];

      // found valid letter, get further prefixes
      auto prefixes =
          get_word_prefixes_in_row(board_mask_row, board_row, col - 1, child);
      for (auto [n, prefix] : prefixes)
        out.push_back(make_tuple(n, prefix + c));


      // finished using this character, add it back to list of allowed
      // characters
      ++rack_count[char_num];
    }

    return out;
  }

  list<string> get_word_suffixes_in_row(uint32_t board_mask_row[board_size],
                                        char board_row[board_size], int col,
                                        DAFSAnode *node) {
    list<string> out = {};

    if (col >= board_size) {
      if (node->terminal)
        return {""};
      return {};
    }
    if (board_row[col] != ' ') {
      if (node->is_null_child(board_row[col]))
        return {};
      DAFSAnode *child = node->children[get_char_num(board_row[col])];
      auto suffixes =
          get_word_suffixes_in_row(board_mask_row, board_row, col + 1, child);
      for (auto suffix : suffixes)
        out.push_back(board_row[col]+suffix);
      return out;
    }

    // space is unfilled
    // check if terminal
    if(node->terminal)
      out.push_back("");

    for (char c : rack_letters) {
      int char_num = get_char_num(c);
      if (rack_count[char_num] == 0)
        continue;
      if (!((board_mask_row[col] >> char_num) & 0x1))
        continue;
      if (node->is_null_child(c))
        continue;
      DAFSAnode *child = node->children[get_char_num(c)];

      // using this character, remove it from the list of allowed characters
      --rack_count[char_num];

      // found valid letter, get further suffixes
      auto suffixes =
          get_word_suffixes_in_row(board_mask_row, board_row, col + 1, child);
      for (auto suffix : suffixes)
        out.push_back(c+suffix);

      // finished using this character, add it back to list of allowed
      // characters
      ++rack_count[char_num];
    }

    return out;
  }

  list<tuple<int, int, string>>
  get_words_in_row(uint32_t board_mask_row[board_size],
                   char board_row[board_size], int row, int col) {
    list<tuple<int, int, string>> out = {};

    // TODO: implement this correctly
    // first check if there's a prior anchor point connected by words
    // (in which case we've already got all words, so this computation is wasted)
    /*if(col > 0 && board_row[col-1] != ' ') {*/
    /*  for(int i=1; i>0; --i) {*/
    /*    if(is_anchor_in_row(board_row, col-i)) {*/
    /*      cout << "skipping" << endl;*/
    /*      return out;*/
    /*    }*/
    /*  }*/
    /*}*/


    cout << "getting prefixes" << endl;
    for (auto [n, prefix] :
         get_word_prefixes_in_row(board_mask_row, board_row, col, tree.root)) {
      int prefix_offset = 1 - prefix.length();
      cout << "got prefix: " << prefix << endl;

      // remove prefix items from rack
      for(int i=0; i<(int)prefix.length(); ++i) {
        if(board_row[col+prefix_offset+i] == ' ')
          --rack_count[get_char_num(prefix[i])];
      }

      list<string> suffixes = get_word_suffixes_in_row(board_mask_row, board_row, col+1, n);
      for(string suffix : suffixes)
          out.push_back(make_tuple(row, col - prefix.length() + 1, prefix+suffix));

      // add prefix items back to rack for next iteration
      for(int i=0; i<(int)prefix.length(); ++i) {
        if(board_row[col+prefix_offset+i] == ' ')
          ++rack_count[get_char_num(prefix[i])];
      }
    }
    return out;
  }

  list<tuple<int, int, string>>
  get_words(uint32_t board_mask[board_size][board_size], board_t board) {
    list<tuple<int, int, string>> out = {};

    for (int row = 0; row < board_size; ++row) {
      for (int col = 0; col < board_size; ++col) {
        // skip non-anchor spaces
        if (!is_anchor(board, row, col))
          continue;
        out.splice(out.end(),
                   get_words_in_row(board_mask[row], board[row], row, col));
      }
    }
    return out;
  }

public:
  BoardSearch(array<array<char, board_size>, board_size> board, string rack,
              DAFSA &wordlist) {
    /**
     * Setup to search board board, given rack rack and wordlist wordlist.
     * Note that wordlist should be formatted as a GADDAG
     */

    // set necessary vars
    tree = wordlist;
    rack_letters = rack;

    // getup transpose of board
    for (int row = 0; row < board_size; ++row) {
      for (int col = 0; col < board_size; ++col) {
        board_hori[row][col] = board[row][col];
        board_vert[row][col] = board[col][row];
      }
    }

    // init masks
    for (int i = 0; i < board_size; ++i) {
      for (int j = 0; j < board_size; ++j) {
        board_hori_mask[i][j] = 0xffffffff;
        board_vert_mask[i][j] = 0xffffffff;
      }
    }

    cross_checks(board_hori_mask, board_hori);
    cross_checks(board_vert_mask, board_vert); 

    for (auto c : rack)
      ++rack_count[get_char_num(c)];

  }

  list<tuple<int, int, int, string>> get_valid_words() {
    /**
     * Returns list of valid words, in format:
     * (start x, start y, left/right, word, score)
     */

    list<tuple<int, int, int, string>> words = {};
    for(auto [r, c, w] : get_words(board_hori_mask, board_hori)) {
      words.push_back(make_tuple(0, r, c, w));
    }
    for(auto [c, r, w] : get_words(board_vert_mask, board_vert)) {
      words.push_back(make_tuple(1, r, c, w));
    }
    return words;
  }
};

namespace py = pybind11;

PYBIND11_MODULE(boardsearch, m) {
  m.doc() = "Effecient wordfinding algorithm for SCRABBLE in C++";

  py::class_<BoardSearch>(m, "BoardSearch")
      .def(py::init<array<array<char, board_size>, board_size>, string,
                    DAFSA &>())
      .def("get_valid_words", &BoardSearch::get_valid_words);
}
