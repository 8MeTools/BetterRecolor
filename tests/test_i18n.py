import btrc.i18n as i18n


def test_t_returns_known_message_for_locale():
    original_lang = i18n.LANG
    try:
        i18n.set_locale("en")
        assert i18n.t("btrc_start") != "btrc_start"

        i18n.set_locale("ja")
        assert i18n.t("btrc_start") != "btrc_start"
    finally:
        i18n.set_locale(original_lang)


def test_t_returns_key_for_unknown_message(monkeypatch):
    original_lang = i18n.LANG
    try:
        monkeypatch.setattr(i18n, "_i18n", None)
        i18n.set_locale("en")
        assert i18n.t("unknown_test_key") == "unknown_test_key"
    finally:
        i18n.set_locale(original_lang)


def test_parse_simple_yaml_reads_basic_messages():
    text = """
# comment
en:
  hello: "Hello"
  plain: value

ja:
  hello: 'こんにちは'
"""

    assert i18n._parse_simple_yaml(text) == {
        "en": {"hello": "Hello", "plain": "value"},
        "ja": {"hello": "こんにちは"},
    }
