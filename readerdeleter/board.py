from .build.dafsa import DAFSA
from .build.boardsearch import BoardSearch

from itertools import combinations

# TODO:
# 1. handle start move
# 2. Figure out features
#       thinking from https://arxiv.org/pdf/1712.01815
#       T x 27 planes--one for each letter
#       where T is history depth (probably 2?)
#       Also 27 several-hot encoding for rack?
#       How bad is this gonna be to train? Might have to reduce
#           something like 27*2*17*17 + 27*12 = ~16,000
#           so I'd want something on the order of 1 million games?
#           very doable, but will that work well?
# 3. Peter thinks Monte Carlo is simply not the way
#       Actually it might be the way--but start with actual Monte Carlo, not just random
#       playout


# TODO: move this to a better location
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ._"

class Board:
    def __init__(self, gaddag: DAFSA, letters: list[list[str]]|None = None):
        self.size = 15
        self.gaddag = gaddag
        # use capital for letters, lowercase for blanks of that letter
        if letters is None:
            self.letters = [[" " for _ in range(self.size)] for _ in range(self.size)]
        else:
            self.letters = letters

        if all(all(space == ' ' for space in row) for row in self.letters):
            self.is_blank = True
        else:
            self.is_blank = False

        self.blank = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.searcher = BoardSearch([tuple(row) for row in self.letters], self.gaddag)
        self.plays = None

    def permute_blank_character(self, word: str, character: str, blanks: int) -> set[str]:
        """
        generate all permutations of 'word' with 'character' replaced with a blank
        """

        out = set()
        chunks = word.split(character)
        chunk_indices = range(1, len(chunks))
        for blank_indices in combinations(chunk_indices, blanks):
            word = chunks[0]
            for j in range(1, len(chunks)):
                if j in blank_indices:
                    word += '_' + chunks[j]
                else:
                    word += character + chunks[j]
            out.add(word)
        return out

    def permute_spare_blank(self, word: str, blanks: int, start: int = 0) -> set[str]:
        """
        generate all permutations of 'word' with characters replaced with blanks.
        (Only newly-placed non-blank characters are replaced)

        If start is specified, only replace characters starting at that index.
        """

        if blanks == 0:
            return set([word])
        out = set()
        for i in range(start, len(word)):
            if word[i] in ('.', '_'):
                continue
            new_word = word[:i] + '_' + word[i+1:]
            out.update(self.permute_spare_blank(new_word, blanks-1, i+1))
        out.update(self.permute_spare_blank(word, blanks-1, 0))
        return out


    def get_blank_positions(
            self,
            rack: str,
            valid_word_plays: set[tuple[int, int, int, str]]
                            ) -> list[tuple[int, int, int, str, str]]:
        if '_' not in rack:
            return [
                (direction, row, col, word, word)
                for (direction, row, col, word) in valid_word_plays
                ]

        out = []
        rack_counts = {c: rack.count(c) for c in ALPHABET}
        for (direction, row, col, word) in valid_word_plays:
            words = set([word])
            word_counts = {c: word.count(c) for c in set(word)}

            # populate every permutation of necessary blanks
            spare_blanks = rack_counts['_']
            for c, word_count in word_counts.items():
                if c == '.':
                    # already used tile
                    continue
                diff = word_count - rack_counts[c]
                if diff > 0:
                    spare_blanks -= diff

                    # populate with every permutation of blanks for this character
                    new_words = set()
                    for w in words:
                        new_words.update(self.permute_blank_character(w, c, diff))
                    words = new_words

            # distribute excess blanks
            new_words = set()
            for w in words:
                new_words.update(self.permute_spare_blank(w, spare_blanks))

            out.extend([(direction, row, col, word, new_word) for new_word in new_words])

        return out

    def get_valid_words(self, rack: str) -> set[tuple[int, int, int, str]]:
        valid_word_plays = set(self.searcher.get_valid_words(rack))
        if self.is_blank:
            return set(filter(lambda x: len(x[3]) > 1, valid_word_plays))
        return valid_word_plays



    def get_plays(self, rack: str) -> list[tuple[int, int, int, str, str]]:
        """
        Get the set of all possibles plays, in the form:
        (direction, row, column, literal word, word with blanks explicit)
        """
        return self.get_blank_positions(rack, self.get_valid_words(rack))

    def play(self, play: tuple[int, int, int, str, str]) -> None:
        column_word, row, col, word, word_blanks = play
        for i,char in enumerate(word):
            cur_r = row + i * (column_word)
            cur_c = col + i * (not column_word)
            if char != ".":
                self.letters[cur_r][cur_c] = char
                if word_blanks[i] == '_':
                    self.blank[cur_r][cur_c] = True



    def update_tile(self, row: int, col: int, letter: str, is_blank: bool) -> None:
        if is_blank:
            self.blank[row][col] = True
        self.searcher.update_cross_check(row, col, letter)

    def __str__(self) -> str:
        out = '    ' + ''.join(str(i)[-1] for i in range(15))
        out += '\n'
        for i, row in enumerate(self.letters):
            out += f'{i:<3} '
            for c in row:
                if c == ' ':
                    out += ' '
                else:
                    out += c
            out += "\n"
        return out
