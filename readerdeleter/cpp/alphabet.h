#include <iostream>

const int alphabet_len = 26;
const char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const int board_size = 15;

const int alphabet_plus_len = alphabet_len + 1;
const char alphabet_plus[] = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ"; 

static inline int get_char_num(char x) {
    return x - 'A';
}


static inline int get_char_plus_num(char x) {
    return x - '@';
}
