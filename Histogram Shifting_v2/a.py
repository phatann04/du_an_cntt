import numpy as np
import cv2

# ===== Load ảnh =====
img = cv2.imread('2.jpg', 0)
if img is None:
    raise FileNotFoundError("Image not found.")

# ===== Histogram =====
hist = np.bincount(img.flatten(), minlength=256)
p = np.argmax(hist)
h = hist[p]

zeros = np.where(hist == 0)[0]

# ===== Chọn Zero =====
if zeros.size > 0:
    # Zero tự nhiên
    z = zeros[np.argmin(np.abs(zeros - p))]
    use_border = False
else:
    # Không có zero → dùng biên
    z = 255 if p < 128 else 0
    use_border = True

print(f"Peak: {p}, Zero: {z}, Capacity: {h}, Border mode: {use_border}")

embed = img.astype(np.int16).copy()

# ===== EMBEDDING =====
if not use_border:
    # ===== CASE 1: Zero tự nhiên =====
    if z > p:
        direction = +1
        mask = (embed > p) & (embed < z)
    else:
        direction = -1
        mask = (embed < p) & (embed > z)

    embed[mask] += direction

    message = np.random.randint(0, 2, h)
    flat = embed.flatten()
    pos = np.where(flat == p)[0]

    for i, idx in enumerate(pos[:h]):
        if message[i] == 1:
            flat[idx] = p + direction

    stego = flat.reshape(embed.shape).astype(np.uint8)

else:
    # ===== CASE 2: Border (0 hoặc 255) =====
    location_map = (img == z)

    if z == 255:
        mask = (embed > p)
        embed[mask] += 1

        message = np.random.randint(0, 2, h)
        flat = embed.flatten()
        pos = np.where(flat == p)[0]

        for i, idx in enumerate(pos[:h]):
            if message[i] == 1:
                flat[idx] = p + 1

    else:  # z == 0
        mask = (embed < p)
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
stego_img = cv2.imread("stego.png", 0).astype(np.int16)
flat = stego_img.flatten()
extracted_bits = []

if not use_border:
    # ===== CASE 1: Zero tự nhiên =====
    if z > p:
        direction = +1
        pos = np.where((flat == p) | (flat == p + 1))[0]

        for idx in pos[:h]:
            if flat[idx] == p:
                extracted_bits.append(0)
            else:
                extracted_bits.append(1)
            flat[idx] = p

        mask = (flat > p) & (flat <= z)
        flat[mask] -= 1

    else:
        direction = -1
        pos = np.where((flat == p) | (flat == p - 1))[0]

        for idx in pos[:h]:
            if flat[idx] == p:
                extracted_bits.append(0)
            else:
                extracted_bits.append(1)
            flat[idx] = p

        mask = (flat < p) & (flat >= z)
        flat[mask] += 1

    restored = flat.reshape(img.shape).astype(np.uint8)

else:
    # ===== CASE 2: Border =====
    if z == 255:
        pos = np.where((flat == p) | (flat == p + 1))[0]

        for idx in pos[:h]:
            if flat[idx] == p:
                extracted_bits.append(0)
            else:
                extracted_bits.append(1)
            flat[idx] = p

        mask = (flat > p)
        flat[mask] -= 1

    else:
        pos = np.where((flat == p) | (flat == p - 1))[0]

        for idx in pos[:h]:
            if flat[idx] == p:
                extracted_bits.append(0)
            else:
                extracted_bits.append(1)
            flat[idx] = p

        mask = (flat < p)
        flat[mask] += 1

    restored = flat.reshape(img.shape)
    restored[location_map] = z
    restored = restored.astype(np.uint8)

# ===== CHECK =====
print("Message correct:", np.array_equal(message, np.array(extracted_bits)))
print("Image restored:", np.array_equal(img, restored))
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim

# ===== HISTOGRAM =====
def get_hist(im):
    return np.bincount(im.flatten(), minlength=256)

hist_orig = get_hist(img)
hist_shift = get_hist(embed.astype(np.uint8))
hist_stego = get_hist(stego)
hist_restored = get_hist(restored)

plt.figure(figsize=(12, 8))

plt.subplot(2,2,1)
plt.title("Original Histogram")
plt.plot(hist_orig)

plt.subplot(2,2,2)
plt.title("Shifted Histogram")
plt.plot(hist_shift)

plt.subplot(2,2,3)
plt.title("Stego Histogram")
plt.plot(hist_stego)

plt.subplot(2,2,4)
plt.title("Restored Histogram")
plt.plot(hist_restored)

plt.tight_layout()
plt.show()


# ===== IMAGE VISUAL =====
diff_map = cv2.absdiff(img, stego)

plt.figure(figsize=(12, 8))

plt.subplot(2,2,1)
plt.title("Original")
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(2,2,2)
plt.title("Stego")
plt.imshow(stego, cmap='gray')
plt.axis('off')

plt.subplot(2,2,3)
plt.title("Restored")
plt.imshow(restored, cmap='gray')
plt.axis('off')

plt.subplot(2,2,4)
plt.title("Difference Map (|I - Stego|)")
plt.imshow(diff_map, cmap='hot')
plt.axis('off')

plt.tight_layout()
plt.show()

# ===== DIFFERENCE MAP AFTER RESTORE =====
diff_restore = cv2.absdiff(img, restored)

plt.figure(figsize=(10, 4))

plt.subplot(1,2,1)
plt.title("Difference (Original vs Stego)")
plt.imshow(diff_map, cmap='hot')
plt.axis('off')

plt.subplot(1,2,2)
plt.title("Difference (Original vs Restored)")
plt.imshow(diff_restore, cmap='hot')
plt.axis('off')

plt.tight_layout()
plt.show()


# ===== METRICS =====
def compute_mse(a, b):
    return np.mean((a.astype(np.float32) - b.astype(np.float32)) ** 2)

def compute_psnr(a, b):
    mse = compute_mse(a, b)
    if mse == 0:
        return float('inf')
    return 10 * np.log10((255**2) / mse)

mse_val = compute_mse(img, stego)
psnr_val = compute_psnr(img, stego)
ssim_val = ssim(img, stego)

capacity = h
bpp = capacity / (img.shape[0] * img.shape[1])

print("\n===== METRICS =====")
print(f"MSE (sau nhúng): {mse_val:.4f}")
print(f"PSNR (sau nhúng): {psnr_val:.4f} dB")
print(f"SSIM (sau nhúng): {ssim_val:.6f}")
print(f"Capacity: {capacity} bits")
print(f"BPP: {bpp:.6f}")