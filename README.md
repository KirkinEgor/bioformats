# Bioinformatics File Readers

A Python library for reading and analyzing various bioinformatics file formats with comprehensive documentation and analysis capabilities.
## Supported Formats

-**FASTA** - Sequence files

-**FASTQ** - Sequence files with quality scores

-**SAM** - Sequence Alignment/Map files

-**VCF** - Variant Call Format files

## Features
### Core Functionality

    Abstract base classes for consistent interface across all readers

    Memory-efficient processing using generators

    Comprehensive validation of file formats and sequences

    Type annotations for better code clarity and IDE support

### Analysis Capabilities

    Quality score analysis for FASTQ files

    Variant statistics for VCF files

    Alignment metrics for SAM files

    Sequence statistics for FASTA files

### Visualization

    FastQC-style plots for quality control

    Statistical summaries and reports

    Genomic region filtering

### Graphical User Interface

    Modern GUI for FASTQ file analysis using CustomTkinter

    Interactive plots with sample size controls

    Real-time statistics display

    File format validation and error handling

## Installation
```bash

git clone https://github.com/bioinf-rnrmu-stotoshka/bioformats-omgmisosoup.git
cd bioformats-omgmisosoup

python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка в режиме разработки
pip install -e.
```

Prerequisites

    Python 3.7+

Required packages:

```bash
pip install -r requirements.txt
```

Usage
Command Line Usage
```python

from classes.fastq_reader import FastqReader

# Basic usage
reader = FastqReader("sample.fastq")
reader.read()

print(f"Total sequences: {reader.count_sequences()}")
print(f"Average length: {reader.get_average_sequence_len()}")

# Generate quality plots
reader.per_base_sequence_quality()
reader.per_base_sequence_content()
reader.sequence_length_distribution()
```

Graphical Interface
```python

from classes.fastq_gui import FastqAnalyzerGUI

# Launch the GUI application
app = FastqAnalyzerGUI()
app.mainloop()
```

The GUI provides:

    File browser with format filtering (.fastq, .fq, .gz)

    Interactive plot generation with configurable sample sizes

    Real-time statistics including sequence count and average length

    Multiple visualization types:

        Per-base sequence quality (FastQC-style)

        Per-base sequence content

        Sequence length distribution

GUI Features
File Management

    Browse and select FASTQ files with format validation

    Support for compressed files (.fastq.gz, .fq.gz)

    Automatic file loading and parsing

Analysis Tools

    Sample Size Control: Adjust analysis sample (1000, 5000, 10000, or all sequences)

    Multiple Plot Types:

        Per Base Sequence Quality: Boxplot with quality score zones

        Per Base Sequence Content: Nucleotide percentage across positions

        Sequence Length Distribution: Histogram of read lengths

Statistics Panel

    Total number of sequences

    Average sequence length

    Total base pairs analyzed

    File information display

Project Structure
```text

bioformats-omgmisosoup/
├── classes/
│   ├── __init__.py
│   ├── sequence_reader.py      # Abstract base class
│   ├── fastq_reader.py         # FASTQ reader implementation
│   ├── fastq_gui.py           # Graphical interface for FASTQ
│   ├── sam_reader.py          # SAM file reader
│   └── vcf_reader.py          # VCF file reader
├── tests/
│   ├── test_fastq_reader.py
│   └── test_sequence_reader.py
├── examples/
│   └── example_usage.py
├── setup.py
└── README.md
```
