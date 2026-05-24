[![CI](https://github.com/8MeTools/BetterRecolor/actions/workflows/ci.yml/badge.svg)](https://github.com/8MeTools/BetterRecolor/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# BetterRecolor

For Japanese, see [README_JP.md](README_JP.md).

## Overview

This tool lets you batch-edit button and text colors shown in-game.  
It edits files decoded to JSON or JSON5 format, then encodes them back to BRLYT (layout files) and BRLAN (animation files). You can use it on Google Colab or in a local environment.

## Getting Started

If you are new to Google Colaboratory, this video may help:

- [How to Use GOOGLE COLAB | Google Colab Tutorials for Beginners | GeeksforGeeks](https://youtu.be/TqqkZLHoY0o?si=wo1SAvFcU866YvkZ)

### Why Colab

- **Environment-independent**  
  Processing runs on assigned cloud machines, so results are not tied to your local PC setup.
- **No local setup required**  
  You can run code in the browser, so local Python and library installation are unnecessary. Even without Python knowledge, you can use the tool by running cells.

## Usage

There are two ways to run BetterRecolor:

- **Run on Google Colab**: Best if you want to use it without local setup
- **Run locally**: Best if you want to iterate repeatedly on your own machine

The input/output model is the same for both methods:

- Input: `Assets/BRLYT` and `Assets/BRLAN`
- Output: `Output`
- Color settings file: `color_config.json`

### 1. Run on Google Colab

1. **Open the notebook in Colab**

   Open [BetterRecolor.ipynb](BetterRecolor.ipynb) in this repository, then choose Open in Colab.

> [!WARNING]
> If you are not confident with Colab execution order, always open the notebook from GitHub for each run. Since this repository may be updated frequently, opening and running a cloned notebook via Google Drive may lead to unexpected behavior if the notebook is updated after cloning.

2. **Run setup cells first**

   Run only until these setup tasks are complete:

   - Re-fetch `BetterRecolor` under `/content/BetterRecolor` (any existing `/content/BetterRecolor` directory will be removed before cloning)
   - Remove development files that are not needed for Colab execution
   - Install dependencies from `requirements.txt`

> [!WARNING]
> The Colab setup cell deletes the existing `/content/BetterRecolor` directory before cloning.  
> If you have edited `color_config.json` or added input files under `/content/BetterRecolor`, download them first or copy them to a separate location such as Google Drive, then move them back after setup.
> Since the JSON structure may change between versions, it is recommended to review the latest `color_config.json` on GitHub before editing.

   When setup finishes successfully, you should see this message:

   ```
   ✅Setup complete! Open color_config.json to edit.
   ```

> [!WARNING]
> The setup section is only the first few cells. Do not run all cells yet.

3. **Edit `color_config.json`**

   Edit this file:

   `/content/BetterRecolor/color_config.json`

   - `presets`: Colors used on the BRLYT side
   - `outline.free` / `outline.select`: Outline colors used on the BRLAN side
   - Use `#RRGGBB` format for all color values

> [!NOTE]
> In Colab, open the left file pane and go to `content` -> `BetterRecolor`, then double-click `color_config.json` to edit it.

4. **Run the remaining cells from top to bottom**

   These steps are performed by the remaining cells:

   - Load and apply color settings
   - Generate output under `Output`

   If a confirmation prompt appears for color settings, review it and continue.

   To run without interactive prompts, you can change the execution cell to:

   ```sh
   !python main.py --lang en --yes
   ```

   - `--lang en`: Skip language selection and run in English
   - `--yes` / `-y`: Automatically confirm the color settings

5. **Get generated files**

   Run the final cell to compress `Output` into `Output.zip` and download it from the browser.

6. **Apply files to your game assets**

   Extract the downloaded files, then overwrite the required `*.d` folders in your original assets.

7. **Repack to SZS and verify**

   Use [Wiimms SZS Tool](https://szs.wiimm.de/wszst/) to repack, then check the result in-game.

### 2. Run Locally

#### Prerequisites

- Python 3.11 or newer is recommended
- `Assets/BRLYT` and `Assets/BRLAN` exist under the project root

#### Steps

1. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

2. **Edit the color settings file**

   Edit `color_config.json`.

   - `presets`: Colors used on the BRLYT side
   - `outline.free` / `outline.select`: Outline colors used on the BRLAN side
   - Use `#RRGGBB` format for all color values

3. **Run the tool**

   ```sh
   python main.py
   ```

   If you run in WSL2, use `python3`:

   ```sh
   python3 main.py
   ```

   To run without interactive prompts, use:

   ```sh
   python main.py --lang en --yes
   ```

   - `--lang ja` / `--lang en`: Skip language selection
   - `--yes` / `-y`: Automatically confirm the color settings

4. **Choose language and confirm settings**

   At startup, you will see:

   `Language / 言語 (ja/en) [ja]:`

   Enter `ja` or `en`.

   Then review the color preview and confirm with `Y/N`.

5. **Check output**

   After processing, files are written to `Output`. The output includes generated files and `pack-guide.txt`.

#### Notes for Re-runs

- **Local environment**
  - Each run recreates `tmp` and `Output`.
  - If you need previous output, back it up before running again.
- **Google Colab**
  - In the provided notebook, the setup step removes and re-clones the entire `/content/BetterRecolor` directory.
  - Any assets or edited config files placed under that directory will be deleted on re-run. Store long-term data in Google Drive, `/content/drive`, or another location that is not removed by the setup step.

## For Developers

### Lint / Test

```sh
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest
```

### Update Colab Badge

The Colab badge URL in `BetterRecolor.ipynb` is generated from `colab_badge.json`.
When the GitHub owner, repository, branch, or notebook path changes, edit `colab_badge.json`, then run:

```sh
python scripts/update_colab_badge.py
```

The script updates only the markdown cell that contains the Colab badge.

### Release Workflow (CalVer)

Uses a date + serial format, for example: `26.01.28.1`

1. Bump version

   ```sh
   python scripts/bump_version.py
   ```

2. Create tag

   ```sh
   python scripts/bump_version.py --tag
   ```

3. Create tag + push (Release is created after CI passes)

   ```sh
   python scripts/bump_version.py --tag --push
   ```

### CI / Release Conditions

- CI runs `ruff check .` and `pytest` on `push` and `pull_request`
- A Release is created only when a `v*` tag (for example `v26.01.28.1`) is attached to a commit that passed CI

## FAQ

### Q. I ran Colab cells in the wrong order. What should I do?

**A.** If you are not confident with Colab execution order, restart cleanly and run again from the beginning.  
In the top menu, choose Runtime, then Disconnect and delete runtime. After that, execute cells in order from the top.

### Q. In multiplayer, some buttons did not change to the selected color.

**A.** Some multiplayer button colors are intentionally not changed because player-by-player identification would become difficult.

## Reporting Issues

- Please use GitHub Issues.

## Third-Party

This repository bundles [wuj5](https://github.com/stblr/wuj5), which is licensed under MIT. See `wuj5/LICENSE` for details.
