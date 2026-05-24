from pathlib import Path

import json5
import pytest

from btrc.brlan import select_color_rule, update_tev_colors


def build_sample_data():
    return {
        "sections": [
            {
                "contents": [
                    {
                        "name": "text",
                        "animations": [
                            {
                                "targets": [
                                    {
                                        "kind": "tev color 0 r",
                                        "keys": [
                                            {"frame": 0.0, "value": 0},
                                            {"frame": 1.0, "value": 0},
                                        ],
                                    },
                                    {
                                        "kind": "tev color 1 r",
                                        "keys": [
                                            {"frame": 0.0, "value": 0},
                                            {"frame": 1.0, "value": 0},
                                        ],
                                    },
                                ]
                            }
                        ],
                    }
                ]
            }
        ]
    }


def test_update_tev_colors_start_and_end():
    data = build_sample_data()
    start_outline = (9, 9, 9)
    start_text = (1, 1, 1)
    end_outline = (8, 8, 8)
    end_text = (2, 2, 2)

    updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)
    targets = updated["sections"][0]["contents"][0]["animations"][0]["targets"]

    tev0 = next(t for t in targets if t["kind"] == "tev color 0 r")
    tev1 = next(t for t in targets if t["kind"] == "tev color 1 r")

    assert tev0["keys"][0]["value"] == start_text[0]
    assert tev0["keys"][1]["value"] == end_text[0]
    assert tev1["keys"][0]["value"] == start_outline[0]
    assert tev1["keys"][1]["value"] == end_outline[0]


def test_update_tev_colors_updates_rgb_and_leaves_alpha():
    data = {
        "sections": [
            {
                "contents": [
                    {
                        "name": "text",
                        "animations": [
                            {
                                "targets": [
                                    {
                                        "kind": f"tev color {color_type} {component}",
                                        "keys": [
                                            {"frame": 0.0, "value": 0},
                                            {"frame": 1.0, "value": 0},
                                        ],
                                    }
                                    for color_type in ("0", "1")
                                    for component in ("r", "g", "b", "a")
                                ]
                            }
                        ],
                    }
                ]
            }
        ]
    }

    updated = update_tev_colors(
        data,
        start_outline=(10, 20, 30),
        start_text=(1, 2, 3),
        end_outline=(40, 50, 60),
        end_text=(4, 5, 6),
    )
    targets = {
        target["kind"]: target["keys"]
        for target in updated["sections"][0]["contents"][0]["animations"][0]["targets"]
    }

    assert [key["value"] for key in targets["tev color 0 r"]] == [1, 4]
    assert [key["value"] for key in targets["tev color 0 g"]] == [2, 5]
    assert [key["value"] for key in targets["tev color 0 b"]] == [3, 6]
    assert [key["value"] for key in targets["tev color 1 r"]] == [10, 40]
    assert [key["value"] for key in targets["tev color 1 g"]] == [20, 50]
    assert [key["value"] for key in targets["tev color 1 b"]] == [30, 60]
    assert [key["value"] for key in targets["tev color 0 a"]] == [0, 0]
    assert [key["value"] for key in targets["tev color 1 a"]] == [0, 0]


def test_update_tev_colors_ignores_non_text_content():
    data = {
        "sections": [
            {
                "contents": [
                    {
                        "name": "icon",
                        "animations": [
                            {
                                "targets": [
                                    {
                                        "kind": "tev color 0 r",
                                        "keys": [{"frame": 0.0, "value": 99}],
                                    }
                                ]
                            }
                        ],
                    }
                ]
            }
        ]
    }

    updated = update_tev_colors(data, (1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4))

    target = updated["sections"][0]["contents"][0]["animations"][0]["targets"][0]
    assert target["keys"][0]["value"] == 99


def test_update_tev_colors_handles_missing_containers():
    assert update_tev_colors({}, (1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4)) == {}
    assert update_tev_colors(
        {"sections": [{"contents": [{"name": "text"}]}]},
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 4),
    ) == {"sections": [{"contents": [{"name": "text"}]}]}


