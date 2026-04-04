import numpy as np


def text_to_bits(text):
    bits = []
    for ch in text:
        bits.extend([int(b) for b in format(ord(ch), '08b')])
    return bits


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int(''.join(map(str, byte)), 2)))
    return ''.join(chars)


def embed_de(image, bits):
    h, w = image.shape
    stego = image.copy()
    location_map = []
    bit_idx = 0

    for i in range(h):
        for j in range(0, w - 1, 2):
            if bit_idx >= len(bits):
                location_map.append(0)
                continue

            x, y = int(stego[i, j]), int(stego[i, j+1])

            l = (x + y) // 2
            d = x - y

            b = bits[bit_idx]
            d_new = 2 * d + b

            x_new = l + (d_new + 1)//2
            y_new = l - d_new//2

            if 0 <= x_new <= 255 and 0 <= y_new <= 255:
                stego[i, j] = x_new
                stego[i, j+1] = y_new
                location_map.append(1)
                bit_idx += 1
            else:
                location_map.append(0)

    return stego, location_map, bit_idx


def extract_de(stego, location_map, bit_len):
    h, w = stego.shape
    recovered = stego.copy()
    bits = []
    lm_idx = 0

    for i in range(h):
        for j in range(0, w - 1, 2):
            if lm_idx >= len(location_map):
                continue

            if location_map[lm_idx] == 1 and len(bits) < bit_len:
                x, y = int(stego[i, j]), int(stego[i, j+1])

                d_new = x - y
                b = d_new & 1
                d = d_new // 2
                l = (x + y)//2

                recovered[i, j] = l + (d + 1)//2
                recovered[i, j+1] = l - d//2

                bits.append(b)

            lm_idx += 1

    return recovered, bits


def psnr(img1, img2):
    mse = np.mean((img1.astype(float) - img2.astype(float))**2)
    if mse == 0:
        return 100
    return 10 * np.log10((255**2)/mse)