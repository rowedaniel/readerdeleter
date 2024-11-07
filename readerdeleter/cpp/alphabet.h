const int alphabet_len = 26;
const char alphabet[] = "abcdefghijklmnopqrstuvwxyz";
const int board_size = 15;

const int alphabet_plus_len = alphabet_len + 1;
const char alphabet_plus[] = "+abcdefghijklmnopqrstuvwxyz"; 

static inline int get_char_num(char x) {
    return x - 'a';
}


static inline int get_char_plus_num(char x) {
    if(x == '+')
        return 0;
    return x - 'a' + 1;
}
