# CareerFoundry Python Course

This repository contains my work for the CareerFoundry Python course, organized by exercise.

## Exercise 1.1: Python Environment Setup and Basic Scripting

### Overview
This exercise focused on setting up a Python development environment, creating basic Python scripts, and learning about virtual environments and package management.

### What Was Accomplished

1. **Python Installation**: Verified Python 3.8.7 installation
2. **Virtual Environment Setup**: Created a virtual environment named `cf-python-base` using Python 3.8.7
3. **Basic Script Creation**: Created `add.py` - a script that takes two user inputs and adds them together
4. **IPython Installation**: Set up IPython shell in the virtual environment for enhanced interactive Python development
5. **Requirements File**: Generated `requirements.txt` to document all installed packages
6. **Environment Replication**: Created a second environment `cf-python-copy` and installed packages from `requirements.txt` to demonstrate environment portability

### Project Structure

```
.
└── Exercise 1.1/
    ├── add.py              # Script that adds two user-input numbers
    ├── hello.py            # Simple "Hello, World!" script
    └── requirements.txt    # List of installed packages and versions
```

### Setup Instructions

#### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment with Python 3.8.7
python3.8 -m venv ~/.virtualenvs/cf-python-base

# Activate the environment
cd ~/.virtualenvs/cf-python-base/bin
source activate
```

#### 2. Install Dependencies

```bash
# Navigate to project directory
cd /path/to/this/repository/Exercise\ 1.1/

# Install packages from requirements.txt
pip install -r requirements.txt
```

#### 3. Verify Installation

```bash
# Check Python version
python --version

# Verify IPython installation
ipython --version
```

### Running the Scripts

#### Run add.py
```bash
python Exercise\ 1.1/add.py
```
The script will prompt you to enter two numbers, then display their sum.

#### Run hello.py
```bash
python Exercise\ 1.1/hello.py
```
This will print "Hello, World!" to the console.

#### Launch IPython Shell
```bash
ipython
```

### Requirements

- Python 3.8.7
- pip (Python package installer)
- Virtual environment support (venv module)

### Installed Packages

The following packages are installed in the virtual environment (see `Exercise 1.1/requirements.txt` for complete list):

- **ipython** (8.12.3) - Enhanced interactive Python shell
- Dependencies: traitlets, jedi, prompt-toolkit, pygments, and others

### Notes

- All scripts were developed and tested in a virtual environment to maintain project isolation
- The requirements.txt file ensures consistent package versions across different environments
- This exercise demonstrates best practices for Python project setup and dependency management

