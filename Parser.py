class ParseTreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse_sentence(self):
        if self.current >= len(self.tokens):
            raise ValueError("Unexpected end of input. The logical statement does not make sense.")

        left = self.parse_term()

        while self.current < len(self.tokens):
            if self.tokens[self.current] in {"AND", "OR", "IMPLIES", "EQUIVALENT"}:
                connective = self.tokens[self.current]
                self.current += 1
                if self.current >= len(self.tokens):
                    raise ValueError(f"Logical operator '{connective}' is missing a second operand.")
                right = self.parse_term()
                left = ParseTreeNode(connective, left, right)
            elif self.tokens[self.current] == ")":
                # Closing parenthesis should terminate this subexpression
                return left
            else:
                # Any other unexpected token is invalid
                raise ValueError(f"Unexpected token: {self.tokens[self.current]}")

        return left

    def parse_term(self):
        if self.current >= len(self.tokens):
            raise ValueError("Unexpected end of input. The logical statement does not make sense.")

        token = self.tokens[self.current]

        if token in {"TRUE", "FALSE", "P", "Q", "S"}:
            self.current += 1
            # Ensure valid tokens follow variables/constants
            if self.current < len(self.tokens) and self.tokens[self.current] not in {"AND", "OR", "IMPLIES", "EQUIVALENT", ")"}:
                raise ValueError(f"Unexpected token after '{token}': {self.tokens[self.current]}")
            return ParseTreeNode(token)

        elif token == "NOT":
            self.current += 1
            if self.current >= len(self.tokens):
                raise ValueError("Logical operator 'NOT' is missing an operand.")
            return ParseTreeNode("NOT", left=self.parse_term())

        elif token == "(":
            self.current += 1
            subtree = self.parse_sentence()
            if self.current >= len(self.tokens) or self.tokens[self.current] != ")":
                raise ValueError("Mismatched parentheses: Expected ')'.")
            self.current += 1  # Consume the closing parenthesis
            return subtree

        elif token == ")":
            raise ValueError("Unmatched closing parenthesis ')'.")
        
        elif token in {"AND", "OR", "IMPLIES", "EQUIVALENT"}:
            raise ValueError(f"Logical operator '{token}' is missing a left operand.")
        
        else:
            raise ValueError(f"Unexpected token: {token}")
