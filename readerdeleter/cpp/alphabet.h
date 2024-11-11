#include <iostream>

const int board_size = 15;

const int alphabet_len = 27;
const char alphabet[] = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ"; 
const char delim = alphabet[0];

static inline int get_char_num(char x) {
    return x - '@';
}
