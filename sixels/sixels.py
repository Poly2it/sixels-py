from PIL import Image

def encode_image(image):
    palette_image = image.convert("P", palette=Image.ADAPTIVE, colors=256)

    pil_palette = palette_image.getpalette()
    palette = []
    for i in range(0, len(pil_palette), 3):
        palette.append(pil_palette[i:i+3])

    data = palette_image.load()

    width, height = palette_image.size

    all_modified_colors = set()

    colors_precomp = [[0 for _ in range(width)] for _ in range(len(palette))]

    # we just could check if mode is RGBA, but it's common for 
    # images without alpha values to still ship in RGBA mode
    if image.mode == 'RGBA' and image.getextrema()[3][0] < 255:
        # alpha mode
        # 9% slower at 1024x1024
        # 11% slower at 64x64
        alpha_data = image.load()
        sixels = []
        for y in range(0, height, 6):
            colors = [list(row) for row in colors_precomp]

            modified_colors = set()

            for x in range(width):
                for z in range(min(6, height - y)):
                    if not alpha_data[x, y + z][-1] < 255:
                        value = data[x, y + z]
                        colors[value][x] |= (1 << z)
                        modified_colors.add(value)

            if len(modified_colors) == 0:
                modified_colors.add(0)

            for color in modified_colors:
                all_modified_colors.add(color)

            minified_palette = [[index, color] for index, color in enumerate(colors) if index in modified_colors]

            for index, (palette_index, color) in enumerate(minified_palette):
                sixels.append("#" + repr(palette_index) + "".join(chr(63 + item) for item in color) + ("-" if index == len(minified_palette) - 1 else "$"))
    else:
        # non-alpha mode

        sixels = []
        for y in range(0, height, 6):
            colors = [list(row) for row in colors_precomp]

            modified_colors = set()

            for x in range(width):
                for z in range(min(6, height - y)):
                    value = data[x, y + z]
                    colors[value][x] |= (1 << z)
                    modified_colors.add(value)

            for color in modified_colors:
                all_modified_colors.add(color)

            minified_palette = [[index, color] for index, color in enumerate(colors) if index in modified_colors]

            for index, (palette_index, color) in enumerate(minified_palette):
                sixels.append("#" + repr(palette_index) + "".join(chr(63 + item) for item in color) + ("-" if index == len(minified_palette) - 1 else "$"))

    minified_full_palette = [color for index, color in enumerate(palette) if index in all_modified_colors]

    palette_strings = []
    for index, color in enumerate(minified_full_palette):
        palette_strings.append("".join([
            "#",
            repr(index),
            ";2;",
            repr(int(color[0] // 2.55)),
            ";",
            repr(int(color[1] // 2.55)),
            ";",
            repr(int(color[2] // 2.55))
        ]))

    sixel = "".join([
        '\x1bPq1;1;"1;1;',
        repr(width),
        ';',
        repr(height),
        '$',
        *palette_strings,
        *sixels,
        '\x1b\\'
    ])

    return sixel
