class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []

    def analyze(self):
        for i, (token, token_type) in enumerate(self.tokens):
            # Implementar reglas sintácticas, por ejemplo, declaración de variables y funciones
            pass

    def get_errors(self):
        return self.errors
