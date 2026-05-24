import json

import pytest

from btrc.colors import (
    build_color_map_from_presets,
    color_presets,
    confirm_apply_colors,
    hex_to_rgb,
    load_color_settings_from_json,
    print_loaded_color_preview,
    propagate_dependent_presets,
    rgb_to_hex,
)


@pytest.fixture
def restore_presets():
    backup = {k: dict(v) for k, v in color_presets.items()}
    try:
        yield
    finally:
        color_presets.clear()
        color_presets.update({k: dict(v) for k, v in backup.items()})


def write_config(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


def test_load_color_settings_from_json_success(tmp_path, restore_presets):
    config_path = tmp_path / "color_config.json"
    write_config(
        config_path,
        {
            "presets": {
                "fuchi_pattern2": {"white": "#010203", "black": "#A0B0C0"},
                "color_base2": {"white": "#111111", "black": "#222222"},
                "color_yajirushi": {"white": "#333333", "black": "#444444"},
                "ability_graph2": {"white": "#555555", "black": "#666666"},
                "black_pt00": {"white": "#777777", "black": "#888888"},
            },
            "outline": {"free": "#123456", "select": "#654321"},
        },
    )

    color_map, text_free_colors, text_select_colors = load_color_settings_from_json(
        config_path
    )

    assert color_map["fuchi_pattern2"] == ((160, 176, 192), (1, 2, 3))
    assert color_map["black_base2"] == ((34, 34, 34), (17, 17, 17))
    assert color_map["black_pt01"] == ((136, 136, 136), (119, 119, 119))
    assert text_free_colors == ((220, 220, 220), (18, 52, 86))
    assert text_select_colors == ((255, 255, 255), (101, 67, 33))


def test_load_color_settings_from_json_missing_key(tmp_path, restore_presets):
    config_path = tmp_path / "color_config.json"
    write_config(config_path, {"presets": {}})

    with pytest.raises(ValueError):
        load_color_settings_from_json(config_path)


def test_load_color_settings_from_json_invalid_hex(tmp_path, restore_presets):
    config_path = tmp_path / "color_config.json"
    write_config(
        config_path,
        {
            "presets": {
                "fuchi_pattern2": {"white": "#000000", "black": "#FFFFFF"},
                "color_base2": {"white": "#434343", "black": "#434343"},
                "color_yajirushi": {"white": "#C8C8C8", "black": "#FFFFFF"},
                "ability_graph2": {"white": "#434343", "black": "#000000"},
                "black_pt00": {"white": "#434343", "black": "ZZZZZZ"},
            },
            "outline": {"free": "#282828", "select": "#787878"},
        },
    )

    with pytest.raises(ValueError):
        load_color_settings_from_json(config_path)


def test_load_color_settings_from_json_not_found(tmp_path, restore_presets):
    with pytest.raises(FileNotFoundError):
        load_color_settings_from_json(tmp_path / "missing.json")


def test_hex_rgb_conversion_helpers():
    assert hex_to_rgb("#0A1B2C") == (10, 27, 44)
    assert hex_to_rgb("0A1B2C") == (10, 27, 44)
    assert rgb_to_hex(10, 27, 44) == "#0A1B2C"


def test_propagate_dependent_presets_updates_aliases(restore_presets):
    propagate_dependent_presets("color_base2", "#010203", "#A0B0C0")

    assert color_presets["black_base2"] == {"white": "#010203", "black": "#A0B0C0"}
    assert color_presets["pikapika"] == {"white": "#010203", "black": "#A0B0C0"}


def test_build_color_map_from_presets_contains_logical_aliases(restore_presets):
    color_presets["color_base2"] = {"white": "#010203", "black": "#A0B0C0"}

    color_map = build_color_map_from_presets()

    assert color_map["color_base2"] == ((160, 176, 192), (1, 2, 3))
    assert color_map["black_base2"] == ((160, 176, 192), (1, 2, 3))
    assert color_map["pikapika"] == ((160, 176, 192), (1, 2, 3))


def test_print_loaded_color_preview_outputs_presets(monkeypatch, restore_presets):
    printed = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(args))

    print_loaded_color_preview(
        text_free_colors=((220, 220, 220), (1, 2, 3)),
        text_select_colors=((255, 255, 255), (4, 5, 6)),
    )

    output = "\n".join(str(args[0]) for args in printed)
    assert "fuchi_pattern2" in output
    assert "free" in output
    assert "select" in output


@pytest.mark.parametrize("answer", ["y", "yes"])
def test_confirm_apply_colors_yes(monkeypatch, answer):
    monkeypatch.setattr("builtins.input", lambda _: answer)
    assert confirm_apply_colors() is True


@pytest.mark.parametrize("answer", ["n", "no", ""])
def test_confirm_apply_colors_no(monkeypatch, answer):
    monkeypatch.setattr("builtins.input", lambda _: answer)
    assert confirm_apply_colors() is False


def test_confirm_apply_colors_invalid_then_yes(monkeypatch):
    responses = iter(["maybe", "sure", "y"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    printed = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(args))
    assert confirm_apply_colors() is True
    assert len(printed) == 2


def test_confirm_apply_colors_invalid_then_no(monkeypatch):
    responses = iter(["what", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(responses))
    printed = []
    monkeypatch.setattr("builtins.print", lambda *args, **kwargs: printed.append(args))
    assert confirm_apply_colors() is False
    assert len(printed) == 1
