"""
Byte Pair Encoding (BPE) tokenizer built from scratch in pure Python,
with special support for mathematical notation and LaTeX commands.
"""

import json
import re
from collections import Counter, defaultdict


class MathBPETokenizer:
    """
    A BPE tokenizer designed for mathematical text and LaTeX expressions.

    The tokenizer preserves LaTeX commands as atomic tokens (they are never
    split during encoding) and handles mathematical operators, numbers, and
    natural-language words.
    """

    # ------------------------------------------------------------------
    # Special tokens
    # ------------------------------------------------------------------
    SPECIAL_TOKENS = {
        "<PAD>": 0,
        "<UNK>": 1,
        "<BOS>": 2,
        "<EOS>": 3,
        "<SEP>": 4,
    }

    # ------------------------------------------------------------------
    # Pre-defined LaTeX tokens (never split)
    # ------------------------------------------------------------------
    LATEX_TOKENS = [
        r"\frac", r"\int", r"\lim", r"\sqrt", r"\sum", r"\prod",
        r"\infty", r"\pi", r"\alpha", r"\beta", r"\gamma", r"\delta",
        r"\theta", r"\lambda", r"\sigma", r"\omega", r"\partial",
        r"\nabla", r"\rightarrow", r"\leftarrow", r"\Rightarrow",
        r"\leq", r"\geq", r"\neq", r"\approx", r"\cdot", r"\times",
        r"\div", r"\pm", r"\mp", r"\in", r"\notin", r"\subset",
        r"\cup", r"\cap", r"\forall", r"\exists",
        r"\mathbb{R}", r"\mathbb{N}", r"\mathbb{Z}", r"\mathbb{Q}",
        r"\mathbb{C}",
        r"\binom", r"\log", r"\ln", r"\sin", r"\cos", r"\tan",
        r"\arcsin", r"\arccos", r"\arctan",
    ]

    # ------------------------------------------------------------------
    # Math operator tokens
    # ------------------------------------------------------------------
    MATH_OPERATORS = [
        "+", "-", "*", "/", "=", "<", ">",
        "(", ")", "[", "]", "{", "}", "^", "_", "|",
    ]

    # ------------------------------------------------------------------
    # Regex used by pre_tokenize  (compiled once at class level)
    # ------------------------------------------------------------------
    # Order matters:
    #   1. LaTeX commands with braces  e.g. \mathbb{R}
    #   2. LaTeX commands              e.g. \frac
    #   3. Numbers (incl. decimals)    e.g. 3.14
    #   4. Words                       e.g. hello
    #   5. Operators / single chars    e.g. +
    #   6. Whitespace runs
    _PRE_TOKENIZE_RE = re.compile(
        r"(\\[a-zA-Z]+\{[^}]*\})"   # \command{...}
        r"|(\\[a-zA-Z]+)"            # \command
        r"|(\d+(?:\.\d+)?)"          # numbers
        r"|([a-zA-ZăâîșțĂÂÎȘȚ]+)"  # words (incl. Romanian diacritics)
        r"|([+\-*/=<>()\[\]{}^_|])"  # operators
        r"|(\s+)"                    # whitespace
        r"|(.)"                      # any other single character
    )

    # ================================================================
    # Construction
    # ================================================================
    def __init__(self, vocab_size: int = 8192) -> None:
        self.target_vocab_size = vocab_size

        # Populated during training (or loading)
        self.vocab: dict[str, int] = {}          # token -> id
        self.inverse_vocab: dict[int, str] = {}  # id -> token
        self.merges: list[tuple[str, str]] = []   # ordered merge rules

    # ================================================================
    # Pre-tokenisation
    # ================================================================
    def pre_tokenize(self, text: str) -> list[str]:
        """Split *text* into a list of preliminary tokens.

        LaTeX commands, numbers, words, operators, and whitespace are each
        kept as individual tokens.  The output list contains no empty strings.
        """
        tokens: list[str] = []
        for match in self._PRE_TOKENIZE_RE.finditer(text):
            token = match.group()
            if token:
                tokens.append(token)
        return tokens

    # ================================================================
    # Training
    # ================================================================
    def train(self, texts: list[str], verbose: bool = True) -> None:
        """Train the BPE tokenizer on a corpus of *texts*.

        Steps
        -----
        1. Pre-tokenize every text in the corpus.
        2. Build the initial vocabulary from individual characters plus all
           special, LaTeX and operator tokens.
        3. Represent each pre-token as a tuple of characters (but keep
           protected tokens intact).
        4. Iteratively find the most-frequent adjacent pair, merge it,
           and add the merged token to the vocabulary until the target
           vocabulary size is reached.
        """
        # -- 1. Pre-tokenize ------------------------------------------------
        if verbose:
            print("[BPE] Pre-tokenizing corpus ...")

        all_pre_tokens: list[str] = []
        for text in texts:
            all_pre_tokens.extend(self.pre_tokenize(text))

        # -- 2. Determine which pre-tokens are "protected" ------------------
        protected: set[str] = set(self.SPECIAL_TOKENS.keys())
        protected.update(self.LATEX_TOKENS)
        protected.update(self.MATH_OPERATORS)

        # -- 3. Build word frequency list ------------------------------------
        #    Each word is stored as a *tuple* of its constituent symbols.
        #    Protected tokens stay as single-element tuples.
        word_freq: Counter[tuple[str, ...]] = Counter()
        for pt in all_pre_tokens:
            if pt in protected:
                word_freq[(pt,)] += 1
            else:
                word_freq[tuple(pt)] += 1

        # -- 4. Build initial vocab ------------------------------------------
        self.vocab = {}
        idx = 0
        # Special tokens first
        for tok, tid in self.SPECIAL_TOKENS.items():
            self.vocab[tok] = tid
            idx = max(idx, tid + 1)

        # LaTeX tokens
        for tok in self.LATEX_TOKENS:
            if tok not in self.vocab:
                self.vocab[tok] = idx
                idx += 1

        # Operator tokens
        for tok in self.MATH_OPERATORS:
            if tok not in self.vocab:
                self.vocab[tok] = idx
                idx += 1

        # Individual characters found in the corpus
        char_set: set[str] = set()
        for word_tuple in word_freq:
            for symbol in word_tuple:
                char_set.add(symbol)
        for ch in sorted(char_set):
            if ch not in self.vocab:
                self.vocab[ch] = idx
                idx += 1

        if verbose:
            print(f"[BPE] Initial vocab size: {len(self.vocab)}")
            print(f"[BPE] Target vocab size : {self.target_vocab_size}")

        # -- 5. Iterative BPE merges ----------------------------------------
        self.merges = []
        num_merges = self.target_vocab_size - len(self.vocab)
        if num_merges <= 0:
            if verbose:
                print("[BPE] Vocab already at target size; no merges needed.")
        else:
            for i in range(num_merges):
                # Count adjacent pairs
                pair_counts: Counter[tuple[str, str]] = Counter()
                for word_tuple, freq in word_freq.items():
                    if len(word_tuple) < 2:
                        continue
                    for j in range(len(word_tuple) - 1):
                        pair_counts[(word_tuple[j], word_tuple[j + 1])] += freq

                if not pair_counts:
                    if verbose:
                        print(f"[BPE] No more pairs to merge at step {i}.")
                    break

                best_pair = pair_counts.most_common(1)[0][0]
                merged_token = best_pair[0] + best_pair[1]

                # Record the merge
                self.merges.append(best_pair)
                if merged_token not in self.vocab:
                    self.vocab[merged_token] = idx
                    idx += 1

                # Apply the merge to every word in the frequency table
                new_word_freq: Counter[tuple[str, ...]] = Counter()
                for word_tuple, freq in word_freq.items():
                    new_word = self._apply_merge(word_tuple, best_pair)
                    new_word_freq[new_word] += freq
                word_freq = new_word_freq

                if verbose and (i + 1) % 500 == 0:
                    print(
                        f"[BPE] Merge {i + 1}/{num_merges}: "
                        f"'{best_pair[0]}' + '{best_pair[1]}' -> '{merged_token}'"
                    )

        # -- 6. Build inverse vocab ------------------------------------------
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}

        if verbose:
            print(f"[BPE] Training complete. Final vocab size: {len(self.vocab)}")

    # ================================================================
    # Encoding
    # ================================================================
    def encode(self, text: str) -> list[int]:
        """Encode *text* into a list of integer token IDs."""
        pre_tokens = self.pre_tokenize(text)

        protected: set[str] = set(self.SPECIAL_TOKENS.keys())
        protected.update(self.LATEX_TOKENS)
        protected.update(self.MATH_OPERATORS)

        ids: list[int] = []
        for pt in pre_tokens:
            if pt in protected:
                ids.append(self.vocab.get(pt, self.SPECIAL_TOKENS["<UNK>"]))
            else:
                # Split into characters, then apply merges in order
                symbols: list[str] = list(pt)
                for left, right in self.merges:
                    symbols = self._apply_merge_list(symbols, left, right)
                for sym in symbols:
                    ids.append(self.vocab.get(sym, self.SPECIAL_TOKENS["<UNK>"]))
        return ids

    # ================================================================
    # Decoding
    # ================================================================
    def decode(self, ids: list[int]) -> str:
        """Decode a list of integer token IDs back into a string."""
        tokens: list[str] = []
        for tid in ids:
            tok = self.inverse_vocab.get(tid, "<UNK>")
            tokens.append(tok)
        return "".join(tokens)

    # ================================================================
    # Save / Load
    # ================================================================
    def save(self, path: str) -> None:
        """Persist vocabulary and merge rules to a JSON file."""
        data = {
            "vocab": self.vocab,
            "merges": [list(pair) for pair in self.merges],
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    def load(self, path: str) -> None:
        """Load vocabulary and merge rules from a JSON file."""
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self.vocab = data["vocab"]
        self.merges = [tuple(pair) for pair in data["merges"]]
        self.inverse_vocab = {v: k for k, v in self.vocab.items()}

    # ================================================================
    # Dunder helpers
    # ================================================================
    def __len__(self) -> int:
        """Return the current vocabulary size."""
        return len(self.vocab)

    # ================================================================
    # Private helpers
    # ================================================================
    @staticmethod
    def _apply_merge(
        word: tuple[str, ...], pair: tuple[str, str]
    ) -> tuple[str, ...]:
        """Return a new word-tuple with every occurrence of *pair* merged."""
        new_word: list[str] = []
        i = 0
        while i < len(word):
            if (
                i < len(word) - 1
                and word[i] == pair[0]
                and word[i + 1] == pair[1]
            ):
                new_word.append(pair[0] + pair[1])
                i += 2
            else:
                new_word.append(word[i])
                i += 1
        return tuple(new_word)

    @staticmethod
    def _apply_merge_list(
        symbols: list[str], left: str, right: str
    ) -> list[str]:
        """Apply a single merge rule (*left* + *right*) to a symbol list."""
        merged: list[str] = []
        i = 0
        while i < len(symbols):
            if (
                i < len(symbols) - 1
                and symbols[i] == left
                and symbols[i + 1] == right
            ):
                merged.append(left + right)
                i += 2
            else:
                merged.append(symbols[i])
                i += 1
        return merged
