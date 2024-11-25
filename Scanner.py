import re

class Scanner:
    def __init__(self, input_string):
        self.input_string = input_string
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        token_regex = r"(TRUE|FALSE|P|Q|S|NOT|AND|OR|IMPLIES|EQUIVALENT|\(|\))"
        self.tokens = re.findall(token_regex, self.input_string)
        cleaned_input = "".join(self.tokens)
        if cleaned_input != self.input_string.replace(" ", ""):
            invalid_index = self._find_invalid_position(cleaned_input)
            raise ValueError(f"There is a typographical error at position {invalid_index}. Invalid token: '{self.input_string[invalid_index]}'")

    def _find_invalid_position(self, cleaned_input):
        for i, (original, valid) in enumerate(zip(self.input_string.replace(" ", ""), cleaned_input)):
            if original != valid:
                return i
        return len(cleaned_input)

    def get_tokens(self):
        return self.tokens