def test_select_color_rule_variants():
    free = ((1, 1, 1), (2, 2, 2))
    select = ((3, 3, 3), (4, 4, 4))

    assert select_color_rule("abc_free_to_select.json5", free, select) == (free, select)
    assert select_color_rule("abc_select_to_free.json5", free, select) == (select, free)
    assert select_color_rule("abc_free.json5", free, select) == (free, free)
    assert select_color_rule("abc_select.json5", free, select) == (select, select)
    assert select_color_rule("fuchi_check_loop.json5", free, select) is None


def test_select_color_rule_w014_mii_select_returns_free_colors():
    free = ((1, 1, 1), (2, 2, 2))
    select = ((3, 3, 3), (4, 4, 4))

    assert (
        select_color_rule("common_w014_mii_select_long_btn_free.brlan.json5", free, select)
        == (free, free)
    )


@pytest.mark.parametrize(
    "filename",
    [
        "common_w004_menu_text_light_02_stop.brlan.json",
        "common_w098_wifi_menu_text_online.brlan.json",
        "common_w010_cup_fuchi_off.brlan.json",
        "common_w010_cup_fuchi_on_to_off.brlan.json",
    ],
)
def test_select_color_rule_select_color_exceptions(filename):
    free = ((1, 1, 1), (2, 2, 2))
    select = ((3, 3, 3), (4, 4, 4))

    assert select_color_rule(filename, free, select) == (select, select)


def test_update_tev_colors_uses_single_color_when_start_and_end_are_equal():
    # Use keys without a 'frame' field to expose the regression:
    # the unfixed implementation accessed key["frame"] unconditionally, raising KeyError.
    # The fix skips the frame check entirely when start == end.
    data = {
        "sections": [
            {
                "contents": [
                    {
                        "name": "text",
                        "animations": [
                            {
                                "targets": [
                                    {
                                        "kind": "tev color 0 r",
                                        "keys": [{"value": 99}],
                                    },
                                    {
                                        "kind": "tev color 1 r",
                                        "keys": [{"value": 99}],
                                    },
                                ]
                            }
                        ],
                    }
                ]
            }
        ]
    }
    color_outline = (7, 8, 9)
    color_text = (1, 2, 3)

    updated = update_tev_colors(data, color_outline, color_text, color_outline, color_text)
    targets = updated["sections"][0]["contents"][0]["animations"][0]["targets"]

    tev0 = next(t for t in targets if t["kind"] == "tev color 0 r")
    tev1 = next(t for t in targets if t["kind"] == "tev color 1 r")

    assert tev0["keys"][0]["value"] == color_text[0]
    assert tev1["keys"][0]["value"] == color_outline[0]


def test_update_tev_colors_real_data():
    data_path = Path(
        "Assets/BRLAN/Channel.d/button/anim/common_w004_menu_text_light_02_select.brlan.json5"
    )
    if not data_path.exists():
        pytest.skip("Sample BRLAN data not found")

    data = json5.loads(data_path.read_text(encoding="utf-8"))
    start_outline = (11, 12, 13)
    start_text = (21, 22, 23)
    end_outline = (31, 32, 33)
    end_text = (41, 42, 43)

    updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)

    for section in updated.get("sections", []):
        for content in section.get("contents", []):
            if content.get("name") != "text":
                continue
            for animation in content.get("animations", []):
                for target in animation.get("targets", []):
                    kind = target.get("kind", "")
                    if not kind.startswith("tev color"):
                        continue
                    parts = kind.split()
                    if len(parts) < 3 or parts[-1] != "r":
                        continue
                    color_type = parts[2]
                    keys = target.get("keys", [])
                    key0 = next((k for k in keys if k.get("frame") == 0.0), None)
                    key1 = next((k for k in keys if k.get("frame") != 0.0), None)
                    if not key0 or not key1:
                        continue

                    if color_type == "0":
                        assert key0["value"] == start_text[0]
                        assert key1["value"] == end_text[0]
                    elif color_type == "1":
                        assert key0["value"] == start_outline[0]
                        assert key1["value"] == end_outline[0]
                    return

    pytest.skip("No suitable tev color target with frame 0.0 and non-0.0 found")
