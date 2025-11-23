from fastq_reader import FastqReader
import customtkinter as ctk
from customtkinter import filedialog, CTk, CTkFrame, CTkLabel, CTkButton, CTkComboBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from pathlib import Path
import tkinter as tk
from tkinter import Toplevel

class FastqAnalyzerGUI(CTk):
    """
    Graphical interface for FASTQ file analysis with statistical visualization.
    
    Provides file selection via dialog with format filtering.
    Uses the existing plot generation from FastqReader class.
    """
    
    def __init__(self):
        super().__init__()
        
        # Configure appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("FASTQ File Analyzer")
        self.geometry("800x600")
        self.minsize(700, 500)
        
        # Initialize reader
        self.reader = None
        self.current_file = None
        self.load_button = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main interface layout"""
        # Main container
        main_frame = CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header_section(main_frame)
        
        # Content area
        content_frame = CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, pady=20)
        
        # File controls panel
        self.create_file_controls(content_frame)
        
        # Analysis controls panel
        self.create_analysis_controls(content_frame)
        
        # Statistics panel
        self.create_stats_panel(content_frame)
    
    def create_header_section(self, parent):
        """Create the application header"""
        header_frame = CTkFrame(parent)
        header_frame.pack(fill="x", pady=(0, 20))
        
        CTkLabel(header_frame, 
                text="FASTQ File Analyzer", 
                font=("Arial", 24, "bold")).pack(pady=20)
        
        CTkLabel(header_frame, 
                text="Analyze and visualize FASTQ sequence data", 
                font=("Arial", 14)).pack(pady=(0, 15))
    
    def create_file_controls(self, parent):
        """Create file selection controls"""
        file_frame = CTkFrame(parent)
        file_frame.pack(fill="x", padx=20, pady=15)
        
        CTkLabel(file_frame, 
                text="File Selection", 
                font=("Arial", 16, "bold")).pack(pady=15)
        
        # File path display
        self.file_label = CTkLabel(file_frame, 
                                  text="No file selected",
                                  wraplength=600,
                                  font=("Arial", 12),
                                  text_color="gray")
        self.file_label.pack(pady=10)
        
        # File selection buttons
        button_frame = CTkFrame(file_frame)
        button_frame.pack(fill="x", pady=15)
        
        CTkButton(button_frame, 
                 text="Browse FASTQ File",
                 command=self.browse_file,
                 height=35,
                 font=("Arial", 12)).pack(side="left", padx=10, fill="x", expand=True)
        
        self.load_button = CTkButton(button_frame,
                 text="Load File",
                 command=self.load_file,
                 state="disabled",
                 height=35,
                 font=("Arial", 12))
        self.load_button.pack(side="left", padx=10, fill="x", expand=True)
    
    def create_analysis_controls(self, parent):
        """Create analysis and visualization controls"""
        analysis_frame = CTkFrame(parent)
        analysis_frame.pack(fill="x", padx=20, pady=15)
        
        CTkLabel(analysis_frame,
                text="Analysis Tools",
                font=("Arial", 16, "bold")).pack(pady=15)
        
        # Plot selection
        CTkLabel(analysis_frame, text="Select Plot Type:", font=("Arial", 12)).pack(anchor="w", pady=10)
        
        self.plot_combo = CTkComboBox(analysis_frame,
                                     values=[
                                         "Per Base Sequence Quality",
                                         "Per Base Sequence Content", 
                                         "Sequence Length Distribution"
                                     ],
                                     state="readonly",
                                     height=35,
                                     font=("Arial", 12))
        self.plot_combo.pack(fill="x", pady=10)
        self.plot_combo.set("Per Base Sequence Quality")
        
        # Sample size control
        sample_frame = CTkFrame(analysis_frame)
        sample_frame.pack(fill="x", pady=10)
        
        CTkLabel(sample_frame, text="Sample Size:", font=("Arial", 12)).pack(side="left", padx=5)
        self.sample_size = CTkComboBox(sample_frame,
                                      values=["1000", "5000", "10000", "All"],
                                      state="readonly",
                                      width=120,
                                      height=35,
                                      font=("Arial", 12))
        self.sample_size.pack(side="right", padx=5)
        self.sample_size.set("5000")
        
        # Generate plot button
        self.plot_button = CTkButton(analysis_frame,
                                   text="Generate Plot",
                                   command=self.generate_plot,
                                   state="disabled",
                                   height=40,
                                   font=("Arial", 14, "bold"))
        self.plot_button.pack(fill="x", pady=20)
    
    def create_stats_panel(self, parent):
        """Create statistics display panel"""
        stats_frame = CTkFrame(parent)
        stats_frame.pack(fill="x", padx=20, pady=15)
        
        CTkLabel(stats_frame,
                text="File Statistics",
                font=("Arial", 16, "bold")).pack(pady=15)
        
        # Statistics labels
        self.stats_text = CTkLabel(stats_frame,
                                  text="No data loaded",
                                  justify="left",
                                  font=("Arial", 12),
                                  text_color="gray")
        self.stats_text.pack(anchor="w", pady=10, padx=10)
    
    def is_fastq_file(self, file_path):
        """Check if file has FASTQ extension"""
        fastq_extensions = {'.fastq', '.fq', '.fastq.gz', '.fq.gz'}
        return Path(file_path).suffix.lower() in fastq_extensions
    
    def browse_file(self):
        """Open file dialog to select FASTQ file"""
        file_types = [
            ("FASTQ files", "*.fastq *.fq"),
            ("Compressed FASTQ", "*.fastq.gz *.fq.gz"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select FASTQ File",
            filetypes=file_types
        )
        
        if file_path and self.is_fastq_file(file_path):
            self.current_file = file_path
            self.file_label.configure(
                text=f"Selected: {os.path.basename(file_path)}",
                text_color="white"
            )
            self.load_button.configure(state="normal")
            self.show_message("File Selected", f"Ready to load: {os.path.basename(file_path)}")
        elif file_path:
            self.show_error("Invalid Format", "Please select a FASTQ file (.fastq, .fq, .gz)")
    
    def load_file(self):
        """Load and parse the selected FASTQ file"""
        if not self.current_file:
            self.show_error("No file selected", "Please select a FASTQ file first")
            return
        
        try:
            # Update UI to show loading state
            self.file_label.configure(text="Loading... Please wait")
            self.load_button.configure(state="disabled")
            self.plot_button.configure(state="disabled")
            self.update_idletasks()
            
            # Create and configure reader
            self.reader = FastqReader(self.current_file)
            self.reader.read()
            
            # Update statistics
            self.update_statistics()
            
            # Enable plot generation
            self.plot_button.configure(state="normal")
            
            self.show_message("Success", f"Loaded {self.reader.count_sequences():,} sequences")
            
        except FileNotFoundError:
            self.show_error("File Not Found", f"Could not find file: {self.current_file}")
            self.reset_file_selection()
        except Exception as e:
            self.show_error("Loading Error", f"Failed to load file: {str(e)}")
            self.reset_file_selection()
    
    def reset_file_selection(self):
        """Reset file selection state"""
        self.current_file = None
        self.file_label.configure(text="No file selected", text_color="gray")
        self.load_button.configure(state="disabled")
        self.plot_button.configure(state="disabled")
        self.stats_text.configure(text="No data loaded", text_color="gray")
    
    def update_statistics(self):
        """Update the statistics display"""
        if not self.reader:
            return
        
        try:
            total_seqs = self.reader.count_sequences()
            avg_length = self.reader.get_average_sequence_len()
            total_bp = self.reader.total_length
            
            stats_text = f"""Total Sequences: {total_seqs:,}
