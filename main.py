import random
class CFG_ab:
  def __init__(self):
    self.non_terminals = ["S"]
    self.terminals = ["a", "b"]
    self.start_symbol = "S"
    self.grammar = {
      "S": ["aSb", ""]
    }
    
  def view(self):
    print("Context-Free Grammar:")
    print("Model: L = { aⁿbⁿ | n ≥ 0 }")
    print(f"Start Symbol: {self.start_symbol}")
    print("Production Rules:")
    for nonterminal, productions in self.grammar.items():
        rules = " | ".join([p if p != "" else "ε" for p in productions])
        print(f"  {nonterminal} → {rules}")  

  def generate_multiple_strings(self, count=10, max_len=10):
    strings = set()
    attempts = 0
    max_attempts = count * 20  # safety limit

    while len(strings) < count and attempts < max_attempts:
        s = self.generate_string(max_len=max_len)
        attempts += 1
        if s is not None and len(s) <= max_len:
            strings.add(s)

    return list(strings)

  def generate_string(self, symbol='S', max_len=10, current_string=''):
    # string exceeds max allowed length so stop it
    if len(current_string) > max_len:
        return None

    # Terminal case
    if symbol in self.terminals:
        return current_string + symbol

    # Only production'S'
    if symbol == 'S':
        prod = random.choice(self.grammar['S'])  # Either ['a', 'S', 'b'] or []
        if prod == "":
            return current_string  # ε-production - empty space

        # expand: aSb left mid and right 
        left = self.generate_string('a', max_len, current_string)
        if left is None: 
            return None

        middle = self.generate_string('S', max_len, left)
        if middle is None:
            return None

        right = self.generate_string('b', max_len, middle)
        return right

    return current_string
  
  def derive(self, target, current='S', steps_so_far=None):
    if steps_so_far is None:
        steps_so_far = [current]

    # Stop if we already matched
    if current == target:
        return steps_so_far

    # Skip paths that are definitely too long
    expanded = current.replace('S', '')
    if len(expanded) > len(target):
        return None

    # No more S to expand
    if 'S' not in current:
        return None

    # Find first occurrence of S (leftmost derivation)
    position = current.find('S')

    # Try replacing it with all available productions
    for option in self.grammar['S']:
        substituted = current[:position] + option + current[position + 1:]
        trail = steps_so_far + [substituted]
        attempt = self.derive(target, substituted, trail)
        if attempt is not None:
            return attempt

    return None

  def show_derivation(self, target):
      steps = self.derive(target)
      if steps:
          print(" → ".join(steps))
      else:
          print(f"No derivation found for: {target}")

  def check_membership(self, string):
      # Checks if a string belongs to L = { aⁿbⁿ | n ≥ 0 }
      # the string must start with 'a' and end with 'b' in order to be valid
      # check recursively if the string can be reduced to ε by removing outer 'a' and 'b'
      if string == "":
          return True  # ε is allowed

      if len(string) < 2:
          return False  # a or b alone is not valid

      if string[0] == 'a' and string[-1] == 'b':
          return self.check_membership(string[1:-1])  # recursively strip outer a/b

      return False  # doesn't match pattern
  
class CFG_abc:
    def __init__(self):
        self.non_terminals = ["S"]
        self.terminals = ["a", "b", "c"]
        self.start_symbol = "S"
        self.grammar = {
            "S": [["a", "S", "b", "S", "c"], ["a"], ["b"], ["c"]]
        }

    def view(self):
        print("CFG for language (approximated):")
        print("S → aSbSc | a | b | c")
        print("CFG may generate strings like 'abc', 'aabbcc', 'aaabbbccc', etc.")
        print("However, it does not guarantee only strings from L = { aⁿbⁿcⁿ | n ≥ 1 }")

    def check_membership(self, s):
        n = len(s)
        if n < 3:
            return False
        i = 0
        while i < n and s[i] == 'a':
            i += 1
        j = i
        while j < n and s[j] == 'b':
            j += 1
        k = j
        while k < n and s[k] == 'c':
            k += 1
        return i > 0 and i == j - i and i == k - j and k == n

    def generate_string(self, symbol='S', max_depth=10, current_depth=0):
      if current_depth > max_depth:
          # fallback: random terminal string to avoid infinite recursion
          return random.choice(self.terminals)

      # pick a random production for the current symbol
      production = random.choice(self.grammar[symbol])

      result = ""
      for sym in production:
          if sym in self.terminals:
              result += sym
          elif sym in self.non_terminals:
              result += self.generate_string(sym, max_depth, current_depth + 1)
      return result

    def generate_strings(self, count=10, max_depth=10):
        generated = set()
        while len(generated) < count:
            s = self.generate_string(max_depth=max_depth)
            generated.add(s)
        
        print("Generated strings are:", ', '.join(generated))
        return list(generated)

  
if __name__ == "__main__":
    cfg = CFG_ab()
    cfg.view()

    generated_strings = cfg.generate_multiple_strings(count=10, max_len=10)
    print("\nGenerated Strings:")
    for s in generated_strings:
        print(s)

    for target_string in generated_strings:
        print(f"\nDerivation for: {target_string}")
        cfg.show_derivation(target_string)

    # Check membership of a string
    test_string = "aabb"
    is_member = cfg.check_membership(test_string)
    print(f"\nIs '{test_string}' in the language? {'Yes' if is_member else 'No'}")


    # Test CFG_abc
    cfg_abc = CFG_abc()
    cfg_abc.view()
    generated_strings_abc = cfg_abc.generate_strings(count=10, max_depth=10)
    print("\nGenerated Strings for CFG_abc:")
    for s in generated_strings_abc:
        print(s)
    for target_string in generated_strings_abc:
        print(f"\nMembership check for: {target_string}")
        is_member_abc = cfg_abc.check_membership(target_string)
        print(f"Is '{target_string}' in the language? {'Yes' if is_member_abc else 'No'}")

