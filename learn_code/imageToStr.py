from PIL import Image
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('file', metavar='image', help='Image wish to produce')
parser.add_argument('-o', '--output', help='output file name')
parser.add_argument('--width', type=int, default=80)
parser.add_argument('--height', type=int, default=80)

args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

# ASCII_CHAR = list("$@B%8&WM#*oahkbepqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.")
ASCII_CHAR = list("._-+=*%$&@#")


def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ASCII_CHAR)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1) / length
    return ASCII_CHAR[int(gray / unit)]


if __name__ == '__main__':
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    text = ''
    for i in range(HEIGHT):
        for j in range(WIDTH):
            text += get_char(*im.getpixel((j, i)))
        text += '\n'

    print(text)

    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(text)
    else:
        with open('output.txt', 'w') as f:
            f.write(text)