Average Length: {avg_length:.2f} bp
Total Base Pairs: {total_bp:,}
File: {os.path.basename(self.current_file)}"""
            
            self.stats_text.configure(text=stats_text, text_color="white")
            
        except Exception as e:
            self.stats_text.configure(text=f"Error calculating statistics: {str(e)}", text_color="red")
    
    def generate_plot(self):
        """Generate the selected plot type using FastqReader's built-in plotting"""
        if not self.reader:
            self.show_error("No data", "Please load a FASTQ file first")
            return
        
        plot_type = self.plot_combo.get()
        sample_size = self.get_sample_size()
        
        try:
            # Update UI to show processing
            self.plot_button.configure(state="disabled", text="Generating...")
            self.update_idletasks()
            
            # Call the appropriate method from FastqReader
            if plot_type == "Per Base Sequence Quality":
                self.reader.per_base_sequence_quality(sample_size or 5000)
            elif plot_type == "Per Base Sequence Content":
                self.reader.per_base_sequence_content(sample_size or 5000)
            elif plot_type == "Sequence Length Distribution":
                self.reader.sequence_length_distribution()
            
            self.show_message("Plot Generated", f"Created {plot_type} visualization")
            
        except Exception as e:
            self.show_error("Plot Error", f"Failed to generate plot: {str(e)}")
        finally:
            # Re-enable plot button
            self.plot_button.configure(state="normal", text="Generate Plot")
    
    def get_sample_size(self):
        """Get sample size from combo box"""
        sample_text = self.sample_size.get()
        if sample_text == "All":
            return None
        return int(sample_text)
    
    def show_message(self, title, message):
        """Show success message in console"""
        print(f"✅ {title}: {message}")
    
    def show_error(self, title, message):
        """Show error message in console"""
        print(f"❌ ERROR - {title}: {message}")


def main():
    """Main function to launch the FASTQ analyzer GUI"""
    try:
        app = FastqAnalyzerGUI()
        app.mainloop()
    except Exception as e:
        print(f"Failed to start application: {e}")


if __name__ == "__main__":
    main()