# File Integrity Checker

A command-line Python tool that monitors file integrity using **SHA-256** hashes.

The program records hashes for selected files in a local JSON baseline. Later, it can calculate the hashes again and report whether files are unchanged, modified, or missing.

## Features

- Calculate SHA-256 hashes.
- Register multiple files in a baseline.
- Verify one file or all registered files.
- List registered files.
- Remove a file from the baseline.
- Read files in chunks instead of loading the entire file into memory.
- Handle common file and baseline errors.

## Requirements

- Python 3.8 or newer
- No third-party packages (Python standard library only)

## Run

Open a terminal in the project directory and run:

```bash
python main.py
```

On some systems, use `python3 main.py` instead.

## How to use

1. Choose **Register files** and enter the paths of the files you want to monitor. Press Enter on an empty line when finished.
2. Choose **Verify one file** to check a specific registered file.
3. Choose **Verify all files** to generate an integrity report for every registered file.
4. Choose **List registered files** to see the files stored in the baseline.
5. Choose **Remove a registered file** to remove an entry from the baseline.
6. Choose **Exit** to close the program.

Relative paths are resolved from the directory containing `main.py`.

## Baseline file

The program creates `baseline.json` locally when files are registered. This file is intentionally excluded from Git because it contains machine-specific file paths and is generated from the files on the user's own computer.

If the baseline does not exist, register files to create a new one.

## Important security note

This project is a learning tool for basic file-integrity monitoring. The baseline is stored locally as JSON. If an attacker can modify both a monitored file and its baseline, they may be able to hide the change. For stronger protection, keep a trusted copy of the baseline somewhere an attacker cannot modify, or use a digitally protected baseline.

## Project structure

```text
file-integrity-checker/
├── main.py
├── README.md
└── .gitignore
```

## Concepts practiced

- Python functions and modules
- File handling and binary reading
- Chunk-based processing
- SHA-256 hashing with `hashlib`
- JSON serialization and deserialization
- Exception handling
- File path handling with `os`
