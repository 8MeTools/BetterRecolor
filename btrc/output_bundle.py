import shutil
from pathlib import Path


PACK_GUIDE_FILENAME = "pack-guide.txt"

_TEMPLATE_DIR = Path(__file__).resolve().parent / "output_templates"
_DEFAULT_LOCALE = "ja"


def _pack_guide_template_path(locale: str) -> Path:
    template_path = _TEMPLATE_DIR / f"pack-guide.{locale}.txt"
    if not template_path.exists():
        template_path = _TEMPLATE_DIR / f"pack-guide.{_DEFAULT_LOCALE}.txt"
    return template_path


def write_pack_guide(output_dir, locale: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    guide_path = output_dir / PACK_GUIDE_FILENAME
    shutil.copy2(_pack_guide_template_path(locale), guide_path)
    return str(guide_path)
