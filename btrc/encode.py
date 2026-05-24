import time

from .i18n import t
from wuj5.api import encode_file


def _empty_timing():
    return {
        "count": 0,
        "input_bytes": 0,
        "output_bytes": 0,
        "read": 0.0,
        "parse": 0.0,
        "pack": 0.0,
        "write": 0.0,
        "total": 0.0,
    }


def _add_timing(target, timing):
    target["count"] += 1
    target["input_bytes"] += timing["input_bytes"]
    target["output_bytes"] += timing["output_bytes"]
    target["read"] += timing["read"]
    target["parse"] += timing["parse"]
    target["pack"] += timing["pack"]
    target["write"] += timing["write"]
    target["total"] += timing["total"]


def _print_timing(label, timing):
    if timing["count"] == 0:
        return
    avg = timing["total"] / timing["count"]
    print(
        f"{label}: {timing['count']} files, "
        f"total={timing['total']:.2f}s, avg={avg:.4f}s/file, "
        f"read={timing['read']:.2f}s, parse={timing['parse']:.2f}s, "
        f"pack={timing['pack']:.2f}s, write={timing['write']:.2f}s"
    )


def _print_slowest_files(timings, limit=5):
    slowest = sorted(timings, key=lambda item: item["total"], reverse=True)[:limit]
    if not slowest:
        return
    print("Slowest encode files:")
    for timing in slowest:
        print(
            f"  {timing['total']:.4f}s "
            f"(parse={timing['parse']:.4f}s, pack={timing['pack']:.4f}s) "
            f"{timing['path']}"
        )


def encode_layout_json_files(files, wuj5_script):
    if not files:
        print(t("no_json"))
        return {"count": 0, "failed": 0, "elapsed": 0.0, "timings": []}
    start = time.perf_counter()
    failed = 0
    timings = []
    by_ext = {}
    for file_path in files:
        try:
            timing = encode_file(file_path, profile=True)
            if timing is not None:
                timings.append(timing)
                _add_timing(by_ext.setdefault(timing["ext"], _empty_timing()), timing)
        except Exception as e:
            failed += 1
            print(f"エラー: {file_path}")
            print(e)
    elapsed = time.perf_counter() - start
    total_timing = _empty_timing()
    for timing in timings:
        _add_timing(total_timing, timing)
    _print_timing("Encode total", total_timing)
    for ext in sorted(by_ext):
        _print_timing(f"Encode {ext.upper()}", by_ext[ext])
    _print_slowest_files(timings)
    print(t("done_encode"))
    return {
        "count": len(files),
        "failed": failed,
        "elapsed": elapsed,
        "timings": timings,
        "by_ext": by_ext,
    }


encode_json_files = encode_layout_json_files
