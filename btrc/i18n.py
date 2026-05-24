from pathlib import Path

try:
    import i18n as _i18n
except Exception:
    _i18n = None

_I18N_DIR = Path(__file__).resolve().parent / "i18n"
_I18N_NAMESPACE = "message"


def _parse_simple_yaml(text: str):
    data = {}
    current_lang = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0 and stripped.endswith(":"):
            current_lang = stripped[:-1].strip()
            data.setdefault(current_lang, {})
            continue
        if current_lang is None or indent < 2 or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and (
            (value[0] == '"' and value[-1] == '"')
            or (value[0] == "'" and value[-1] == "'")
        ):
            value = value[1:-1]
        data[current_lang][key.strip()] = value
    return data


def _load_yaml(path: Path):
    try:
        import yaml  # type: ignore

        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        try:
            return _parse_simple_yaml(path.read_text(encoding="utf-8"))
        except Exception:
            return None


def _load_messages():
    messages = {}
    if not _I18N_DIR.exists():
        return messages
    for path in sorted(
        list(_I18N_DIR.glob("message.*.yml"))
        + list(_I18N_DIR.glob("message.*.yaml"))
    ):
        data = _load_yaml(path)
        if not isinstance(data, dict):
            continue
        for lang, entries in data.items():
            if isinstance(entries, dict):
                lang_messages = messages.setdefault(str(lang), {})
                for key, value in entries.items():
                    lang_messages[str(key)] = str(value)
    return messages


MESSAGES = _load_messages()
LANG = "ja"

if _i18n is not None:
    _i18n.load_path.append(str(_I18N_DIR))
    _i18n.set("filename_format", "{namespace}.{locale}.{format}")
    _i18n.set("file_format", "yml")
    _i18n.set("locale", LANG)
    try:
        _i18n.load_everything()
    except Exception:
        pass


def set_locale(locale: str):
    global LANG
    LANG = locale
    if _i18n is not None:
        _i18n.set("locale", locale)
        try:
            _i18n.load_everything()
        except Exception:
            pass


def t(key: str):
    if _i18n is not None:
        try:
            lookup = key
            if not key.startswith(f"{_I18N_NAMESPACE}."):
                lookup = f"{_I18N_NAMESPACE}.{key}"
            return _i18n.t(lookup)
        except Exception:
            pass
    return MESSAGES.get(LANG, {}).get(key, key)
