import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

class CSVSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Splitter")

        # Initialize file and directory paths
        self.file_path = None
        self.output_dir = None

        # Create a label for instructions
        self.label = tk.Label(root, text="Select a CSV file and output folder.")
        self.label.pack(pady=10, padx=100)

        # Frame for file selection
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(pady=5)

        # Button to select a file
        self.select_file_btn = tk.Button(self.file_frame, text="Select CSV File", command=self.select_file)
        self.select_file_btn.pack(side=tk.LEFT)

        # Label to display selected file
        self.file_label = tk.Label(self.file_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=5)

        self.input_rec = tk.Label(root, text="")
        self.input_rec.pack(pady=0)
        # Frame for folder selection
        self.folder_frame = tk.Frame(root)
        self.folder_frame.pack(pady=5)

        # Button to select output directory
        self.select_folder_btn = tk.Button(self.folder_frame, text="Select Output Folder", command=self.select_folder)
        self.select_folder_btn.pack(side=tk.LEFT)

        # Label to display selected output folder
        self.folder_label = tk.Label(self.folder_frame, text="No folder selected")
        self.folder_label.pack(side=tk.LEFT, padx=5)

        # Entry to specify the number of records per split
        self.records_label = tk.Label(root, text="Enter number of records per file:")
        self.records_label.pack(pady=5)
        self.records_entry = tk.Entry(root)
        self.records_entry.pack(pady=5)
        #
        
        #
        # Button to run the split
        self.split_btn = tk.Button(root, text="Split CSV", command=self.split_file)
        self.split_btn.pack(pady=10)
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()  # Ensure all pending geometry calculations are done
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.file_label.config(text=f"Selected file: {os.path.basename(self.file_path)}")
            self.input_rec.config(text=f"Number of records: {len(pd.read_csv(self.file_path))}")
        else:
            self.file_label.config(text=f"No file selected")
            self.input_rec.config(text=f"")

    def select_folder(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.folder_label.config(text=f"Selected folder: {self.output_dir}")
        else:
            self.folder_label.config(text=f"No folder selected")

    def split_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a CSV file.")
            return

        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        try:
            records_per_file = (int(self.records_entry.get()))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for records per file.")
            return

        try:
            self.modify_and_split_file(self.file_path, records_per_file, self.output_dir)
            messagebox.showinfo("Success", "CSV file split successfully!")
            self.output_dir=self.output_dir
            self.file_label.config(text=f"No file selected")
            self.input_rec.config(text=f"")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def modify_and_split_file(self, file_path, records_per_file, output_dir):
        # Read the CSV file using pandas
        df = pd.read_csv(file_path)

        # Split the file into chunks
        total_records = len(df)
        num_files = total_records // records_per_file + (1 if total_records % records_per_file != 0 else 0)

        # Get the file name without extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Save each chunk into a new file
        for i in range(num_files):
            start_idx = i * records_per_file
            end_idx = min((i + 1) * records_per_file, total_records)
            chunk = df[start_idx:end_idx]

            # Create the full path for the output file in the chosen directory
            output_file = os.path.join(output_dir, f"{file_name}_part_{i + 1}.csv")
            chunk.to_csv(output_file, index=False)
            print(f"Saved {output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVSplitterApp(root)
    root.mainloop()
