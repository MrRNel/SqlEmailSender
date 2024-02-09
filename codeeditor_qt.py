# codeeditor_qt.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

class CodeEditor(QMainWindow):
    def __init__(self, file_name):
        super().__init__()
        self.initUI(file_name)

    def initUI(self, file_name):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Code Editor")

        # Create a QScintilla editor widget
        self.editor = QsciScintilla(self)
        self.editor.setGeometry(0, 0, 800, 550)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create a Python lexer for syntax highlighting
        lexer = QsciLexerPython(self.editor)
        self.editor.setLexer(lexer)

        # Create a Save button
        self.save_button = QPushButton("Save", self)
        self.save_button.setGeometry(10, 560, 80, 30)
        self.save_button.clicked.connect(self.saveFile)

        # Create a layout for the editor and the Save button
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        layout.addWidget(self.save_button)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Open the specified code file
        self.openCodeFile(file_name)

    def openCodeFile(self, file_name):
        if os.path.exists(file_name):
            try:
                with open(file_name, "r") as file:
                    content = file.read()
                    self.editor.setText(content)
                    self.current_file = file_name
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error opening file: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", f"File not found: {file_name}")

    def saveFile(self):
        if hasattr(self, "current_file") and self.current_file:
            try:
                content = self.editor.text()
                with open(self.current_file, "w") as file:
                    file.write(content)
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving file: {str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No file to save.")

def main(file_name):
    app = QApplication(sys.argv)
    editor = CodeEditor(file_name)
    editor.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python codeeditor_qt.py <file_name>")
        sys.exit(1)
    main(sys.argv[1])
