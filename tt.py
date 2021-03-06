import pytesseract
from PIL import Image
from collections import defaultdict

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def get_threshold(image):
    pixel_dict = defaultdict(int)

    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            pixel_dict[pixel] += 1

    # count_max = max(pixel_dict.values())
    # pixel_dict_reverse = {v: k for k, v in pixel_dict.items()}
    # threshold = pixel_dict_reverse[count_max]

    # 灰度平均值获取阈值
    # threshold = sum([k * v for k, v in pixel_dict.items()]) / (rows * cols)

    # 迭代最佳阈值

    tmax = max(map(int, pixel_dict.keys()))
    tmin = min(map(int, pixel_dict.keys()))

    t = (tmax + tmin) / 2

    t1 = -1
    while int(t) != int(t1):
        t1 = t
        tb = []
        tf = []
        for i in pixel_dict.keys():
            if int(i) < t1:
                tb.append(i)
            else:
                tf.append(i)
        tba = sum([pixel_dict[i] * int(i) for i in tb]) / sum([pixel_dict[i] for i in tb])
        tfa = sum([pixel_dict[i] * int(i) for i in tf]) / sum([pixel_dict[i] for i in tf])
        t = (tba + tfa) / 2
    threshold = t
    return threshold


def get_bin_table(threshold, rate=0.1):
    table = []
    # for i in range(256):
    #     if threshold * (1 - rate) <= i <= threshold * (1 + rate):
    #         table.append(1)
    #     else:
    #         table.append(0)
    for i in range(256):
        if i < threshold * (1 - rate):
            table.append(0)
        else:
            table.append(255)
    return table


def cut_noise(image):
    rows, cols = image.size
    change_pos = []

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            pixel_set = []
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if image.getpixel((m, n)) != 0:
                        pixel_set.append(image.getpixel((m, n)))

            if len(pixel_set) <= 5:
                change_pos.append((i, j))

    for pos in change_pos:
        image.putpixel(pos, 0)

    return image


def pic_add(image):
    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            if pixel <= 128:
                value = int(pixel * pixel / 128)
            else:
                value = int(255 - (255 - pixel) * (255 - pixel) / 128)

            image.putpixel((i, j), value)
    return image


def ave_nosie(image):
    rows, cols = image.size
    pos = []
    value = []
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            pos.append((i, j))
            val = 0
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    val += image.getpixel((m, n))
            value.append(int(val / 9))
    for i, j in zip(pos, value):
        image.putpixel(i, j)
    for i in range(cols):
        image.putpixel((0, i), 255)
        image.putpixel((rows - 1, i), 255)
    for i in range(rows):
        image.putpixel((i, 0), 255)
        image.putpixel((i, cols - 1), 255)
    return image


def OCR_lmj(img_path):
    image = Image.open(img_path)
    imgry = image.convert('L')

    max_pixel = get_threshold(imgry)

    table = get_bin_table(threshold=max_pixel, rate=0.1)
    out = imgry.point(table, '1')
    out = cut_noise(out)
    out.show()
    text = pytesseract.image_to_string(out)
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = ''.join([x for x in text if x not in exclude_char_list])

    return text


def main():
    image_path = r'F:\temp_py\captcha.jpg'
    # print(OCR_lmj(image_path))
    image = Image.open(image_path)
    imgry = image.convert('L')
    # imgry = pic_add(pic_add(pic_add(imgry)))
    imgry = ave_nosie(imgry)
    max_pixel = get_threshold(imgry)
    table = get_bin_table(threshold=max_pixel, rate=0.0)
    out = imgry.point(table, '1')
    out.save('temp.jpg')
    out = cut_noise(out)
    out.save('temp1.jpg')
    text = pytesseract.image_to_string(out, config='--psm 13')
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text1 = ''.join([x for x in text if x not in exclude_char_list])
    print(text, text1)
    image.save('temp2.jpg')
    image1 = Image.open('temp2.jpg')
    print(pytesseract.image_to_string(image1, config='--psm 13'))
    print(pytesseract.image_to_string(image, config='--psm 13'))


main()
