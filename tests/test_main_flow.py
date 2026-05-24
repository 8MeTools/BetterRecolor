import builtins

import main as app


def test_choose_locale_defaults_to_ja_for_unknown_input(monkeypatch):
    selected = []
    monkeypatch.setattr(builtins, "input", lambda _: "xx")
    monkeypatch.setattr(app, "set_locale", lambda locale: selected.append(locale))

    assert app.choose_locale() == "ja"
    assert selected == ["ja"]


def test_copy_all_preserves_nested_structure(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "Title.d" / "button").mkdir(parents=True)
    (src / "Title.d" / "button" / "layout.json").write_text("data", encoding="utf-8")

    app.copy_all(src, dst)

    assert (dst / "Title.d" / "button" / "layout.json").read_text(
        encoding="utf-8"
    ) == "data"


def test_reset_dir_recreates_empty_directory(tmp_path):
    path = tmp_path / "work"
    path.mkdir()
    (path / "old.txt").write_text("old", encoding="utf-8")

    app.reset_dir(path)

    assert path.is_dir()
    assert list(path.iterdir()) == []


def test_write_pack_guide_creates_japanese_user_guide(tmp_path):
    guide_path = app.write_pack_guide(tmp_path, "ja")

    assert guide_path == str(tmp_path / app.PACK_GUIDE_FILENAME)
    guide_text = (tmp_path / app.PACK_GUIDE_FILENAME).read_text(encoding="utf-8")
    assert "日本語" in guide_text


def test_write_pack_guide_creates_english_user_guide(tmp_path):
    guide_path = app.write_pack_guide(tmp_path, "en")

    assert guide_path == str(tmp_path / app.PACK_GUIDE_FILENAME)
    guide_text = (tmp_path / app.PACK_GUIDE_FILENAME).read_text(encoding="utf-8")
    assert "English" in guide_text


def test_write_pack_guide_falls_back_to_japanese_for_unknown_locale(tmp_path):
    app.write_pack_guide(tmp_path, "unknown")

    guide_text = (tmp_path / app.PACK_GUIDE_FILENAME).read_text(encoding="utf-8")
    assert "日本語" in guide_text


def test_main_returns_before_side_effects_when_color_config_fails(monkeypatch):
    events = []
    def fake_choose_locale():
        events.append("locale")
        return "en"

    monkeypatch.setattr(app, "choose_locale", fake_choose_locale)
    monkeypatch.setattr(
        app,
        "load_color_settings_from_json",
        lambda path: (_ for _ in ()).throw(ValueError("bad config")),
    )
    monkeypatch.setattr(app, "reset_dir", lambda path: events.append("reset"))
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)

    app.main()

    assert events == ["locale"]


def test_main_returns_before_file_work_when_user_cancels(monkeypatch):
    events = []
    def fake_choose_locale():
        events.append("locale")
        return "en"

    monkeypatch.setattr(app, "choose_locale", fake_choose_locale)
    monkeypatch.setattr(
        app,
        "load_color_settings_from_json",
        lambda path: ({}, ((1, 1, 1), (2, 2, 2)), ((3, 3, 3), (4, 4, 4))),
    )
    monkeypatch.setattr(app, "print_loaded_color_preview", lambda *args: events.append("preview"))
    monkeypatch.setattr(app, "confirm_apply_colors", lambda: False)
    monkeypatch.setattr(app, "reset_dir", lambda path: events.append("reset"))
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)

    app.main()

    assert events == ["locale", "preview"]


def test_main_happy_path_calls_major_steps_in_order(monkeypatch, tmp_path):
    events = []
    brlyt_path = tmp_path / "layout.brlyt.json"
    brlan_path = tmp_path / "anim.brlan.json"
    brlyt_path.write_text('{"name": "text"}', encoding="utf-8")

    def fake_reset_dir(path):
        events.append("reset")

    def fake_copy_all(src, dst):
        events.append("copy")

    def fake_list_layout_json_files(root):
        if len([event for event in events if event == "list"]) == 0:
            events.append("list")
            return [brlyt_path]
        events.append("list")
        return [brlan_path]

    def fake_apply_tev_colors(text, color_map):
        events.append("brlyt")
        return text

    def fake_read_layout_json(path):
        events.append("read_brlan")
        return {"sections": []}

    def fake_select_color_rule(path, free, select):
        events.append("rule")
        return free, select

    def fake_update_tev_colors(data, *args):
        events.append("brlan")
        return data

    def fake_write_layout_json(path, data):
        events.append("write_brlan")

    def fake_choose_locale():
        events.append("locale")
        return "en"

    monkeypatch.setattr(app, "choose_locale", fake_choose_locale)
    monkeypatch.setattr(
        app,
        "load_color_settings_from_json",
        lambda path: (
            {"color_yajirushi": ((5, 5, 5), (6, 6, 6))},
            ((1, 1, 1), (2, 2, 2)),
            ((3, 3, 3), (4, 4, 4)),
        ),
    )
    monkeypatch.setattr(app, "print_loaded_color_preview", lambda *args: events.append("preview"))
    monkeypatch.setattr(app, "confirm_apply_colors", lambda: True)
    monkeypatch.setattr(app, "reset_dir", fake_reset_dir)
    monkeypatch.setattr(app, "copy_all", fake_copy_all)
    monkeypatch.setattr(app, "list_layout_json_files", fake_list_layout_json_files)
    monkeypatch.setattr(app, "apply_tev_colors", fake_apply_tev_colors)
    monkeypatch.setattr(app, "read_layout_json", fake_read_layout_json)
    monkeypatch.setattr(app, "select_color_rule", fake_select_color_rule)
    monkeypatch.setattr(app, "update_tev_colors", fake_update_tev_colors)
    monkeypatch.setattr(app, "write_layout_json", fake_write_layout_json)
    monkeypatch.setattr(app, "encode_layout_json_files", lambda files, script: events.append("encode"))
    monkeypatch.setattr(app, "remove_json_files", lambda files: events.append("cleanup"))
    monkeypatch.setattr(app, "move_all_files", lambda src, dst: events.append("move"))
    monkeypatch.setattr(app, "write_pack_guide", lambda output, locale: events.append(f"guide:{locale}"))
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)

    app.main()

    assert events == [
        "locale",
        "preview",
        "reset",
        "reset",
        "reset",
        "copy",
        "copy",
        "list",
        "brlyt",
        "list",
        "read_brlan",
        "rule",
        "brlan",
        "write_brlan",
        "encode",
        "cleanup",
        "move",
        "move",
        "guide:en",
    ]
