from .build.dafsa import DAFSA
from .build.boardsearch import BoardSearch

from itertools import combinations

# TODO: move this to a better location
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ._"

class Board:
    def __init__(self, gaddag: DAFSA):
        self.size = 15
        self.gaddag = gaddag
        self.letters = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.blanks = []

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
        print("permuting blanks for", word, character)

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
            print("permuting necessary blanks")
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
            print("words looks like", words)

            # distribute excess blanks
            print("distributing excess blanks")
            new_words = set()
            for w in words:
                new_words.update(self.permute_spare_blank(w, spare_blanks))
                print("words from", w, "looks like", self.permute_spare_blank(w, spare_blanks))

            out.extend([(direction, row, col, word, new_word) for new_word in new_words])

        return out


    def get_plays(self, rack: str) -> list[tuple[int, int, int, str, str]]:
        """
        Get the set of all possibles plays, in the form:
        (direction, row, column, literal word, word with blanks explicit)
        """
        # TODO: score words
        board_data = [tuple(row) for row in self.letters]
        board = BoardSearch(board_data, rack, self.gaddag)
        valid_word_plays = list(set(board.get_valid_words()))
        return self.get_blank_positions(rack, valid_word_plays)
