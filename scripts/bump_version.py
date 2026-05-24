import argparse
import datetime as dt
import re
import subprocess
from pathlib import Path


VERSION_PATH = Path("VERSION")
TAG_PREFIX = "v"
DATE_FMT = "%y.%m.%d"
TAG_RE = re.compile(r"^v?(?P<date>\d{2}\.\d{2}\.\d{2})\.(?P<seq>\d+)$")


def get_today_str():
    return dt.datetime.now().strftime(DATE_FMT)


def run_git(args):
    return subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )


def get_git_tags():
    try:
        result = run_git(["tag", "--list"])
    except Exception:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def read_version_file():
    if not VERSION_PATH.exists():
        return None
    return VERSION_PATH.read_text(encoding="utf-8").strip()


def next_sequence_for_date(date_str, tags, current_version):
    max_seq = 0
    for tag in tags:
        m = TAG_RE.match(tag)
        if not m:
            continue
        if m.group("date") == date_str:
            max_seq = max(max_seq, int(m.group("seq")))

    if current_version:
        m = TAG_RE.match(current_version)
        if m and m.group("date") == date_str:
            max_seq = max(max_seq, int(m.group("seq")))

    return max_seq + 1


def update_version():
    today = get_today_str()
    tags = get_git_tags()
    current_version = read_version_file()
    seq = next_sequence_for_date(today, tags, current_version)
    version = f"{today}.{seq}"

    VERSION_PATH.write_text(version + "\n", encoding="utf-8")
    return version


def create_tag(tag):
    run_git(["tag", tag])


def push(tag, remote):
    run_git(["push", remote, "HEAD"])
    run_git(["push", remote, tag])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", action="store_true", help="create git tag")
    parser.add_argument("--push", action="store_true", help="push commit and tag")
    parser.add_argument(
        "--remote",
        default="origin",
        help="git remote to push to (default: origin)",
    )
    args = parser.parse_args()

    version = update_version()
    print(f"Updated VERSION -> {version}")

    tag = f"{TAG_PREFIX}{version}"
    if args.tag:
        create_tag(tag)
        print(f"Created tag -> {tag}")
    else:
        print(f"Tag hint: {tag}")

    if args.push:
        push(tag, args.remote)
        print(f"Pushed commit and tag -> {args.remote}")


if __name__ == "__main__":
    main()
