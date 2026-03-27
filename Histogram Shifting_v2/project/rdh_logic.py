import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

class RDH:
    @staticmethod
    def analyze_image(img):
        hist = np.bincount(img.flatten(), minlength=256)
        p = np.argmax(hist)
        h = hist[p]
        zeros = np.where(hist == 0)[0]

        if zeros.size > 0:
            z = zeros[np.argmin(np.abs(zeros - p))]
            use_border = False
        else:
            z = 255 if p < 128 else 0
            use_border = True
        return p, z, h, use_border

    @staticmethod
    def embed_data(img, p, z, h, use_border, bits_to_embed):
        embed = img.astype(np.int16).copy()
        
        # Chỉ lấy số lượng bit bằng đúng khả năng chứa h
        message = bits_to_embed[:h]
        if len(message) < h: # Pad thêm 0 nếu tin nhắn ngắn hơn capacity
            message = np.pad(message, (0, h - len(message)), 'constant')

        if not use_border:
            direction = 1 if z > p else -1
            mask = (embed > p) & (embed < z) if z > p else (embed < p) & (embed > z)
            embed[mask] += direction
            
            flat = embed.flatten()
            pos = np.where(flat == p)[0]
            for i, idx in enumerate(pos[:h]):
                if message[i] == 1:
                    flat[idx] = p + direction
            stego = flat.reshape(embed.shape).astype(np.uint8)
            return stego, message, None
        else:
            location_map = (img == z)
            if z == 255:
                embed[embed > p] += 1
                flat = embed.flatten()
                pos = np.where(flat == p)[0]
                for i, idx in enumerate(pos[:h]):
                    if message[i] == 1: flat[idx] = p + 1
            else:
                embed[embed < p] -= 1
                flat = embed.flatten()
                pos = np.where(flat == p)[0]
                for i, idx in enumerate(pos[:h]):
                    if message[i] == 1: flat[idx] = p - 1
            
            stego = flat.reshape(embed.shape).astype(np.uint8)
            return stego, message, location_map
        
    @staticmethod
    def extract_data(stego, p, z, h, use_border):
        flat = stego.astype(np.int16).flatten()
        extracted_bits = []
        
        # Xác định hướng dịch chuyển để lấy bit
        direction = 1 if (not use_border and z > p) or (use_border and z == 255) else -1
        
        # Tìm các vị trí chứa tin (điểm đỉnh p và điểm đã dịch chuyển p + direction)
        pos = np.where((flat == p) | (flat == p + direction))[0]

        for idx in pos[:h]:
            if flat[idx] == p:
                extracted_bits.append(0)
            else:
                extracted_bits.append(1)
            flat[idx] = p # Trả về giá trị p gốc để chuẩn bị restore ảnh
            
        return flat, np.array(extracted_bits)

    @staticmethod
    def restore_image(flat, img_shape, p, z, use_border, location_map):
        if not use_border:
            direction = 1 if z > p else -1
            if z > p:
                mask = (flat > p) & (flat <= z)
                flat[mask] -= 1
            else:
                mask = (flat < p) & (flat >= z)
                flat[mask] += 1
            restored = flat.reshape(img_shape).astype(np.uint8)
        else:
            if z == 255:
                flat[flat > p] -= 1
            else:
                flat[flat < p] += 1
            
            restored = flat.reshape(img_shape)
            # Khôi phục các điểm ảnh biên bị mất từ location map
            restored[location_map] = z
            restored = restored.astype(np.uint8)
            
        return restored

    @staticmethod
    def calculate_metrics(img_orig, img_stego, h):
        mse = np.mean((img_orig.astype(np.float32) - img_stego.astype(np.float32)) ** 2)
        psnr = 10 * np.log10((255**2) / mse) if mse > 0 else 100
        ssim_val = ssim(img_orig, img_stego)
        bpp = h / (img_orig.shape[0] * img_orig.shape[1])
        return psnr, ssim_val, bpp

