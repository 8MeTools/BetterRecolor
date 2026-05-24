from btrc.cleanup import move_all_files, remove_json_files


def test_move_all_files_merges_existing_directories(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    (src / "Title.d" / "brlan").mkdir(parents=True)
    (dst / "Title.d" / "brlyt").mkdir(parents=True)
    (src / "Title.d" / "brlan" / "anim.brlan").write_text(
        "brlan", encoding="utf-8"
    )
    (dst / "Title.d" / "brlyt" / "layout.brlyt").write_text(
        "brlyt", encoding="utf-8"
    )

    move_all_files(src, dst)

    assert not (src / "Title.d").exists()
    assert (dst / "Title.d" / "brlan" / "anim.brlan").read_text(
        encoding="utf-8"
    ) == "brlan"
    assert (dst / "Title.d" / "brlyt" / "layout.brlyt").read_text(
        encoding="utf-8"
    ) == "brlyt"


def test_remove_json_files_removes_only_given_files(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    other = tmp_path / "other.txt"
    first.write_text("{}", encoding="utf-8")
    second.write_text("{}", encoding="utf-8")
    other.write_text("keep", encoding="utf-8")

    remove_json_files([first, second])

    assert not first.exists()
    assert not second.exists()
    assert other.exists()


def test_move_all_files_overwrites_existing_file(tmp_path):
    src = tmp_path / "src"
    dst = tmp_path / "dst"
    src.mkdir()
    dst.mkdir()
    (src / "same.txt").write_text("new", encoding="utf-8")
    (dst / "same.txt").write_text("old", encoding="utf-8")

    move_all_files(src, dst)

    assert (dst / "same.txt").read_text(encoding="utf-8") == "new"
    assert not (src / "same.txt").exists()
