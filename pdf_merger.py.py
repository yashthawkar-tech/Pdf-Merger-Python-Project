import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pypdf import PdfWriter
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("500x400")
        self.pdf_files = []
        
        # Title
        title_label = tk.Label(root, text="PDF Merger", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # Add PDF button
        add_btn = tk.Button(button_frame, text="Add PDF Files", command=self.add_files, bg="#4CAF50", fg="white", padx=10, pady=5)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Remove selected button
        remove_btn = tk.Button(button_frame, text="Remove Selected", command=self.remove_file, bg="#f44336", fg="white", padx=10, pady=5)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear all button
        clear_btn = tk.Button(button_frame, text="Clear All", command=self.clear_files, bg="#FF9800", fg="white", padx=10, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Listbox to display selected files
        list_label = tk.Label(root, text="Selected PDFs:", font=("Arial", 10, "bold"))
        list_label.pack(anchor=tk.W, padx=20, pady=(10, 0))
        
        self.file_listbox = tk.Listbox(root, height=8, width=60)
        self.file_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(self.file_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Output filename entry
        filename_frame = tk.Frame(root)
        filename_frame.pack(padx=20, pady=10, fill=tk.X)
        
        tk.Label(filename_frame, text="Output Filename:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.output_entry = tk.Entry(filename_frame, width=30)
        self.output_entry.pack(side=tk.LEFT, padx=10)
        self.output_entry.insert(0, "merged.pdf")
        
        # Merge button
        merge_btn = tk.Button(root, text="Merge PDFs", command=self.merge_pdfs, bg="#2196F3", fg="white", padx=20, pady=10, font=("Arial", 11, "bold"))
        merge_btn.pack(pady=10)
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
        self.update_listbox()
    
    def remove_file(self):
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.pdf_files.pop(index)
            self.update_listbox()
    
    def clear_files(self):
        self.pdf_files = []
        self.update_listbox()
    
    def update_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for idx, file in enumerate(self.pdf_files, 1):
            self.file_listbox.insert(tk.END, f"{idx}. {os.path.basename(file)}")
    
    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("Warning", "Please select at least one PDF file!")
            return
        
        output_filename = self.output_entry.get()
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        try:
            merger = PdfWriter()
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(output_filename)
            messagebox.showinfo("Success", f"PDFs merged successfully!\nOutput: {output_filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop() 