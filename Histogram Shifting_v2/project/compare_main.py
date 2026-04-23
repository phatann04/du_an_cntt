import sys
import time
import cv2
import numpy as np

from PySide6.QtWidgets import *
from PySide6.QtGui import QPixmap, QImage, QFont
from PySide6.QtCore import Qt

from compare_ui import Ui_MainWindow

# ===== IMPORT 2 THUẬT TOÁN =====
from de_core import embed_de, extract_de, text_to_bits, bits_to_text, psnr, ssim
from hs_logic import RDH

# ===== MATPLOTLIB =====
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# =========================
def cv_to_qt(img):
    h, w = img.shape
    return QPixmap.fromImage(QImage(img.data, w, h, w, QImage.Format_Grayscale8))


# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image = None

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Metric", "DE", "HS"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout(self.ui.metrics_widget)
        layout.addWidget(QLabel("2. Comparison Metrics", font=QFont("Arial", 10, QFont.Bold)))
        layout.addWidget(self.table)
        self.table.setFrameShape(QFrame.Box)
        self.table.setLineWidth(1)

        # ===== CHART =====
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout_chart = QVBoxLayout(self.ui.chart_widget)
        layout_chart.addWidget(QLabel("3. Charts",font=QFont("Arial", 10, QFont.Bold)))
        layout_chart.addWidget(self.canvas)

        # ===== CONNECT =====
        self.ui.loadImage.clicked.connect(self.load_image)
        self.ui.compare.clicked.connect(self.run_compare)

    # =========================
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open", "", "Images (*.png *.jpg)")
        if path:
            self.image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

            self.ui.image.setPixmap(
                cv_to_qt(self.image).scaled(300, 200, Qt.KeepAspectRatio)
            )

            QMessageBox.information(self, "OK", "Load ảnh thành công")

    # =========================
    def run_compare(self):
        if self.image is None:
            QMessageBox.warning(self, "Error", "Chưa load ảnh")
            return

        # ===== INPUT MESSAGE =====
        text, ok = QInputDialog.getText(self, "Input", "Nhập message:")
        if not ok or text == "":
            return

        bits = text_to_bits(text)

        h, w = self.image.shape
        total_pixels = h * w

        # =====================================
        # ===== 1. DE =====
        # =====================================
        T = int(self.ui.threshold.text())

        start = time.time()
        stego_de, lm_de, bit_len_de, cap_de = embed_de(self.image, bits, T)
        embed_time_de = time.time() - start

        start = time.time()
        rec_de, bits_de = extract_de(stego_de, lm_de, bit_len_de)
        extract_time_de = time.time() - start

        msg_de = bits_to_text(bits_de)

        psnr_de = psnr(self.image, stego_de)
        ssim_de = ssim(self.image, stego_de)
        cap_bpp_de = cap_de / total_pixels
        reversible_de = "YES" if np.array_equal(self.image, rec_de) else "NO"

        # =====================================
        # ===== 2. HS =====
        # =====================================
        k = int(self.ui.k_pairs.text())

        p, z, cap_hs, use_border = RDH.analyze_image(self.image, k)

        start = time.time()
        stego_hs, bits_embed_hs, _ = RDH.embed_data(
            self.image, p, z, cap_hs, use_border, np.array(bits)
        )
        embed_time_hs = time.time() - start

        start = time.time()
        flat_hs, bits_hs = RDH.extract_data(stego_hs, p, z, cap_hs, use_border)
        rec_hs = RDH.restore_image(flat_hs, self.image.shape, p, z, use_border, None)
        extract_time_hs = time.time() - start

        # 🔥 FIX MESSAGE HS (cắt đúng độ dài)
        msg_hs = bits_to_text(bits_hs[:len(bits)])

        psnr_hs, ssim_hs, cap_bpp_hs = RDH.calculate_metrics(
            self.image, stego_hs, cap_hs
        )
        reversible_hs = "YES" if np.array_equal(self.image, rec_hs) else "NO"

        # =====================================
        # ===== TABLE =====
        # =====================================
        data = [
            ("Capacity (bpp)", f"{cap_bpp_de:.6f}", f"{cap_bpp_hs:.6f}"),
            ("PSNR", f"{psnr_de:.2f}", f"{psnr_hs:.2f}"),
            ("SSIM", f"{ssim_de:.4f}", f"{ssim_hs:.4f}"),
            ("Embed Time", f"{embed_time_de:.4f}s", f"{embed_time_hs:.4f}s"),
            ("Extract Time", f"{extract_time_de:.4f}s", f"{extract_time_hs:.4f}s"),
            ("Message", msg_de, msg_hs),
            ("Reversible", reversible_de, reversible_hs),
        ]

        self.table.setRowCount(len(data))

        for i, (k, v1, v2) in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(k))
            self.table.setItem(i, 1, QTableWidgetItem(v1))
            self.table.setItem(i, 2, QTableWidgetItem(v2))

        # =====================================
        # ===== CHART =====
        # =====================================
        self.figure.clear()

        # ===== TẠO 2 BIỂU ĐỒ =====
        ax1 = self.figure.add_subplot(211)
        ax2 = self.figure.add_subplot(212)


        # ===== STYLE AXIS (không khung) =====
        def style_axis(ax):
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', linestyle='--', alpha=0.4)
            ax.tick_params(axis='both', labelsize=8)


        # =========================
        # ===== CHART 1: PSNR =====
        # =========================
        labels_psnr = ["PSNR"]
        x1 = np.arange(len(labels_psnr))
        width = 0.3

        bars1 = ax1.bar(x1 - width/2, [psnr_de], width, label="DE")
        bars2 = ax1.bar(x1 + width/2, [psnr_hs], width, label="HS")

        for bars in [bars1, bars2]:
            for b in bars:
                ax1.text(
                    b.get_x() + b.get_width()/2,
                    b.get_height(),
                    f"{b.get_height():.2f}",
                    ha='center',
                    va='bottom',
                    fontsize=7
                )

        ax1.set_title("PSNR Comparison", fontsize=10)
        ax1.set_xticks(x1)
        ax1.set_xticklabels(labels_psnr)
        ax1.legend(fontsize=8)

        style_axis(ax1)


        # =========================
        # ===== CHART 2: OTHERS ===
        # =========================
        labels_other = ["Capacity", "SSIM", "EmbedT", "ExtractT"]

        de_vals = [cap_bpp_de, ssim_de, embed_time_de, extract_time_de]
        hs_vals = [cap_bpp_hs, ssim_hs, embed_time_hs, extract_time_hs]

        x2 = np.arange(len(labels_other))

        bars3 = ax2.bar(x2 - width/2, de_vals, width, label="DE")
        bars4 = ax2.bar(x2 + width/2, hs_vals, width, label="HS")

        for bars in [bars3, bars4]:
            for b in bars:
                ax2.text(
                    b.get_x() + b.get_width()/2,
                    b.get_height(),
                    f"{b.get_height():.4f}",
                    ha='center',
                    va='bottom',
                    fontsize=7
                )

        ax2.set_title("Other Metrics Comparison", fontsize=10)
        ax2.set_xticks(x2)
        ax2.set_xticklabels(labels_other)
        ax2.legend(fontsize=8)

        style_axis(ax2)


        # ===== FIX LỆCH CHUẨN NHẤT =====
        self.figure.tight_layout(pad=1.2)

        self.canvas.draw()


# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())