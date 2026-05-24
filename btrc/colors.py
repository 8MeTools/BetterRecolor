import json
from pathlib import Path
import re
from colr import color
from .i18n import t

HEX_PATTERN = re.compile(r"^#([A-Fa-f0-9]{6})$")


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return "#%02X%02X%02X" % (r, g, b)

# 必要なプリセット
PRIMARY_PRESET_DEFAULTS = {
    "fuchi_pattern2": {"black": "#FFFFFF", "white": "#000000"},
    "color_base2": {"black": "#434343", "white": "#434343"},
    "color_yajirushi": {"black": "#FFFFFF", "white": "#C8C8C8"},
    "ability_graph2": {"black": "#000000", "white": "#434343"},
    "black_pt00": {"black": "#434343", "white": "#434343"},
}

PRIMARY_PRESET_NAMES = tuple(PRIMARY_PRESET_DEFAULTS.keys())

# 依存関係にあるプリセットは、ユーザが変更した際に同じ色を適用する。
# 例: color_base2を変更したら、black_base2とpikapikaも同じ色にする。
PRESET_DEPENDENCIES = {
    "color_base2": ("black_base2", "pikapika"),
    "black_pt00": ("black_pt01",),
}

# プレビュー表示の順番
PRESET_DISPLAY_ORDER = (
    "fuchi_pattern2",
    "color_base2",
    "black_base2",
    "pikapika",
    "color_yajirushi",
    "ability_graph2",
    "black_pt00",
    "black_pt01",
)


def _build_initial_presets():
    presets = {name: dict(values) for name, values in PRIMARY_PRESET_DEFAULTS.items()}
    for primary_name, dependent_names in PRESET_DEPENDENCIES.items():
        for dependent_name in dependent_names:
            presets[dependent_name] = dict(presets[primary_name])
    return presets


color_presets = _build_initial_presets()


def propagate_dependent_presets(primary_name, white, black):
    """Apply the same colors to presets that are defined as dependents."""
    for dependent_name in PRESET_DEPENDENCIES.get(primary_name, ()):
        if dependent_name not in color_presets:
            color_presets[dependent_name] = {"white": white, "black": black}
            continue
        color_presets[dependent_name]["white"] = white
        color_presets[dependent_name]["black"] = black


def _validate_and_normalize_hex(value, key_name):
    if not isinstance(value, str) or not HEX_PATTERN.match(value):
        raise ValueError(
            t("color_json_invalid_hex").format(key_name=key_name, value=value)
        )
    return value.upper()

# Logical color-map keys and the preset each one derives from.
# This centralizes the structure so that it can be reused without duplication.
COLOR_MAP_PRESET_SOURCES = {
    "fuchi_pattern2": "fuchi_pattern2",
    "color_base2": "color_base2",
    "black_base2": "color_base2",   # alias of color_base2
    "pikapika": "color_base2",      # alias of color_base2
    "color_yajirushi": "color_yajirushi",
    "ability_graph2": "ability_graph2",
    "black_pt00": "black_pt00",
    "black_pt01": "black_pt00",     # alias of black_pt00
}

def build_color_map_from_presets():
    color_map = {}
    for key, source_preset in COLOR_MAP_PRESET_SOURCES.items():
        black_hex = color_presets[source_preset]["black"]
        white_hex = color_presets[source_preset]["white"]
        black_rgb = hex_to_rgb(black_hex)
        white_rgb = hex_to_rgb(white_hex)
        color_map[key] = (black_rgb, white_rgb)
    return color_map

def load_color_settings_from_json(config_path):
    config_path = Path(config_path)
    if not config_path.is_file():
        raise FileNotFoundError(t("color_json_not_found").format(path=config_path))

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            t("color_json_parse_error").format(path=config_path, error=e.msg)
        ) from e
    except UnicodeDecodeError as e:
        raise ValueError(
            t("color_json_decode_error").format(path=config_path, error=e)
        ) from e

    presets = data.get("presets")
    outline = data.get("outline")
    if not isinstance(presets, dict):
        raise ValueError(t("color_json_missing_key").format(key_name="presets"))
    if not isinstance(outline, dict):
        raise ValueError(t("color_json_missing_key").format(key_name="outline"))

    for preset_name in PRIMARY_PRESET_NAMES:
        preset = presets.get(preset_name)
        if not isinstance(preset, dict):
            raise ValueError(
                t("color_json_missing_key").format(key_name=f"presets.{preset_name}")
            )
        white = _validate_and_normalize_hex(
            preset.get("white"), f"presets.{preset_name}.white"
        )
        black = _validate_and_normalize_hex(
            preset.get("black"), f"presets.{preset_name}.black"
        )
        color_presets[preset_name]["white"] = white
        color_presets[preset_name]["black"] = black
        propagate_dependent_presets(preset_name, white, black)

    free_outline_hex = _validate_and_normalize_hex(outline.get("free"), "outline.free")
    select_outline_hex = _validate_and_normalize_hex(
        outline.get("select"), "outline.select"
    )
    free_outline_rgb = hex_to_rgb(free_outline_hex)
    select_outline_rgb = hex_to_rgb(select_outline_hex)

    default_free_text = (220, 220, 220)
    default_select_text = (255, 255, 255)
    text_free_colors = (default_free_text, free_outline_rgb)
    text_select_colors = (default_select_text, select_outline_rgb)
    return build_color_map_from_presets(), text_free_colors, text_select_colors


def print_loaded_color_preview(text_free_colors, text_select_colors):
    print(t("section_loaded_color_preview"))
    for preset_name in PRESET_DISPLAY_ORDER:
        print_preset(preset_name)

    free_outline = rgb_to_hex(*text_free_colors[1])
    select_outline = rgb_to_hex(*text_select_colors[1])
    print(
        t("preview_outline").format(
            state_name="free", value=free_outline, block=color("■", fore=free_outline)
        )
    )
    print(
        t("preview_outline").format(
            state_name="select",
            value=select_outline,
            block=color("■", fore=select_outline),
        )
    )


def confirm_apply_colors():
    while True:
        choice = input(t("prompt_confirm_apply")).strip().lower()
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no", ""}:
            return False
        print(t("invalid_yes_no"))


def print_preset(name):
    preset = color_presets[name]
    print(t("preset_title").format(name=name))
    print(
        t("preset_white").format(
            value=preset["white"], block=color("■", fore=preset["white"])
        )
    )
    print(
        t("preset_black").format(
            value=preset["black"], block=color("■", fore=preset["black"])
        )
    )
