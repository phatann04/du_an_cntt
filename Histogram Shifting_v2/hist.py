import numpy as np
import cv2
from matplotlib import pyplot as plt

# ===== Load ảnh =====
img = cv2.imread('6.jpg', 0)
if img is None:
    raise FileNotFoundError("Image not found. Check path/filename or working directory.")

# ===== Histogram ====
hist = np.bincount(img.flatten(), minlength=256)

p = np.argmax(hist)
h = hist[p]

# tìm zero gần nhất (trái hoặc phải)
zeros = np.where(hist == 0)[0]
if zeros.size == 0:
    raise ValueError("Algorithm requires at least one zero-count histogram bin. Use a different image or preprocess it.")
else:
    z = zeros[np.argmin(np.abs(zeros - p))]

print("Peak:", p, "Zero:", z, "Capacity:", h)

embed = img.astype(np.int16).copy()

# ===== CASE 1: zero bên phải =====
if z > p:
    mask = (embed > p) & (embed < z)
    embed[mask] += 1

    message = np.random.randint(0, 2, h)
    flat = embed.flatten()
    pos = np.where(flat == p)[0]

    for i, idx in enumerate(pos[:h]):
        if message[i] == 1:
            flat[idx] = p + 1

    stego = flat.reshape(embed.shape).astype(np.uint8)

# ===== CASE 2: zero bên trái =====
else:
    mask = (embed < p) & (embed > z)
    embed[mask] -= 1

    message = np.random.randint(0, 2, h)
    flat = embed.flatten()
    pos = np.where(flat == p)[0]

    for i, idx in enumerate(pos[:h]):
        if message[i] == 1:
            flat[idx] = p - 1

    stego = flat.reshape(embed.shape).astype(np.uint8)

cv2.imwrite("stego.png", stego)

# ===== EXTRACT + RESTORE =====
img2 = cv2.imread("stego.png", 0).astype(np.int16)
flat2 = img2.flatten()

arr = []

if z > p:
    pos = np.where((flat2 == p) | (flat2 == p+1))[0]

    for idx in pos[:h]:
        if flat2[idx] == p:
            arr.append(0)
        else:
            arr.append(1)
            flat2[idx] = p

    mask = (flat2 > p+1) & (flat2 <= z)
    flat2[mask] -= 1

else:
    pos = np.where((flat2 == p) | (flat2 == p-1))[0]

    for idx in pos[:h]:
        if flat2[idx] == p:
            arr.append(0)
        else:
            arr.append(1)
            flat2[idx] = p

    mask = (flat2 < p-1) & (flat2 >= z)
    flat2[mask] += 1

restored = flat2.reshape(img2.shape).astype(np.uint8)

# ===== CHECK =====
print("Message correct:", np.array_equal(message, np.array(arr)))
print("Image restored:", np.array_equal(img, restored))
