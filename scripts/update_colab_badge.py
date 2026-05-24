import argparse
import json
from pathlib import Path


CONFIG_PATH = Path("colab_badge.json")
NOTEBOOK_PATH = Path("BetterRecolor.ipynb")
BADGE_IMAGE_URL = "https://colab.research.google.com/assets/colab-badge.svg"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_colab_url(config):
    owner = config["github_owner"].strip("/")
    repo = config["github_repo"].strip("/")
    branch = config["github_branch"].strip("/")
    notebook_path = config["notebook_path"].strip("/")
    return (
        "https://colab.research.google.com/github/"
        f"{owner}/{repo}/blob/{branch}/{notebook_path}"
    )


def build_badge_html(colab_url):
    return (
        f'<a href="{colab_url}" target="_parent">'
        f'<img src="{BADGE_IMAGE_URL}" alt="Open In Colab"/>'
        "</a>"
    )


def update_colab_badge(notebook, badge_html):
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue

        source = cell.get("source", [])
        source_text = "".join(source)
        if BADGE_IMAGE_URL in source_text:
            cell["source"] = [badge_html]
            return True

    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default=CONFIG_PATH,
        type=Path,
        help=f"badge config path (default: {CONFIG_PATH})",
    )
    parser.add_argument(
        "--notebook",
        default=NOTEBOOK_PATH,
        type=Path,
        help=f"notebook path (default: {NOTEBOOK_PATH})",
    )
    args = parser.parse_args()

    config = read_json(args.config)
    notebook = read_json(args.notebook)
    colab_url = build_colab_url(config)
    badge_html = build_badge_html(colab_url)

    if not update_colab_badge(notebook, badge_html):
        raise RuntimeError(f"Colab badge markdown cell was not found in {args.notebook}")

    write_json(args.notebook, notebook)
    print(f"Updated Colab badge -> {colab_url}")


if __name__ == "__main__":
    main()
