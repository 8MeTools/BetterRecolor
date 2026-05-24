def update_tev_colors(data, start_outline, start_text, end_outline, end_text):
    for section in data.get("sections", []):
        for content in section.get("contents", []):
            if content.get("name") != "text":
                continue
            for animation in content.get("animations", []):
                for target in animation.get("targets", []):
                    kind = target.get("kind", "")
                    if not kind.startswith("tev color"):
                        continue
                    color_type = kind.split()[2]
                    component = kind.split()[-1]

                    for key in target.get("keys", []):
                        if start_outline == end_outline and start_text == end_text:
                            color = start_text if color_type == "0" else start_outline
                        else:
                            color = (
                                start_text if (color_type == "0" and key["frame"] == 0.0)
                                else end_text if (color_type == "0")
                                else start_outline
                                if (color_type == "1" and key["frame"] == 0.0)
                                else end_outline
                            )
                        if component == "r":
                            key["value"] = color[0]
                        elif component == "g":
                            key["value"] = color[1]
                        elif component == "b":
                            key["value"] = color[2]
    return data


def select_color_rule(filename, text_free_colors, text_select_colors):
    name = filename.lower()
    if "free_to_select" in name:
        return text_free_colors, text_select_colors
    if "select_to_free" in name:
        return text_select_colors, text_free_colors
    if "free" in name and "select" not in name:
        return (text_free_colors, text_free_colors)
    if "select" in name and "free" not in name:
        return (text_select_colors, text_select_colors)
    if "stop" in name:
        return (text_select_colors, text_select_colors)
    if "common_w098_wifi_menu_text" in name:
        return (text_select_colors, text_select_colors)
    if "common_w010_cup_fuchi_off" in name or "common_w010_cup_fuchi_on_to_off" in name:
        return (text_select_colors, text_select_colors)
    # 本来は"free"として扱われるべきだが、名前にファイル名に"mii_select"が含まれているために一般的な条件に当てはまらないために
    # 例外的に"free"の色を適用するように個別で条件を追加している.
    if "common_w014_mii_select_long_btn_free" in name:
        return (text_free_colors, text_free_colors)
    if "fuchi_check_loop" in name:
        return None
    return None
