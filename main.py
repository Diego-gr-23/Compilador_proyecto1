import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador Léxico")
        self.setGeometry(300, 300, 600, 400)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        self.analyze_button = QPushButton("Analizar", self)
        self.analyze_button.clicked.connect(self.analyze_file)
        
        self.open_button = QPushButton("Abrir Archivo", self)
        self.open_button.clicked.connect(self.open_file)
        
        self.result_label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        try:
            file_dialog = QFileDialog(self)
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            file_dialog.setNameFilter("Text Files (*.txt)")
            
            if file_dialog.exec():
                file_name = file_dialog.selectedFiles()[0]
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al abrir el archivo: {str(e)}")
            self.text_edit.clear()

    def analyze_file(self):
        try:
            content = self.text_edit.toPlainText()
            if not content:
                QMessageBox.warning(self, "Advertencia", "Primero debes cargar un archivo.")
                return

            # Aquí iría la lógica del lexer (esto se mantendría igual)

            # Temporarily simulating result text (since Lexer isn't implemented in this snippet)
            self.result_label.setText("Análisis completado con éxito.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al analizar el archivo: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
