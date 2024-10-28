class SemanticAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []

    def analyze(self):
        # Implementar reglas semánticas, por ejemplo, verificar tipos de datos y parámetros
        pass

    def get_errors(self):
        return self.errors
