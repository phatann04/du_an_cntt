import sys
import cv2
import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


# =======================
# TEXT <-> BIT
# =======================
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


# =======================
# DE ALGORITHM
# =======================
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

            x, y = int(stego[i, j]), int(stego[i, j + 1])
            l = (x + y) // 2
            d = x - y

            b = bits[bit_idx]
            d_new = 2 * d + b

            x_new = l + (d_new + 1) // 2
            y_new = l - d_new // 2

            if 0 <= x_new <= 255 and 0 <= y_new <= 255:
                stego[i, j], stego[i, j + 1] = x_new, y_new
                location_map.append(1)
                bit_idx += 1
            else:
                location_map.append(0)

    return stego, location_map, bit_idx


def extract_de(stego, location_map, bit_len):
    h, w = stego.shape
    recovered = stego.copy()
    extracted_bits = []
    lm_idx = 0

    for i in range(h):
        for j in range(0, w - 1, 2):
            if lm_idx >= len(location_map):
                continue

            if location_map[lm_idx] == 1 and len(extracted_bits) < bit_len:
                x, y = int(recovered[i, j]), int(recovered[i, j + 1])

                d_new = x - y
                b = d_new & 1
                d = d_new // 2
                l = (x + y) // 2

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
    if mse == 0:
        return 100
    return 10 * np.log10((255 ** 2) / mse)


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
# IMAGE CONVERT
# =======================
def cv_to_qt(img):
    h, w = img.shape
    return QPixmap.fromImage(QImage(img.data, w, h, w, QImage.Format_Grayscale8))


# =======================
# GUI
# =======================
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reversible Data Hiding - DE")
        self.resize(1000, 700)

        self.image = None
        self.stego = None
        self.location_map = None
        self.bit_len = 0

        layout = QVBoxLayout()

        # ===== IMAGE =====
        img_layout = QHBoxLayout()
        self.label1 = QLabel("Original")
        self.label2 = QLabel("Stego")
        self.label3 = QLabel("Recovered")

        for lbl in [self.label1, self.label2, self.label3]:
            lbl.setFixedSize(300, 300)
            lbl.setStyleSheet("border:1px solid black;")
            lbl.setAlignment(Qt.AlignCenter)

        img_layout.addWidget(self.label1)
        img_layout.addWidget(self.label2)
        img_layout.addWidget(self.label3)

        # ===== INPUT =====
        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Nhập thông điệp...")

        # ===== OUTPUT =====
        self.output_text = QLineEdit()
        self.output_text.setReadOnly(True)

        # ===== TABLE =====
        self.table = QTableWidget(5, 2)
        self.table.setHorizontalHeaderLabels(["Thông số", "Giá trị"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)

        self.table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                background-color: #f9f9f9;
                gridline-color: #ccc;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                font-weight: bold;
                padding: 5px;
            }
        """)

        # ===== BUTTON =====
        btn_layout = QHBoxLayout()
        btn_load = QPushButton("Load Image")
        btn_embed = QPushButton("Embed")
        btn_extract = QPushButton("Extract")

        btn_load.clicked.connect(self.load_image)
        btn_embed.clicked.connect(self.embed)
        btn_extract.clicked.connect(self.extract)

        btn_layout.addWidget(btn_load)
        btn_layout.addWidget(btn_embed)
        btn_layout.addWidget(btn_extract)

        # ===== ADD =====
        layout.addLayout(img_layout)
        layout.addWidget(self.input_text)
        layout.addLayout(btn_layout)
        layout.addWidget(self.output_text)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg)")
        if path:
            self.image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            self.label1.setPixmap(cv_to_qt(self.image).scaled(300, 300))

    def embed(self):
        if self.image is None:
            return

        bits = text_to_bits(self.input_text.text())
        self.stego, self.location_map, self.bit_len = embed_de(self.image, bits)
        self.label2.setPixmap(cv_to_qt(self.stego).scaled(300, 300))

    def extract(self):
        if self.stego is None:
            return

        recovered, bits = extract_de(self.stego, self.location_map, self.bit_len)
        self.label3.setPixmap(cv_to_qt(recovered).scaled(300, 300))
        self.output_text.setText(bits_to_text(bits))

        # ===== METRICS =====
        payload = self.bit_len
        h, w = self.image.shape
        capacity = payload / (h * w)
        psnr_val = psnr(self.image, self.stego)
        ssim_val = ssim(self.image, self.stego)
        reversible = "YES ✅" if np.array_equal(self.image, recovered) else "NO ❌"

        data = [
            ("Payload (bits)", payload),
            ("Embedding Capacity (bpp)", f"{capacity:.6f}"),
            ("PSNR (dB)", f"{psnr_val:.2f}"),
            ("SSIM", f"{ssim_val:.4f}"),
            ("Perfect Reversibility", reversible),
        ]

        for i, (k, v) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(k)))
            self.table.setItem(i, 1, QTableWidgetItem(str(v)))


# RUN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())