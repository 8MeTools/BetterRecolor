from pathlib import Path


PACK_GUIDE_FILENAME = "pack-guide.txt"

_TEMPLATE_DIR = Path(__file__).resolve().parent / "output_templates"
_DEFAULT_LOCALE = "ja"


def read_pack_guide(locale: str) -> str:
    template_path = _TEMPLATE_DIR / f"pack-guide.{locale}.txt"
    if not template_path.exists():
        template_path = _TEMPLATE_DIR / f"pack-guide.{_DEFAULT_LOCALE}.txt"
    return template_path.read_text(encoding="utf-8")


def write_pack_guide(output_dir, locale: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    guide_path = output_dir / PACK_GUIDE_FILENAME
    guide_path.write_text(read_pack_guide(locale), encoding="utf-8")
    return str(guide_path)
