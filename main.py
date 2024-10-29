import sys
import tokenize
import io
import ast
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel
)
from PyQt6.QtCore import Qt

class AnalizadorLexico(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Analizador Léxico")
        self.setGeometry(100, 100, 1200, 800)

        # Cuadro de texto para mostrar el contenido del archivo
        self.textbox = QTextEdit(self)
        self.textbox.setReadOnly(False)

        # Cuadro de texto para mostrar los errores
        self.textbox_errores = QTextEdit(self)
        self.textbox_errores.setReadOnly(True)
        self.textbox_errores.setPlaceholderText("Aquí se mostrarán los errores léxicos, sintácticos y semánticos...")

        # Etiqueta para el área de errores
        self.label_errores = QLabel("Errores Detectados:")
        
        # Tabla para mostrar tokens
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["TOKEN", "TIPO", "CANTIDAD"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(1, 200)
        self.tree.setColumnWidth(2, 100)

        # Botones
        self.button_cargar = QPushButton("Cargar Documento", self)
        self.button_cargar.clicked.connect(self.abrir_archivo)

        self.button_analizar = QPushButton("Analizar Documento", self)
        self.button_analizar.clicked.connect(self.analizar_documento)

        self.button_limpiar = QPushButton("Limpiar", self)
        self.button_limpiar.clicked.connect(self.limpiar)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.button_cargar)
        layout.addWidget(self.button_analizar)
        layout.addWidget(self.button_limpiar)

        # Área de texto y tabla de tokens
        layout.addWidget(QLabel("Contenido del Archivo:"))
        layout.addWidget(self.textbox)
        layout.addWidget(QLabel("Tokens Encontrados:"))
        layout.addWidget(self.tree)

        # Área de errores
        layout.addWidget(self.label_errores)
        layout.addWidget(self.textbox_errores)

        # Configuración del widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def abrir_archivo(self):
        # Función para abrir un archivo y mostrar su contenido en el cuadro de texto
        archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona un archivo de texto", "", "Text Files (*.txt)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as file:
                contenido = file.read()
                self.textbox.setPlainText(contenido)

    def analizar_documento(self):
        # Función para analizar el contenido del cuadro de texto
        contenido = self.textbox.toPlainText().strip()
        tokens_encontrados = []
        errores_lexicos = []
        errores_sintacticos = []
        errores_semanticos = []

        # Verificación léxica
        try:
            token_generador = tokenize.tokenize(io.BytesIO(contenido.encode('utf-8')).readline)
            for token in token_generador:
                if token.type == tokenize.ENCODING:
                    continue
                if token.type in {tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT}:
                    continue

                if token.type == tokenize.NAME:
                    if token.string in {"entero", "decimal", "boleano", "cadena", "si", "sino", "mientras", "hacer",
                                        "verdadero", "falso"}:
                        tipo = "Palabra Reservada"
                    else:
                        tipo = "Identificador"
                elif token.type == tokenize.OP:
                    tipo = "Operador"
                elif token.type == tokenize.NUMBER:
                    tipo = "Número"
                elif token.type == tokenize.STRING:
                    tipo = "Cadena"
                elif token.type == tokenize.COMMENT:
                    tipo = "Comentario"
                else:
                    continue

                tokens_encontrados.append((token.string, tipo))

        except tokenize.TokenError as e:
            errores_lexicos.append(f"Error de tokenización en la línea {e.args[1][0]}: {str(e)}")

        # Verificación sintáctica
        try:
            ast.parse(contenido)
        except SyntaxError as e:
            errores_sintacticos.append(f"Error sintáctico en la línea {e.lineno}: {e.msg}")

        # Verificación semántica si no hay errores sintácticos
        if not errores_sintacticos:
            try:
                exec(contenido)
            except Exception as e:
                if hasattr(e, 'lineno'):
                    errores_semanticos.append(f"Error semántico en la línea {e.lineno}: {str(e)}")
                else:
                    errores_semanticos.append(f"Error semántico: {str(e)}")

            # Comprobar condiciones específicas
            si_condiciones = contenido.count("si")
            hacer_condiciones = contenido.count("hacer")

            if si_condiciones > hacer_condiciones:
                errores_semanticos.append("Condición 'si' no seguida de 'hacer'")

        # Limpiar el TreeWidget y el área de errores
        self.tree.clear()
        self.textbox_errores.clear()

        # Mostrar errores en el área de errores
        if errores_lexicos:
            self.textbox_errores.append("Errores Léxicos:")
            for error in errores_lexicos:
                self.textbox_errores.append(error)

        if errores_sintacticos:
            self.textbox_errores.append("\nErrores Sintácticos:")
            for error in errores_sintacticos:
                self.textbox_errores.append(error)

        if errores_semanticos:
            self.textbox_errores.append("\nErrores Semánticos:")
            for error in errores_semanticos:
                self.textbox_errores.append(error)

        # Mostrar tokens en la tabla si no hay errores
        if not (errores_lexicos or errores_sintacticos or errores_semanticos):
            conteo_tokens = {}
            for token, tipo in tokens_encontrados:
                if tipo not in conteo_tokens:
                    conteo_tokens[tipo] = {}
                if token not in conteo_tokens[tipo]:
                    conteo_tokens[tipo][token] = 0
                conteo_tokens[tipo][token] += 1

            # Insertar datos en la tabla
            for tipo, tokens in conteo_tokens.items():
                for token, cantidad in tokens.items():
                    item = QTreeWidgetItem([token, tipo, str(cantidad)])
                    self.tree.addTopLevelItem(item)

    def limpiar(self):
        # Limpiar el cuadro de texto, el área de errores y la tabla de tokens
        self.textbox.clear()
        self.textbox_errores.clear()
        self.tree.clear()

def main():
    app = QApplication(sys.argv)
    ventana = AnalizadorLexico()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
