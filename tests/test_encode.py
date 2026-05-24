import builtins

from btrc import encode


def make_timing(path, ext, total):
    return {
        "path": path,
        "ext": ext,
        "input_bytes": 10,
        "output_bytes": 20,
        "read": 0.1,
        "parse": 0.2,
        "pack": 0.3,
        "write": 0.4,
        "total": total,
    }


def test_encode_layout_json_files_empty_input(monkeypatch):
    calls = []
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: calls.append(args))

    result = encode.encode_layout_json_files([], "unused")

    assert result == {"count": 0, "failed": 0, "elapsed": 0.0, "timings": []}
    assert calls


def test_encode_layout_json_files_collects_timings_by_ext(monkeypatch):
    calls = []

    def fake_encode_file(path, profile=False):
        calls.append((path, profile))
        if str(path).endswith(".brlyt.json"):
            return make_timing(path, "brlyt", 1.0)
        return make_timing(path, "brlan", 2.0)

    monkeypatch.setattr(encode, "encode_file", fake_encode_file)
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)

    result = encode.encode_layout_json_files(
        ["first.brlyt.json", "second.brlan.json"],
        "unused",
    )

    assert calls == [
        ("first.brlyt.json", True),
        ("second.brlan.json", True),
    ]
    assert result["count"] == 2
    assert result["failed"] == 0
    assert len(result["timings"]) == 2
    assert result["by_ext"]["brlyt"]["count"] == 1
    assert result["by_ext"]["brlan"]["count"] == 1
    assert result["by_ext"]["brlan"]["total"] == 2.0


def test_encode_layout_json_files_continues_after_failure(monkeypatch):
    calls = []

    def fake_encode_file(path, profile=False):
        calls.append(path)
        if path == "bad.brlan.json":
            raise RuntimeError("encode failed")
        return make_timing(path, "brlyt", 1.0)

    monkeypatch.setattr(encode, "encode_file", fake_encode_file)
    monkeypatch.setattr(builtins, "print", lambda *args, **kwargs: None)

    result = encode.encode_layout_json_files(
        ["good.brlyt.json", "bad.brlan.json", "later.brlyt.json"],
        "unused",
    )

    assert calls == ["good.brlyt.json", "bad.brlan.json", "later.brlyt.json"]
    assert result["count"] == 3
    assert result["failed"] == 1
    assert len(result["timings"]) == 2
