import argparse
import os
import shutil
import time

from btrc.config import (
    ASSETS_DIR,
    BRLAN_JSON_DIR,
    BRLYT_JSON_DIR,
    COLOR_CONFIG_PATH,
    OUTPUT_DIR,
    WUJ5_SCRIPT,
)
from btrc.brlan import select_color_rule, update_tev_colors
from btrc.brlyt import apply_tev_colors
from btrc.cleanup import move_all_files, remove_json_files
from btrc.colors import (
    confirm_apply_colors,
    load_color_settings_from_json,
    print_loaded_color_preview,
)
from btrc.encode import encode_layout_json_files
from btrc.i18n import set_locale, t
from btrc.json_io import list_layout_json_files, read_layout_json, write_layout_json
from btrc.output_bundle import write_pack_guide


def parse_args(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--lang",
        choices=("ja", "en"),
        help="Skip language selection and use the specified language.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip the confirmation prompt and run with the current settings.",
    )
    return parser.parse_args(argv)


def choose_locale(lang=None):
    if lang is None:
        choice = input("Language / 言語 (ja/en) [ja]: ").strip().lower()
        if choice not in {"ja", "en"}:
            choice = "ja"
    else:
        choice = lang
    set_locale(choice)
    return choice


def print_paths():
    print(t("using_assets_dir").format(path=ASSETS_DIR))
    print(t("using_tmp_brlyt_dir").format(path=BRLYT_JSON_DIR))
    print(t("using_tmp_brlan_dir").format(path=BRLAN_JSON_DIR))
    print(t("using_wuj5_script").format(path=WUJ5_SCRIPT))
    print(t("using_output_dir").format(path=OUTPUT_DIR))


def copy_all(src_dir, dst_dir):
    src_dir = str(src_dir)
    dst_dir = str(dst_dir)
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        dst_root = os.path.join(dst_dir, rel) if rel != "." else dst_dir
        os.makedirs(dst_root, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(dst_root, f))


def reset_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)


def main(argv=None):
    args = parse_args(argv)
    start_time = time.perf_counter()
    locale = choose_locale(args.lang)
    # print_paths()
    print(t("btrc_start"))

    color_config_path = COLOR_CONFIG_PATH

    try:
        color_map, text_free_colors, text_select_colors = load_color_settings_from_json(
            color_config_path
        )
    except (FileNotFoundError, ValueError, OSError) as e:
        print(t("color_json_load_failed").format(path=color_config_path, error=e))
        return

    print(t("color_json_load_success").format(path=color_config_path))
    print_loaded_color_preview(text_free_colors, text_select_colors)
    if not args.yes and not confirm_apply_colors():
        print(t("operation_cancelled"))
        return

    print(t("reset_tmp_and_edited"))
    reset_dir(BRLYT_JSON_DIR)
    reset_dir(BRLAN_JSON_DIR)
    reset_dir(OUTPUT_DIR)

    print(t("copy_assets_to_tmp"))
    copy_all(ASSETS_DIR / "BRLYT", BRLYT_JSON_DIR)
    copy_all(ASSETS_DIR / "BRLAN", BRLAN_JSON_DIR)

    brlyt_files = list_layout_json_files(BRLYT_JSON_DIR)
    print(t("brlyt_json_count").format(count=len(brlyt_files)))
    text_black_rgb, text_white_rgb = (text_select_colors[1], text_select_colors[0])
    arrow_black_rgb, arrow_white_rgb = color_map["color_yajirushi"]
    color_map.update(
        {
            "text": (text_black_rgb, text_white_rgb),
            "active_text": (text_black_rgb, text_white_rgb),
            "chara02": (arrow_white_rgb, arrow_black_rgb),
        }
    )

    for i, path in enumerate(brlyt_files, 1):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        new_text = apply_tev_colors(text, color_map)
        if new_text is not None:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
        if i == 1 or i % 50 == 0 or i == len(brlyt_files):
            print(
                t("brlyt_update_progress").format(
                    current=i, total=len(brlyt_files)
                )
            )

    brlan_files = list_layout_json_files(BRLAN_JSON_DIR)
    print(t("brlan_json_count").format(count=len(brlan_files)))
    for i, path in enumerate(brlan_files, 1):
        data = read_layout_json(path)
        rule = select_color_rule(path, text_free_colors, text_select_colors)
        if rule is None:
            continue
        (start_outline, start_text), (end_outline, end_text) = rule
        updated = update_tev_colors(data, start_outline, start_text, end_outline, end_text)
        write_layout_json(path, updated)
        if i == 1 or i % 50 == 0 or i == len(brlan_files):
            print(
                t("brlan_update_progress").format(
                    current=i, total=len(brlan_files)
                )
            )

    print(t("encode_json"))
    encode_layout_json_files(brlyt_files + brlan_files, WUJ5_SCRIPT)
    print(t("cleanup_json"))
    remove_json_files(brlyt_files + brlan_files)

    print(t("move_tmp_to_edited"))
    move_all_files(BRLYT_JSON_DIR, OUTPUT_DIR)
    move_all_files(BRLAN_JSON_DIR, OUTPUT_DIR)
    write_pack_guide(OUTPUT_DIR, locale)
    elapsed = time.perf_counter() - start_time
    print(t("btrc_done").format(elapsed=elapsed))


if __name__ == "__main__":
    main()
