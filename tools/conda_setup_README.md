# FMSLogo Code Evaluator - conda Setup

## Overview
This tool automatically evaluates FMSLogo code submissions and provides detailed feedback on whether the code meets daily challenge requirements.

## Prerequisites
- **conda** installed (Anaconda or Miniconda)
- **Python 3.9+**
- **GUI support** (for turtle graphics display)

## Setup Instructions

### 1. Create conda Environment
```bash
conda create -n turtle_eval python=3.9
```

### 2. Activate Environment
```bash
conda activate turtle_eval
```

### 3. Install Dependencies
```bash
# Install packages available through conda
conda install matplotlib tk

# Install turtle via pip (not available in conda)
pip install turtle
```

### 4. Verify Installation
```bash
# Check that packages are installed
conda list
```

## Running the Evaluator

### GUI Mode (Recommended)
```bash
# Make sure environment is active
conda activate turtle_eval

# Navigate to project directory
cd /path/to/teaching_my_autistic_son_programming

# Run the evaluator
python tools/fmslogo_evaluator.py
```

### Console Mode
```bash
conda activate turtle_eval
cd /path/to/teaching_my_autistic_son_programming
python tools/fmslogo_evaluator.py --console
```

## Daily Workflow

### Quick Start
```bash
# Activate environment
conda activate turtle_eval

# Run evaluator
python tools/fmslogo_evaluator.py

# When done, deactivate
conda deactivate
```

### Step-by-Step Usage
1. **Activate environment**: `conda activate turtle_eval`
2. **Open evaluator**: GUI window appears
3. **Select day number** from dropdown (1-7)
4. **Paste student's code** in text area
5. **Click "Evaluate Code"** button
6. **Review results** in output panel
7. **Close application** when done
8. **Deactivate environment**: `conda deactivate`

## Environment Management

### List All conda Environments
```bash
conda env list
```

### Remove Environment (if needed)
```bash
conda env remove -n turtle_eval
```

### Export Environment (for sharing)
```bash
conda activate turtle_eval
conda env export > environment.yml
```

### Create from Exported Environment
```bash
conda env create -f environment.yml
```

## Troubleshooting

### "conda: command not found"
- Ensure conda is installed and in your PATH
- Try restarting terminal after conda installation

### "No module named turtle"
```bash
conda activate turtle_eval
pip install turtle
```

### "No module named tkinter"
```bash
# On Ubuntu/Debian
sudo apt-get install python3-tk

# Then reinstall Python in conda
conda install python=3.9
```

### Turtle graphics window doesn't appear
- Ensure you have GUI/X11 support
- Try console mode: `python tools/fmslogo_evaluator.py --console`
- On Linux, ensure DISPLAY variable is set

### "ModuleNotFoundError: No module named matplotlib"
```bash
conda activate turtle_eval
conda install matplotlib
```

## Example Session

```bash
# Start evaluation session
$ conda activate turtle_eval
(turtle_eval) $ cd /home/user/teaching_my_autistic_son_programming
(turtle_eval) $ python tools/fmslogo_evaluator.py

# GUI opens, evaluate code, close application

(turtle_eval) $ conda deactivate
$
```

## Features Available

### Supported Days
- **Day 1**: Forward/Backward movement
- **Day 2**: Left/Right turns and corners
- **Day 5**: Square creation
- More days can be added by extending the evaluator

### Evaluation Output
- **Visual turtle graphics** - See exactly what the code draws
- **Pass/fail tests** - Specific requirements for each day
- **Detailed feedback** - Constructive suggestions for improvement
- **Score summary** - Overall assessment and next steps

## Environment Benefits

✅ **Isolated dependencies** - Won't interfere with system Python  
✅ **Reproducible setup** - Same environment every time  
✅ **Easy cleanup** - Remove environment when no longer needed  
✅ **Version control** - Specific package versions for stability  
✅ **Cross-platform** - Works on Windows, Mac, Linux  

## Quick Reference

| Command | Purpose |
|---------|---------|
| `conda activate turtle_eval` | Start using the environment |
| `conda deactivate` | Stop using the environment |
| `conda list` | Show installed packages |
| `conda env list` | Show all environments |
| `python tools/fmslogo_evaluator.py` | Run the evaluator (GUI) |
| `python tools/fmslogo_evaluator.py --console` | Run in console mode |

---

**Note**: Always activate the conda environment before running the evaluator to ensure all dependencies are available.