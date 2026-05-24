import re


def apply_tev_colors(json_text, color_map):
    pattern = re.compile(
        r'(\s*"name": "(fuchi_pattern2|color_base2|black_base2|pikapika|'
        r'color_yajirushi|ability_graph2|black_pt00|black_pt01|text|active_text|chara02)"'
        r'.*?("tev color 1 a": \d+))',
        re.DOTALL,
    )
    matches = list(re.finditer(pattern, json_text))
    if not matches:
        return None

    for match in reversed(matches):
        block_text = match.group(1)
        block_name = match.group(2)
        black_rgb, white_rgb = color_map.get(block_name, ((0, 0, 0), (255, 255, 255)))

        block_text = re.sub(
            r'"tev color 0 r": \d+(,?)',
            f'"tev color 0 r": {black_rgb[0]}\\1',
            block_text,
        )
        block_text = re.sub(
            r'"tev color 0 g": \d+(,?)',
            f'"tev color 0 g": {black_rgb[1]}\\1',
            block_text,
        )
        block_text = re.sub(
            r'"tev color 0 b": \d+(,?)',
            f'"tev color 0 b": {black_rgb[2]}\\1',
            block_text,
        )

        block_text = re.sub(
            r'"tev color 1 r": \d+(,?)',
            f'"tev color 1 r": {white_rgb[0]}\\1',
            block_text,
        )
        block_text = re.sub(
            r'"tev color 1 g": \d+(,?)',
            f'"tev color 1 g": {white_rgb[1]}\\1',
            block_text,
        )
        block_text = re.sub(
            r'"tev color 1 b": \d+(,?)',
            f'"tev color 1 b": {white_rgb[2]}\\1',
            block_text,
        )

        json_text = json_text[: match.start()] + block_text + json_text[match.end() :]

    return json_text
