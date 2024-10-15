import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFont, QColor
from pdf_merger import merge_pdfs

class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet(self.load_styles())
        self.setWindowIcon(QIcon("resources/icon.png"))  # Optional: Add your custom icon
        self.pdf_files = []

        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Title Label
        title = QLabel("PDF Merger")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(title)

        # PDF Table
        self.pdf_table = QTableWidget(0, 2)
        self.pdf_table.setHorizontalHeaderLabels(["PDF Files", "Action"])
        self.pdf_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.pdf_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.pdf_table.setStyleSheet("background: #f0f0f0; border-radius: 10px; padding: 10px;")
        self.pdf_table.verticalHeader().setVisible(False)  # Hide vertical headers for cleaner look
        self.pdf_table.setShowGrid(False)  # Remove internal table grid lines for a cleaner appearance
        self.update_table_placeholder()

        layout.addWidget(self.pdf_table)

        # Buttons Layout
        button_layout = QHBoxLayout()
        self.btn_select_pdfs = QPushButton("Select PDFs")
        self.btn_select_pdfs.clicked.connect(self.select_pdfs)
        button_layout.addWidget(self.btn_select_pdfs)

        self.btn_select_output_directory = QPushButton("Select Output Directory")
        self.btn_select_output_directory.clicked.connect(self.select_output_directory)
        button_layout.addWidget(self.btn_select_output_directory)

        layout.addLayout(button_layout)

        # Output Directory Display
        self.output_directory = QLabel("No directory selected, using default (Documents)")
        self.output_directory.setStyleSheet("color: #555;")
        layout.addWidget(self.output_directory)

        # Output Filename Input
        self.output_filename = QLineEdit()
        self.output_filename.setPlaceholderText("Enter output filename (e.g., merged_output.pdf)")
        self.output_filename.setStyleSheet("padding: 8px; border: 1px solid #ddd; border-radius: 5px;")
        layout.addWidget(self.output_filename)

        # Merge Button
        self.btn_merge = QPushButton("Merge PDFs")
        self.btn_merge.setObjectName("mergeButton")
        self.btn_merge.clicked.connect(self.handle_merge_pdfs)
        layout.addWidget(self.btn_merge)

        self.setLayout(layout)

    def load_styles(self):
        """Load a modern stylesheet for the application."""
        with open("styles.qss", "r") as f:
            return f.read()

    def select_pdfs(self):
        """Open a file dialog to select multiple PDF files."""
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
                    self.add_pdf_to_table(file)
            self.update_table_placeholder()

    def add_pdf_to_table(self, pdf_file):
        """Add a PDF file to the table widget."""
        row = self.pdf_table.rowCount()
        self.pdf_table.insertRow(row)

        # Add PDF filename
        pdf_item = QTableWidgetItem(os.path.basename(pdf_file))
        pdf_item.setFont(QFont("Arial", 10))
        pdf_item.setForeground(QColor("#2E3440"))  # Ensure text color is visible
        pdf_item.setToolTip(pdf_file)  # Show full path on hover
        pdf_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Make it non-editable but selectable
        self.pdf_table.setItem(row, 0, pdf_item)

        # Add Remove Button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("background-color: #BF616A; color: #ECEFF4; padding: 5px;")
        remove_button.clicked.connect(lambda: self.remove_pdf(row))
        self.pdf_table.setCellWidget(row, 1, remove_button)

    def remove_pdf(self, row):
        """Remove a PDF file from the table and list."""
        self.pdf_files.pop(row)
        self.pdf_table.removeRow(row)
        self.update_table_placeholder()

    def update_table_placeholder(self):
        """Update the placeholder message in the table if no PDFs are added."""
        if self.pdf_table.rowCount() == 0:
            self.pdf_table.setRowCount(1)
            placeholder_item = QTableWidgetItem("No PDFs selected")
            placeholder_item.setFlags(Qt.ItemIsEnabled)  # Make the placeholder non-selectable
            placeholder_item.setForeground(QColor("#888"))  # Gray color for placeholder text
            self.pdf_table.setItem(0, 0, placeholder_item)
            self.pdf_table.setSpan(0, 0, 1, 2)  # Span across both columns
        else:
            self.pdf_table.setRowCount(len(self.pdf_files))

    def select_output_directory(self):
        """Open a dialog to select the output directory."""
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_directory.setText(f"Output Directory: {directory}")
        else:
            self.output_directory.setText("No directory selected, using default (Documents)")

    def handle_merge_pdfs(self):
        """Handle the merge PDFs button click."""
        output_directory = (
                self.output_directory.text().replace("Output Directory: ", "")
                or os.path.expanduser("~/Documents")
        )
        output_filename = self.output_filename.text().strip() or "merged_output.pdf"

        try:
            merge_pdfs(self.pdf_files, output_directory, output_filename)
            QMessageBox.information(self, "Success", f"PDFs have been successfully merged into {os.path.join(output_directory, output_filename)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while merging PDFs: {str(e)}")
