import os
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox, Frame, Scrollbar, Listbox, StringVar, END
from PyPDF2 import PdfMerger

def select_pdfs():
    """Open a file dialog to select multiple PDF files."""
    files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF files", "*.pdf")],
        initialdir=os.getcwd()
    )
    for file in files:
        if file not in pdf_files:
            pdf_files.append(file)
            update_pdf_listbox()

def update_pdf_listbox():
    """Update the Listbox to display the current PDFs with delete buttons."""
    listbox_files.delete(0, END)
    for pdf in pdf_files:
        listbox_files.insert(END, pdf)

def remove_pdf(index):
    """Remove a PDF file from the list."""
    del pdf_files[index]
    update_pdf_listbox()

def select_output_directory():
    """Open a dialog to select the output directory."""
    directory = filedialog.askdirectory(title="Select Output Directory", initialdir=os.getcwd())
    if directory:
        output_directory.set(directory)
        label_output_directory.config(text=directory)

def merge_pdfs():
    """Merge the selected PDF files and save to the specified location."""
    if not pdf_files:
        messagebox.showwarning("No Files", "Please select at least two PDF files.")
        return

    # Use the default Documents folder if no output directory is selected
    default_directory = os.path.expanduser("~/Documents")
    if not output_directory.get():
        output_directory.set(default_directory)

    # Use a default filename if none is provided
    filename = output_filename.get().strip() or "merged_output.pdf"
    # Ensure the output filename ends with .pdf
    if not filename.lower().endswith(".pdf"):
        filename += ".pdf"

    output_file = os.path.join(output_directory.get(), filename)

    try:
        merger = PdfMerger()
        for pdf in pdf_files:
            merger.append(pdf)

        merger.write(output_file)
        merger.close()
        messagebox.showinfo("Success", f"PDFs have been successfully merged into {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while merging PDFs: {e}")

# Initialize the GUI
root = Tk()
root.title("PDF Merger")
root.geometry("600x500")

# Store selected PDF files
pdf_files = []

# Output directory and filename
output_directory = StringVar()
output_filename = StringVar()

# Frame for list of selected PDFs
frame_listbox = Frame(root)
frame_listbox.pack(pady=10, fill="both", expand=True)

# Scrollable Listbox for PDFs
scrollbar = Scrollbar(frame_listbox, orient="vertical")
listbox_files = Listbox(frame_listbox, yscrollcommand=scrollbar.set, selectmode="single", height=10)
scrollbar.config(command=listbox_files.yview)
scrollbar.pack(side="right", fill="y")
listbox_files.pack(side="left", fill="both", expand=True)

# Function to remove the selected PDF
def on_listbox_select(event):
    selection = listbox_files.curselection()
    if selection:
        index = selection[0]
        remove_pdf(index)

listbox_files.bind('<Delete>', on_listbox_select)

# Select PDF files button
btn_select_pdfs = Button(root, text="Select PDFs", command=select_pdfs)
btn_select_pdfs.pack(pady=10)

# Select output directory button
btn_select_output_directory = Button(root, text="Select Output Directory", command=select_output_directory)
btn_select_output_directory.pack(pady=10)

# Label for showing selected output directory
label_output_directory = Label(root, text="No directory selected, using default (Documents)", justify="left")
label_output_directory.pack(pady=5)

# Input for output file name
Label(root, text="Output Filename:").pack(pady=5)
entry_output_filename = Entry(root, textvariable=output_filename)
entry_output_filename.pack(pady=5)
entry_output_filename.insert(0, "merged_output.pdf")

# Merge PDFs button
btn_merge = Button(root, text="Merge PDFs", command=merge_pdfs)
btn_merge.pack(pady=20)

# Start the GUI loop
root.mainloop()
