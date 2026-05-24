from pathlib import Path

from btrc.json_io import (
    list_json_files,
    list_layout_json_files,
    read_json,
    read_layout_json,
    write_json,
    write_layout_json,
)


def test_list_layout_json_files_finds_json_and_json5_recursively(tmp_path):
    root = tmp_path / "root"
    nested = root / "nested"
    nested.mkdir(parents=True)
    json_file = root / "layout.brlyt.json"
    json5_file = nested / "anim.brlan.json5"
    ignored_file = nested / "layout.brlyt"
    json_file.write_text("{}", encoding="utf-8")
    json5_file.write_text("{}", encoding="utf-8")
    ignored_file.write_text("ignored", encoding="utf-8")

    files = {Path(path).name for path in list_layout_json_files(root)}

    assert files == {"layout.brlyt.json", "anim.brlan.json5"}


def test_read_layout_json_reads_standard_json(tmp_path):
    path = tmp_path / "data.json"
    path.write_text('{"name": "text", "value": 1}', encoding="utf-8")

    assert read_layout_json(path) == {"name": "text", "value": 1}


def test_read_layout_json_reads_json5_features(tmp_path):
    path = tmp_path / "data.json5"
    path.write_text(
        """
        {
          // json5 comment
          name: "text",
          values: [1, 2,],
        }
        """,
        encoding="utf-8",
    )

    assert read_layout_json(path) == {"name": "text", "values": [1, 2]}


def test_write_layout_json_round_trips_standard_json(tmp_path):
    path = tmp_path / "data.json"
    data = {"name": "text", "value": "日本語"}

    write_layout_json(path, data)

    assert read_layout_json(path) == data
    assert "日本語" in path.read_text(encoding="utf-8")


def test_write_layout_json_round_trips_json5(tmp_path):
    path = tmp_path / "data.json5"
    data = {"name": "text", "value": 1}

    write_layout_json(path, data)

    assert read_layout_json(path) == data


def test_json_aliases_point_to_layout_json_functions():
    assert list_json_files is list_layout_json_files
    assert read_json is read_layout_json
    assert write_json is write_layout_json
