import sys
from PySide6.QtWidgets import QApplication
from ui import PDFMergerApp

def main():
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
