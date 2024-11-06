# How to make Readers cry

## Speed of generation
- __DONE__ Consider converting DAFSA into a GADDAG
  - https://en.wikipedia.org/wiki/GADDAG
  - I think literally exactly the same, but instead of storing dictionary $D$, you store $D' = \{ REV(x)+y | xy \in D\}$
    - Actually, I think that for my purposes, $D' = \{ y+REV(x) | xy \in D\}$ will be better (so you can check suffix first? Actually idk)
  - Since scrabble words are ~5 characters, will increase size of DAFSA by a factor of 5 loosely
- __TODO__ speed up GADDAG generation (takes time in the minutes right now)
- __TODO__ Maybe parallelize parts of this?
- check [here](https://raw.githubusercontent.com/quackle/quackle/refs/heads/master/data/raw_lexica/ods5.raw) for wordlist?
- __TODO__ Turns out that there are a bunch of unplayable words since e.g. there only exists 1xZ and 2xBLANK in the bag, so cull those first before making GADDAG.

## Scoring
- __TODO__ scoring

## Possible routes

I was looking at [this article](https://medium.com/@14domino/scrabble-is-nowhere-close-to-a-solved-game-6628ec9f5ab0)
and had some thoughts.

### Static Evaluation
- For heuristic, I feel like a neural net or svm makes sense?
  - probably want specific data on rack
  - perhaps some info on board?
    - the # vowels/consonants?
    - positioning?
- Superleaves from quackle?
  - I downloaded them but gonna have to decode
  - look at [this](https://github.com/quackle/quackle/blob/master/encodeleaves/encodeleaves.cpp)
- IMPORTANT: bingos are huge, and only 2 blanks per game, so v. important to make sure blanks are played well.
- I think it makes a lot of sense to use a [statistical prediction of the opponent's hand](https://www.researchgate.net/profile/Eyal-Amir/publication/220815435_Opponent_Modeling_in_Scrabble/links/56249b3308ae93a5c92cbdb1/Opponent-Modeling-in-Scrabble.pdf)
  - this should make monte carlo much more accurate
  - improve training significantly?
    
### Tree Search
- Limited ply Monte-Carlo I think will be extremely useful
  - Search highest options (15 or so) according to heuristic
  - Go to depth (apparently 2-3 might be enough? I'm for sure doing more during training though)
  - Article above's [implementation](https://domino14.github.io/macondo/howitworks.html) seems to take a weighted sum of points scored and Monte-Carlo results---but I'm not sure that this makes sense. Shouldn't Monte-Carlo necessarily take into account points scored this turn?
  - Gonna have to parallelize this for sure


## Endgame
- Deterministic once bag is empty
  - use minimax+alpha/beta pruning
  - B* apparently works too?
- If we can get this a bit faster, can fully explore and play perfectly (on average) even slightly before bag is empty.
  - Maybe a more advanced search algo like dfs w/ iterative deepening or fixed-distance minimax?
