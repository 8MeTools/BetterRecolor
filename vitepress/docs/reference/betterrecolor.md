# What Is BetterRecolor?

Last updated: April 3, 2026

BetterRecolor is a tool for batch-editing the button and text colors shown in-game.

When editing UI files manually, you need to find the target files, update multiple `BRLYT` and `BRLAN` files, and check for missed changes. BetterRecolor moves that work into `color_config.json` so the changes can be applied in a single workflow.

## What It Does

- Batch-edits button and text colors
- Applies color settings to BRLYT files
- Applies outline colors to BRLAN files
- Runs in Google Colab or a local environment
- Writes generated files to `Output`

## Why Use Google Colab?

Google Colab lets you run BetterRecolor without setting up Python locally.

| Benefit | Description |
| --- | --- |
| Less environment-dependent | Processing runs on an assigned cloud machine, so results are less affected by differences in your local PC setup. |
| No local setup required | You can install dependencies and run the tool from browser cells. |

If you are not familiar with Python or the internal game file structure, start with the Colab workflow.

## Inputs and Outputs

BetterRecolor uses the following layout.

| Type | Location |
| --- | --- |
| Input | `Assets/BRLYT` and `Assets/BRLAN` |
| Color settings | `color_config.json` |
| Output | `Output` |

For the full run workflow, see the [Quick Start](/getting-started).

## Color Configuration

The main fields in `color_config.json` are:

| Field | Description |
| --- | --- |
| `presets` | Colors used by BRLYT files |
| `outline.free` | BRLAN outline colors for the normal state |
| `outline.select` | BRLAN outline colors for the selected state |

Use `#RRGGBB` for all color values.

## Checking Colors in Switch Toolbox

Some entries in `color_config.json`, such as `white` and `black`, correspond to Pane colors that can be inspected in Switch Toolbox. A practical workflow is to preview the Pane in Switch Toolbox, choose the color you want, and then copy that value into `color_config.json`.

For example, `MenuSingle.szs` contains Panes such as:

| Pane Name | File Name |
| --- | --- |
| `fuchi_pattern2` (`fuchi_pattern`) | `./button/blyt/common_w004_menu.brlyt` |
| `color_base2` (`color_base`) | `./button/blyt/common_w004_menu.brlyt` |
| `color_yajirushi` | `./button/blyt/common_w016_yajirushi_left.brlyt` |
| `ability_graph2` (`ability_graph`) | `./control/blyt/common_w099_machine_ability.brlyt` |
| `black_pt00` (`black_parts_t_00`) | `./control/blyt/common_w027_chara_name.brlyt` |

::: tip
When checking vanilla files, search for the Pane name shown in parentheses.
:::

Open `MenuSingle.szs` in Switch Toolbox, inspect the target Pane, choose the desired color, update the corresponding value in `color_config.json`, and then run BetterRecolor.

