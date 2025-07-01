# Setting Up the Development Environment

This guide describes how to set up a virtual environment for the project.

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

## Virtual Environment Setup Instructions

1. **Check Python Version**
   ```bash
   python3.12 --version
   ```
   Should display version 3.12.x or higher.

2. **Create Virtual Environment**
   ```bash
   python3.12 -m venv reader
   ```
   This will create a `reader` directory with all necessary files.

3. **Activate Virtual Environment**
   - For macOS/Linux:
     ```bash
     source reader/bin/activate
     ```
   - For Windows:
     ```cmd
     reader\Scripts\activate
     ```
   After activation, you'll see `(reader)` at the beginning of your command prompt.

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Deactivating the Environment

When you're done working, deactivate the virtual environment with:
```bash
deactivate
```

## Reactivation

To reactivate the environment after closing the terminal:
1. Navigate to the project's root directory
2. Run the activation command from step 3
