# CFGParser - LFA Project
This Python module provides a practical implementation of context-free grammars (CFGs), with utilities for generating valid strings, checking membership, and tracing derivations for specific languages.
# 🎯 CFG Definition
Create a programmatic representation of the following context-free grammar: ``` S → aSb | ε ```

```
self.non_terminals = ["S"]            # list of non-terminal symbols
self.terminals = ["a", "b"]           # list of terminal symbols
self.start_symbol = "S"              # start symbol
self.grammar = {                     # dictionary of production rules
    "S": ["aSb", ""]                 # "aSb" for recursive case, "" for epsilon
}
```

# 🧪String Generator
The generator randomly chooses how to expand the current symbol. It continues expanding recursively until it hits the empty production or exceeds the length limit.
Sample logic:
```
prod = random.choice(self.grammar['S'])  # "aSb" or ""
if prod == "":
    return current_string  # ε
left = self.generate_string('a', ...)
middle = self.generate_string('S', ...)
right = self.generate_string('b', ...)
```
Calling:
```
CFG_ab().generate_multiple_strings(5)
```
...might output:
```
ab
aabb
aaabbb
ε
```
# 🔄 Derivation Tracer
We can trace how a string was derived using leftmost derivations:
```
S → aSb → aaSbb → aaaSbbb → aaabbb
```
This is done by replacing the leftmost S in each step using the grammar rules until the target string is reached.

# ✅ Membership Test
The function checks whether a string is in the language by:
- Verifying equal numbers of a and b
- Ensuring they are correctly ordered (all a's before all b's)

The implementation is recursive:
```
def check_membership(self, s):
    if s == "":
        return True
    if s[0] == 'a' and s[-1] == 'b':
        return self.check_membership(s[1:-1])
    return False
```

# ⚠ Bonus Extension: Attempting L = { aⁿbⁿcⁿ | n ≥ 1 }
❗ Why this is not Context-Free
This language is not context-free, which can be proven using the pumping lemma for CFGs. It requires matching three separate counts — something CFGs can't handle naturally.

⚙ Simulated Grammar
Even so, we simulate an approximation using:

```
S → aSbSc | a | b | c
```
Implemented as:

```
self.non_terminals = ["S"]
self.terminals = ["a", "b", "c"]
self.grammar = {
    "S": [["a", "S", "b", "S", "c"], ["a"], ["b"], ["c"]]
}
```
This does not guarantee correctness, but may generate strings like:

```
abc, aabbcc, aaabbbccc
```
# 🧾 Recognizer
To detect if a string is in { aⁿbⁿcⁿ | n ≥ 1 }, the checker counts the number of a, b, and c, ensuring order and equal counts:

```
def check_membership(self, s):
    count_a = len(list(itertools.takewhile(lambda x: x == 'a', s)))
    count_b = len(list(itertools.takewhile(lambda x: x == 'b', s[count_a:])))
    count_c = len(s) - count_a - count_b
    return count_a == count_b == count_c and count_a > 0
```
# ▶ How to Run
Requirements: Python 3

Execute the program with:

```
python3 main.py
```
Output includes:

- Grammar details

- A list of generated strings

- Derivation steps

- Membership checks








