import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout,
                             QWidget, QFileDialog, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtGui import QFont
from lexer import Lexer

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

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["TOKEN", "TIPO", "CANTIDAD"])

        font = QFont()
        font.setBold(True)
        self.table_widget.horizontalHeader().setFont(font)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.analyze_button)
        layout.addWidget(self.table_widget)

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

            lexer = Lexer(content)
            lexer.analyze()
            tokens = lexer.get_tokens()

            # Contar la cantidad de cada token
            token_counts = {}
            for token, tipo in tokens:
                if token in token_counts:
                    token_counts[token]['count'] += 1
                else:
                    token_counts[token] = {'type': tipo, 'count': 1}

            self.table_widget.setRowCount(len(token_counts))

            # Llenar la tabla con los tokens y sus tipos y cantidades
            for row, (token, data) in enumerate(token_counts.items()):
                self.table_widget.setItem(row, 0, QTableWidgetItem(token))
                self.table_widget.setItem(row, 1, QTableWidgetItem(data['type']))
                self.table_widget.setItem(row, 2, QTableWidgetItem(str(data['count'])))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al analizar el archivo: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

