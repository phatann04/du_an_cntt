import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim

class RDH:
    # Lưu thông tin các peak để dùng trong embed/extract/restore
    peaks_info = []
    location_maps = []

    @staticmethod
    def _is_overlap(range1, range2):
        """Kiểm tra hai khoảng có chồng lấn hay không"""
        return not (range1[1] <= range2[0] or range1[0] >= range2[1])

    @staticmethod
    def analyze_image(img, k=3):
        hist = np.bincount(img.flatten(), minlength=256)

        # Sắp xếp các peak theo tần suất giảm dần
        peak_candidates = np.argsort(hist)[::-1]

        RDH.peaks_info = []
        used_zeros = set()
        used_ranges = []
        border_used = False
        total_capacity = 0

        zeros = np.where(hist == 0)[0]

        for p in peak_candidates:
            if len(RDH.peaks_info) >= k:
                break

            h = int(hist[p])
            if h == 0:
                continue

            # ===== 1. Tìm zero bin khả dụng =====
            available_zeros = [z for z in zeros if z not in used_zeros]
            use_border = False

            if available_zeros:
                # Chọn zero gần peak nhất
                z = int(min(available_zeros, key=lambda x: abs(x - p)))
            else:
                # Nếu không có zero bin, sử dụng border nhưng chỉ một lần
                if border_used:
                    continue
                z = 255 if p < 128 else 0
                use_border = True
                border_used = True

            # ===== 2. Kiểm tra chồng lấn vùng dịch chuyển =====
            new_range = (min(p, z), max(p, z))
            overlap = any(RDH._is_overlap(new_range, r) for r in used_ranges)
            if overlap:
                continue  # Bỏ qua cặp này nếu bị chồng lấn

            # ===== 3. Lưu cặp hợp lệ =====
            RDH.peaks_info.append((int(p), int(z), h, use_border))
            used_zeros.add(z)
            used_ranges.append(new_range)
            total_capacity += h

        # Sắp xếp theo giá trị peak để đảm bảo tính ổn định khi nhúng
        RDH.peaks_info.sort(key=lambda x: x[0])

        if not RDH.peaks_info:
            raise ValueError("Không tìm được cặp Peak–Zero hợp lệ.")

        # Giá trị đại diện để tương thích với main.py
        p_rep, z_rep, _, use_border_rep = RDH.peaks_info[0]
        return p_rep, z_rep, total_capacity, use_border_rep
    @staticmethod
    def embed_data(img, p, z, h, use_border, bits_to_embed):
        stego = img.astype(np.int16).copy()
        bit_index = 0
        location_maps = []

        for (p_i, z_i, h_i, use_border_i) in RDH.peaks_info:
            message = bits_to_embed[bit_index:bit_index + h_i]
            if len(message) < h_i:
                message = np.pad(message, (0, h_i - len(message)), 'constant')

            if not use_border_i:
                direction = 1 if z_i > p_i else -1
                mask = ((stego > p_i) & (stego < z_i)) if z_i > p_i else \
                       ((stego < p_i) & (stego > z_i))
                stego[mask] += direction

                flat = stego.flatten()
                pos = np.where(flat == p_i)[0]
                for i, idx in enumerate(pos[:h_i]):
                    if message[i] == 1:
                        flat[idx] = p_i + direction
                stego = flat.reshape(stego.shape).astype(np.int16)
                location_maps.append(None)
            else:
                location_map = (stego == z_i)
                if z_i == 255:
                    stego[stego > p_i] += 1
                    direction = 1
                else:
                    stego[stego < p_i] -= 1
                    direction = -1

                flat = stego.flatten()
                pos = np.where(flat == p_i)[0]
                for i, idx in enumerate(pos[:h_i]):
                    if message[i] == 1:
                        flat[idx] = p_i + direction
                stego = flat.reshape(stego.shape)
                location_maps.append(location_map)

            bit_index += h_i

        RDH.location_maps = location_maps
        return stego.astype(np.uint8), bits_to_embed[:h], location_maps

    @staticmethod
    def extract_data(stego, p, z, h, use_border):
        flat = stego.astype(np.int16).flatten()
        extracted_bits = []

        for (p_i, z_i, h_i, use_border_i) in RDH.peaks_info:
            direction = 1 if (not use_border_i and z_i > p_i) or \
                             (use_border_i and z_i == 255) else -1

            pos = np.where((flat == p_i) | (flat == p_i + direction))[0]

            for idx in pos[:h_i]:
                if flat[idx] == p_i:
                    extracted_bits.append(0)
                else:
                    extracted_bits.append(1)
                flat[idx] = p_i

        return flat, np.array(extracted_bits[:h])

    @staticmethod
    def restore_image(flat, img_shape, p, z, use_border, location_map):
        for i, (p_i, z_i, h_i, use_border_i) in enumerate(RDH.peaks_info):
            if not use_border_i:
                if z_i > p_i:
                    mask = (flat > p_i) & (flat <= z_i)
                    flat[mask] -= 1
                else:
                    mask = (flat < p_i) & (flat >= z_i)
                    flat[mask] += 1
            else:
                if z_i == 255:
                    flat[flat > p_i] -= 1
                else:
                    flat[flat < p_i] += 1

                # Khôi phục từ location map
                if hasattr(RDH, 'location_maps'):
                    lm = RDH.location_maps[i]
                    if lm is not None:
                        restored_temp = flat.reshape(img_shape)
                        restored_temp[lm] = z_i
                        flat = restored_temp.flatten()

        restored = flat.reshape(img_shape).astype(np.uint8)
        return restored

    @staticmethod
    def calculate_metrics(img_orig, img_stego, h):
        mse = np.mean((img_orig.astype(np.float32) - img_stego.astype(np.float32)) ** 2)
        psnr = 10 * np.log10((255**2) / mse) if mse > 0 else 100
        ssim_val = ssim(img_orig, img_stego)
        bpp = h / (img_orig.shape[0] * img_orig.shape[1])
        return psnr, ssim_val, bpp