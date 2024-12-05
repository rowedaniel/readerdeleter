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
SCORES = {
        "A": 1,
        "B": 3,
        "C": 3,
        "D": 2,
        "E": 1,
        "F": 4,
        "G": 2,
        "H": 4,
        "I": 1,
        "J": 8,
        "K": 5,
        "L": 1,
        "M": 3,
        "N": 1,
        "O": 1,
        "P": 3,
        "Q": 10,
        "R": 1,
        "S": 1,
        "T": 1,
        "U": 1,
        "V": 4,
        "W": 4,
        "X": 8,
        "Y": 4,
        "Z": 10,
        "_": 0,
        }


class Board:
    def __init__(self, gaddag: DAFSA, letters: list[list[str]]|None = None):
        self.size = 15
        self.gaddag = gaddag
        # use capital for letters, lowercase for blanks of that letter
        if letters is None:
            self.letters = [[" " for _ in range(self.size)] for _ in range(self.size)]
        else:
            self.letters = letters
        self.blank = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.searcher = BoardSearch([tuple(row) for row in self.letters], self.gaddag)

        # lowercase = letter, UPPERCASE = word
        # t = triple, d = double
        self.score_multipliers = [
                "T  d   T   d  T",
                " D   t   t   D ",
                "  D   d d   D  ",
                "d  D   d   D  d",
                "    D     D    ",
                " t   t   t   t ",
                "  d   d d   d  ",
                "t  d   *   d  t",
                "  d   d d   d  ",
                " t   t   t   t ",
                "    D     D    ",
                "d  D   d   D  d",
                "  D   d d   D  ",
                " D   t   t   D ",
                "T  d   T   d  T",
                ]

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
            valid_word_plays: list[tuple[int, int, int, str]]
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


    def get_plays(self, rack: str) -> list[tuple[int, int, int, str, str]]:
        """
        Get the set of all possibles plays, in the form:
        (direction, row, column, literal word, word with blanks explicit)
        """
        # TODO: score words
        valid_word_plays = list(set(self.searcher.get_valid_words(rack)))
        return self.get_blank_positions(rack, valid_word_plays)

    def auxiliary_score(self, row: int, col: int, char: str, direction: bool):
        """
        score the words incidental to a play. For instance, consider the following board:

        t
        e
        s
        t
        SUPPER

        where "SUPPER" is new.
        Then we must not only count the score of SUPPER but also that of the new word "tests".
        """
        score = 0

        # going one direction
        cur_r = row + direction
        cur_c = col + (not direction)
        while cur_r < self.size and cur_c < self.size and self.letters[cur_r][cur_c] != " ":
            if not self.blank[cur_r][cur_c]:
                score += SCORES[self.letters[cur_r][cur_c]]
            cur_r += direction
            cur_c += (not direction)

        # going the other direction
        cur_r = row - direction
        cur_c = col - (not direction)
        while cur_r >= 0 and cur_c >= 0 and self.letters[cur_r][cur_c] != " ":
            if not self.blank[cur_r][cur_c]:
                score += SCORES[self.letters[cur_r][cur_c]]
            cur_r -= direction
            cur_c -= (not direction)

        word_multiplier = 1
        if score > 0:
            # a word did exist, so add this letter's score again
            multiplier = 1
            if self.score_multipliers[row][col] == "d":
                multiplier = 2
            elif self.score_multipliers[row][col] == "t": 
                multiplier = 3
            elif self.score_multipliers[row][col] == "D": 
                word_multiplier *= 2
            elif self.score_multipliers[row][col] == "T": 
                word_multiplier *= 3
            score += SCORES[char] * multiplier
        return score * word_multiplier
        

    def score_play(self, play: tuple[int, int, int, str, str]) -> int:
        """
        Score a play = (direction, row, col, word, word(with blanks) )
        """
        score = 0
        word_multiplier = 1
        word = play[4]
        aux_score = 0
        for i,char in enumerate(word):
            row = play[1] + i * (play[0])
            col = play[2] + i * (not play[0])
            if char == '.':
                # preexisting letter
                if not self.blank[row][col]: # blanks score 0
                    score += SCORES[self.letters[row][col]]
            else:
                multiplier = 1
                if self.score_multipliers[row][col] == "d":
                    multiplier = 2
                elif self.score_multipliers[row][col] == "t": 
                    multiplier = 3
                elif self.score_multipliers[row][col] == "D": 
                    word_multiplier *= 2
                elif self.score_multipliers[row][col] == "T": 
                    word_multiplier *= 3
                score += SCORES[char] * multiplier
                aux_score += self.auxiliary_score(row, col, char, not play[0])
        return score * word_multiplier + aux_score

    def play(self, play: tuple[int, int, int, str, str]) -> None:
        column_word, row, col, word, word_blanks = play
        for i,char in enumerate(word):
            cur_r = row + i * (column_word)
            cur_c = col + i * (not column_word)
            if char != ".":
                self.letters[cur_r][cur_c] = char
                if word_blanks[i] == '_':
                    self.blank[cur_r][cur_c] = True




    def __str__(self) -> str:
        out = '    ' + ''.join(str(i)[-1] for i in range(15))
        out += '\n'
        for i, row in enumerate(self.letters):
            out += f'{i:<3} '
            for j, c in enumerate(row):
                if c == ' ':
                    out += self.score_multipliers[i][j]
                    # out += ' '
                else:
                    out += c
            out += "\n"
        return out
