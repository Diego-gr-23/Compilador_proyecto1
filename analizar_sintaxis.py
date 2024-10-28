class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.errors = []

    def analyze(self):
        i = 0
        while i < len(self.tokens):
            token, token_type = self.tokens[i]

            # Verificación de punto y coma en declaraciones
            if token_type == "Identificador" and i + 1 < len(self.tokens) and self.tokens[i + 1][0] == "=":
                if i + 3 >= len(self.tokens) or self.tokens[i + 3][0] != ";":
                    self.errors.append(f"Error: Falta ';' al final de la declaración cerca de '{token}'")
            
            # Verificación de condicionales y bucles con paréntesis
            elif token in ["si", "mientras"]:
                if i + 1 >= len(self.tokens) or self.tokens[i + 1][0] != "(":
                    self.errors.append(f"Error: Falta '(' después de '{token}'")
                if i + 3 >= len(self.tokens) or self.tokens[i + 3][0] != ")":
                    self.errors.append(f"Error: Falta ')' en la condición de '{token}'")

            i += 1

    def get_errors(self):
        return self.errors
