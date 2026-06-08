# Quick Start

BetterRecolor can be run in two ways.

| Method | Best for |
| --- | --- |
| Google Colab | Running the tool from a browser without local setup |
| Local environment | Repeatedly iterating on files from your own machine |

Both methods use the same input, configuration, and output layout.

| Type | Location |
| --- | --- |
| Input | `Assets/BRLYT` and `Assets/BRLAN` |
| Color settings | `color_config.json` |
| Output | `Output` |

## Run in Google Colab

1. Open `BetterRecolor.ipynb` from GitHub in Google Colab.
2. Run only the setup cells first.
3. Edit `/content/BetterRecolor/color_config.json`.
4. Run the remaining cells from top to bottom.
5. Download the generated `Output.zip`.

::: warning
The Colab setup cells delete the existing `/content/BetterRecolor` directory before cloning a fresh copy.
If you have edited `color_config.json` or added input files under that directory, back them up to Google Drive or another safe location first.
:::

## Run Locally

Python 3.11 or later is recommended.

```sh
pip install -r requirements.txt
python main.py
```

To skip interactive prompts and run in English, use:

```sh
python main.py --lang en --yes
```

On WSL2, use `python3`:

```sh
python3 main.py
```

## Color Settings

Edit the following fields in `color_config.json`.

| Field | Description |
| --- | --- |
| `presets` | Colors applied to BRLYT files |
| `outline.free` | BRLAN outline colors for the normal state |
| `outline.select` | BRLAN outline colors for the selected state |

All colors must use `#RRGGBB` format.

## After Generating Output

1. Extract the generated files from `Output` or `Output.zip`.
2. Copy the required `*.d` folders over your source assets.
3. Repack the files into SZS archives with [Wiimms SZS Tool](https://szs.wiimm.de/wszst/).
4. Check the result in-game.

## Notes

- Local runs recreate `tmp` and `Output` each time.
- In Colab, rerunning the setup cells deletes everything under `/content/BetterRecolor`.
- Some multiplayer button colors may intentionally remain unchanged to preserve player identification.

