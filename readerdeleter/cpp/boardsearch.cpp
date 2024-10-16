/**
 * Creates a model of the board
 * based on
 * https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
 */

#include <array>
#include <cstdint>
#include <iostream>
#include <list>
#include <map>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>

#include "alphabet.h"
#include "dafsa.cpp"

using namespace std;

typedef array<array<char, board_size>, board_size> board_t;

class BoardSearch {
private:
  DAFSA tree;
  int rack_count[alphabet_len + 1] = {
      0}; // count of every tile, plus blank tiles
  uint32_t board_hori_mask[board_size][board_size] = {{0}};
  uint32_t board_vert_mask[board_size][board_size] = {{0}};

  board_t board_hori;
  board_t board_vert;
  void cross_checks(uint32_t mask[board_size][board_size], board_t board) {
    /**
     * for all spaces adjacent to other spaces, find all legal characters with
     * down words for that space
     */

    for (int row = 0; row < board_size; ++row) {
      for (int col = 0; col < board_size; ++col) {

        // only cross-check spaces with words above/below
        // TODO: maybe generate anchors first, since we only need to generate
        // cross-check for anchors I think?
        if (board[row][col] != ' ' ||
            ((row - 1 < 0 || board[row - 1][col] == ' ') &&
             (row + 1 >= board_size || board[row + 1][col] == ' ')))
          continue;

        // check every character here
        for (int i = 0; i < alphabet_len; ++i) {

          // get this character
          auto node = tree.root;
          if (node->children.find(alphabet[i]) == node->children.end())
            continue;
          node = node->children[alphabet[i]];

          int j = 1;
          // go up
          while (row - j >= 0 && board[row - j][col] != ' ') {
            if (node->children.find(board[row - j][col]) ==
                node->children.end()) {
              break;
            }
            node = node->children[board[row - j][col]];
            j += 1;
          }
          if (board[row - j][col] != ' ') {
            // couldn't find a valid word before beginning of prefix
            continue;
          }

          // check pivot character
          if (node->children.find('+') == node->children.end()) {
            continue;
          }
          node = node->children['+'];

          // go down
          j = 1;
          while (row + j >= 0 && board[row + j][col] != ' ') {
            if (node->children.find(board[row + j][col]) ==
                node->children.end()) {
              break;
            }
            node = node->children[board[row + j][col]];
            j += 1;
          }
          if (board[row + j][col] != ' ') {
            // couldn't find a valid word before end of suffix
            continue;
          }

          if (node->terminal) {
            // mark this letter as valid in this space
            mask[row][col] |= 1 << i;
          }
        }
      }
    }
  }

  list<tuple<int, int, bool, string, int>> get_words(uint32_t board_mask[board_size][board_size]) {
    return {};
  }


public:
  BoardSearch(board_t board, string rack, DAFSA &wordlist) {
    /**
     * Setup to search board board, given rack rack and wordlist wordlist.
     * Note that wordlist should be formatted as a GADDAG
     */

    // set necessary vars
    tree = wordlist;
    board_hori = board;

    // getup transpose of board
    for (int row = 0; row < board_size; ++row) {
      for (int col = 0; col < board_size; ++col) {
        board_vert[row][col] = board_hori[col][row];
      }
    }

    // print some stuff
    cout << "board_hori: " << endl;
    for (auto row : board_hori) {
      for (auto col : row) {
        cout << col;
      }
      cout << endl;
    }

    cross_checks(board_hori_mask, board_hori);
    /*cross_checks(board_vert_mask, board_vert);*/

    // print some more stuff
    cout << "board_vert: " << endl;
    for (auto row : board_vert) {
      for (auto col : row) {
        cout << col;
      }
      cout << endl;
    }

    for (auto c : rack)
      ++rack_count[get_char_num(c)];

    cout << endl << "rack: " << rack << " = ";
    for (int i = 0; i < alphabet_len; ++i)
      cout << rack_count[i];
    cout << endl;

    /* for (int row = 0; row < board_size; ++row) { */
    /*   for (int col = 0; col < board_size; ++col) { */
    /*     cout << " " << board_hori_mask[row][col] << " "; */
    /*   } */
    /*   cout << endl; */
    /* } */
  }

  list<tuple<int, int, bool, string, int>> get_valid_words() {
    /**
     * Returns list of valid words, in format:
     * (start x, start y, left/right, word, score)
     */

      // TODO: do this for vertical too
      return get_words(board_hori_mask);
  }
};

namespace py = pybind11;

PYBIND11_MODULE(boardsearch, m) {
  m.doc() = "Effecient wordfinding algorithm for SCRABBLE in C++";

  py::class_<BoardSearch>(m, "BoardSearch")
      .def(py::init<board_t, string, DAFSA &>())
      .def("get_valid_words", &BoardSearch::get_valid_words);
}
