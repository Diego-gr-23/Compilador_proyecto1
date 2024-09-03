import re
from token_definitions import KEYWORDS, OPERATORS, SYMBOLS, NUMERIC_PATTERN, IDENTIFIER_PATTERN

class Lexer:
    def __init__(self, content):
        self.content = content
        self.tokens = []
        self.errors = []

    def analyze(self):
        lines = self.content.splitlines()
        for line_number, line in enumerate(lines, start=1):
            self.analyze_line(line, line_number)

    def analyze_line(self, line, line_number):
        words = line.split()
        for word in words:
            token_type = self.identify_token(word)
            if token_type:
                self.tokens.append((word, token_type))
            else:
                self.errors.append((line_number, word))

    def identify_token(self, word):
        if word in KEYWORDS:
            return KEYWORDS[word]
        elif word in OPERATORS:
            return OPERATORS[word]
        elif word in SYMBOLS:
            return SYMBOLS[word]
        elif re.fullmatch(NUMERIC_PATTERN, word):
            return "Numero"
        elif re.fullmatch(IDENTIFIER_PATTERN, word):
            return "Identificador"
        return None

    def get_tokens(self):
        return self.tokens

    def get_errors(self):
        return self.errors
