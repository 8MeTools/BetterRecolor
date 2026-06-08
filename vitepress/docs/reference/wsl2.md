# Run on WSL2

Last updated: April 4, 2026

This page explains how to run BetterRecolor on WSL2.

The workflow is mostly the same as on Windows or macOS, but Python on Ubuntu and Debian-based distributions may block system-wide package installation because of PEP 668. The recommended approach is to create a project-local virtual environment with `venv` and install dependencies there.

## Audience

This page is for users who:

- use WSL2
- want to run BetterRecolor inside WSL2
- are comfortable with basic Linux shell commands

::: warning
Run the commands below in a WSL2 terminal, not in PowerShell or Command Prompt.
:::

## Verified Environment

The following environment has been tested:

- Windows 11 Home 64-bit
- WSL2 with Ubuntu 24.04 LTS
- Python 3.12.2

## Prerequisites

Install Python, pip, and venv in WSL2 before continuing.

Reference: [Install Python, pip, and venv on WSL2 and create a virtual environment](https://zenn.dev/ak_yoshimatsu/articles/69457d3f44fe55)

## Steps

### 1. Clone the Repository

```bash
git clone https://github.com/8MeTools/BetterRecolor.git
```

### 2. Change into the Repository Directory

```bash
cd path/to/BetterRecolor
```

Replace `path/to/BetterRecolor` with the actual path to your cloned repository.

### 3. Create a Virtual Environment

```bash
python3 -m venv .btrc
```

This creates a `.btrc` virtual environment inside the BetterRecolor directory.

To confirm that it was created, list hidden files:

```bash
ls -la
```

### 4. Activate the Virtual Environment

```bash
source .btrc/bin/activate
```

After activation, your shell prompt should include `(.btrc)`.

```bash
(.btrc) user@hostname:~/path/to/BetterRecolor$
```

### 5. Install Dependencies

Install dependencies while the virtual environment is active.

```bash
pip install -r requirements.txt
```

### 6. Run BetterRecolor

```bash
python3 main.py
```

Follow the prompts to choose a language and confirm the color settings.

To skip the prompts and run in English, use:

```bash
python3 main.py --lang en --yes
```

### 7. Deactivate the Virtual Environment

When you are done, deactivate the environment:

```bash
deactivate
```

The `(.btrc)` prefix should disappear from your prompt.

## Running Again

For future runs, change into the repository, activate the virtual environment, and start BetterRecolor.

```bash
cd path/to/BetterRecolor
source .btrc/bin/activate
python3 main.py
```

## Notes

On WSL2, avoid installing Python packages directly into the system Python environment. Keeping BetterRecolor dependencies inside `.btrc` makes the setup easier to reproduce and prevents conflicts with system-managed Python packages.

