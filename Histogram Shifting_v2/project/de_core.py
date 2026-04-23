import numpy as np

# =======================
# TEXT <-> BIT
# =======================
def text_to_bits(text):
    return [int(b) for ch in text for b in format(ord(ch), '08b')]


def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int(''.join(map(str, byte)), 2)))
    return ''.join(chars)


# =======================
# IMPROVED DE (FIXED)
# =======================
def embed_de(image, bits, T=8):
    h, w = image.shape
    # Đảm bảo làm việc trên kiểu dữ liệu lớn để tránh tràn số khi tính toán d_new
    stego = image.copy().astype(np.int8 if image.dtype == np.int8 else np.int16)
    
    # Nếu ảnh gốc là uint8, ta nên dùng int16 để tính toán trung gian
    image_int = image.astype(np.int16)
    stego = image.copy().astype(np.int32)

    location_map = []
    bit_idx = 0
    capacity_count = 0  # Đây là True Capacity sẽ hiển thị trên bảng

    for i in range(h):
        for j in range(0, w - 1, 2):
            x = int(image_int[i, j])
            y = int(image_int[i, j + 1])

            l = (x + y) // 2
            d = x - y

            # --- ĐIỀU KIỆN QUYẾT ĐỊNH TRUE CAPACITY ---
            # Thử nghiệm với trường hợp xấu nhất (nhúng bit 1) để kiểm tra tràn
            d_test = 2 * d + 1
            x_test = l + (d_test + 1) // 2
            y_test = l - d_test // 2

            # Nếu thỏa mãn ngưỡng T và không gây tràn (0-255)
            if abs(d) < T and 0 <= x_test <= 255 and 0 <= y_test <= 255:
                # Tăng True Capacity bất kể có nhúng bit hay không
                capacity_count += 1 

                # --- LOGIC NHÚNG BIT THỰC TẾ ---
                if bit_idx < len(bits):
                    b = bits[bit_idx]
                    d_new = 2 * d + b

                    stego[i, j] = (l + (d_new + 1) // 2)
                    stego[i, j + 1] = (l - d_new // 2)

                    location_map.append(1)
                    bit_idx += 1
                else:
                    # Đã hết bit để nhúng nhưng vị trí này vẫn được tính là có khả năng nhúng
                    location_map.append(0)
            else:
                # Không thỏa mãn T hoặc bị tràn ảnh
                location_map.append(0)

    stego = np.clip(stego, 0, 255).astype(np.uint8)
    
    # Trả về capacity_count để bạn đưa vào dòng "True Capacity" trong bảng
    return stego, location_map, bit_idx, capacity_count

# =======================
# EXTRACTION
# =======================
def extract_de(stego, location_map, bit_len):
    h, w = stego.shape
    recovered = stego.copy().astype(np.uint8)
    extracted_bits = []
    lm_idx = 0

    for i in range(h):
        for j in range(0, w - 1, 2):
            if lm_idx < len(location_map):
                # Chỉ xử lý nếu location_map đánh dấu là 1
                if location_map[lm_idx] == 1 and len(extracted_bits) < bit_len:
                    x_s = int(stego[i, j])
                    y_s = int(stego[i, j + 1])

                    d_new = x_s - y_s
                    l = (x_s + y_s) // 2
                    
                    b = d_new & 1 # Lấy bit cuối (LSB)
                    d = d_new // 2 # Phục hồi d cũ bằng phép chia nguyên
                    
                    recovered[i, j] = l + (d + 1) // 2
                    recovered[i, j + 1] = l - d // 2
                    
                    extracted_bits.append(b)
                
                lm_idx += 1

    return recovered, extracted_bits

# =======================
# METRICS
# =======================
def psnr(img1, img2):
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    return 100 if mse == 0 else 10 * np.log10((255**2) / mse)


def ssim(img1, img2):
    C1, C2 = 6.5025, 58.5225
    img1, img2 = img1.astype(float), img2.astype(float)

    mu1, mu2 = img1.mean(), img2.mean()
    sigma1, sigma2 = img1.var(), img2.var()
    sigma12 = ((img1 - mu1) * (img2 - mu2)).mean()

    return ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / (
        (mu1**2 + mu2**2 + C1) * (sigma1 + sigma2 + C2)
    )
    
# =======================
# DỮ LIỆU BIỂU ĐỒ (DÙNG CHO NÚT TEST T)
# =======================
def get_capacity_data(image, bits, T_list=[1, 2, 4, 8, 16, 32]):
    """
    Hàm này chạy thử nhiều ngưỡng T để lấy dữ liệu vẽ biểu đồ.
    Nó gọi hàm embed_de bên trên nhưng không làm thay đổi logic của hàm đó.
    """
    capacities_bpp = []
    
    # Kích thước ảnh để tính bpp (bits per pixel)
    h, w = image.shape
    total_pixels = h * w
    
    for t in T_list:
        # Gọi hàm embed_de của bạn để lấy capacity_count (giá trị thứ 4)
        _, _, _, cap_count = embed_de(image, bits, T=t)
        
        # Tính toán giá trị bpp (trục Y cho biểu đồ)
        bpp = cap_count / total_pixels
        capacities_bpp.append(bpp)
    
    return T_list, capacities_bpp