import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileDialog, 
                               QMessageBox, QInputDialog, QHeaderView, QTableWidgetItem)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

# Import class từ file rdh_logic.py của ông
from rdh_logic import RDH 
# Import UI từ file đã convert (đổi tên cho đúng file của ông)
from ui_app import Ui_MainWindow 
class RDH_Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Khởi tạo engine và biến lưu trữ
        self.engine = RDH()
        self.cv_img_orig = None
        self.cv_img_stego = None
        self.cv_img_restored = None
        
        # Cấu hình bảng thông số
        self.setup_metrics_table()
        
        # Kết nối sự kiện
        self.ui.btn_load.clicked.connect(self.load_image)
        self.ui.btn_rdh.clicked.connect(self.run_full_process)
        self.ui.btn_save_stego.clicked.connect(lambda: self.save_image(self.cv_img_stego, "stego"))
        self.ui.bth_save_restore.clicked.connect(lambda: self.save_image(self.cv_img_restored, "restored"))
        self.ui.btn_clear.clicked.connect(self.clear_all)
        hist_labels = [
            (self.ui.hist_ori, "Original Histogram", lambda: self.cv_img_orig),
            (self.ui.hist_stego, "Stego Histogram", lambda: self.cv_img_stego),
            (self.ui.hist_restore, "Restored Histogram", lambda: self.cv_img_restored)
        ]

        for label, title, img_func in hist_labels:
            label.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            label.setCursor(Qt.PointingHandCursor)
            # Dùng lambda để truyền đúng dữ liệu ảnh tại thời điểm click
            label.mousePressEvent = lambda e, t=title, f=img_func: self.interactive_histogram(f(), t)

    def setup_metrics_table(self):
        self.ui.metrics.setColumnCount(2)
        self.ui.metrics.setHorizontalHeaderLabels(["Thông số", "Giá trị"])
        self.ui.metrics.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.metrics.verticalHeader().setVisible(False)

    def get_hist_pixmap(self, cv_img, title):
        """Vẽ histogram chuẩn Matplotlib cho báo cáo"""
        fig, ax = plt.subplots(figsize=(2.8, 2.0), dpi=100)
        ax.hist(cv_img.ravel(), bins=256, range=[0, 256], color='teal', alpha=0.7)
        ax.set_title(title, fontsize=9, fontweight='bold')
        plt.tight_layout()
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        rgba = np.frombuffer(canvas.buffer_rgba(), dtype='uint8').reshape(canvas.get_width_height()[1], canvas.get_width_height()[0], 4)
        plt.close(fig)
        return QPixmap.fromImage(QImage(rgba.data, rgba.shape[1], rgba.shape[0], QImage.Format_RGBA8888))

    def display_cv_image(self, cv_img, label_widget):
        if cv_img is None: return
        h, w = cv_img.shape[:2]
        q_img = QImage(cv_img.data, w, h, w, QImage.Format_Grayscale8)
        label_widget.setPixmap(QPixmap.fromImage(q_img).scaled(label_widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_widget.setText("")

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Image Files (*.png *.jpg *.bmp)")
        if path:
            self.cv_img_orig = cv2.imread(path, 0)
            self.display_cv_image(self.cv_img_orig, self.ui.img_ori)
            self.ui.hist_ori.setPixmap(self.get_hist_pixmap(self.cv_img_orig, "Original Hist"))

    def run_full_process(self):
        if self.cv_img_orig is None:
            QMessageBox.warning(self, "Lỗi", "Chưa có ảnh gốc")
            return

        # 1. Nhập tin nhắn văn bản
        text, ok = QInputDialog.getText(self, 'Input', 'Nhập tin nhắn cần giấu:')
        if not ok or not text: return
        
        # Chuyển văn bản thành bit
        input_bits = np.unpackbits(np.frombuffer(text.encode('utf-8'), dtype=np.uint8))

        # 2. Bước Analyze
        p, z, h, use_border = self.engine.analyze_image(self.cv_img_orig)

        # 3. Bước Embed
        self.cv_img_stego, embedded_bits, loc_map = self.engine.embed_data(
            self.cv_img_orig, p, z, h, use_border, input_bits
        )

        # 4. Bước Extract (Lấy flat để chuẩn bị restore)
        flat_after_extract, extracted_bits = self.engine.extract_data(
            self.cv_img_stego, p, z, h, use_border
        )

        # 5. Bước Restore
        self.cv_img_restored = self.engine.restore_image(
            flat_after_extract, self.cv_img_orig.shape, p, z, use_border, loc_map
        )
        input_bits = np.unpackbits(np.frombuffer(text.encode('utf-8'), dtype=np.uint8))
        len_input_bits = len(input_bits) # Lưu lại độ dài này

        # 6. Giải mã tin nhắn trích xuất được (decode bits -> string)
        try:
            # Chỉ lấy đúng số bit tương ứng với tin nhắn đã nhúng
            useful_bits = extracted_bits[:len_input_bits] 
            decoded_text = np.packbits(useful_bits).tobytes().decode('utf-8', errors='ignore')
            decoded_text = decoded_text.strip('\x00')
        except:
            decoded_text = "Lỗi giải mã"

        # 7. Tính toán Metrics 
        psnr, ssim_val, bpp = self.engine.calculate_metrics(self.cv_img_orig, self.cv_img_stego, h)

        # 8. Cập nhật UI
        self.display_cv_image(self.cv_img_stego, self.ui.img_stego)
        self.display_cv_image(self.cv_img_restored, self.ui.img_restored)
        self.ui.hist_stego.setPixmap(self.get_hist_pixmap(self.cv_img_stego, "Stego Hist"))
        self.ui.hist_restore.setPixmap(self.get_hist_pixmap(self.cv_img_restored, "Restored Hist"))

        # Điền bảng Metrics
        is_reversible = np.array_equal(self.cv_img_orig, self.cv_img_restored)
        data = [
            ("Peak Pixel (P)", p),
            ("Zero Pixel (Z)", z),
            ("Sức chứa (Capacity)", f"{h} bits"),
            ("PSNR", f"{psnr:.2f} dB"),
            ("SSIM", f"{ssim_val:.4f}"),
            ("BPP", f"{bpp:.4f}"),
            ("Tin trích xuất", decoded_text),
            ("Tính thuận nghịch", "Hoàn hảo ✅" if is_reversible else "Thất bại ❌")
        ]
        
        self.ui.metrics.setRowCount(len(data))
        for i, (k, v) in enumerate(data):
            self.ui.metrics.setItem(i, 0, QTableWidgetItem(str(k)))
            self.ui.metrics.setItem(i, 1, QTableWidgetItem(str(v)))

    def save_image(self, img, type_name):
        if img is None:
            QMessageBox.warning(self, "Lỗi", f"Không có ảnh {type_name} để lưu!")
            return
        path, _ = QFileDialog.getSaveFileName(self, f"Save {type_name}", f"{type_name}.png", "PNG (*.png)")
        if path: cv2.imwrite(path, img)

    def interactive_histogram(self, cv_img, title):
        if cv_img is None: 
            QMessageBox.warning(self, "Lỗi", "Ảnh chưa được load!")
            return
        
        # Bật lại chế độ tương tác để tránh bị block GUI
        plt.ion() 
        
        # Tạo hoặc lấy figure theo tên title
        fig = plt.figure(num=title, figsize=(10, 6))
        fig.clf() # Xóa nội dung cũ để vẽ mới
        
        ax = fig.add_subplot(111)
        
        # Vẽ histogram
        ax.hist(cv_img.ravel(), bins=256, range=[0, 256], 
                color='teal', alpha=0.7, histtype='stepfilled', 
                edgecolor='black', linewidth=0.5)
        
        ax.set_title(f"Cửa sổ soi chi tiết: {title}")
        ax.set_xlabel("Giá trị Pixel (0-255)")
        ax.set_ylabel("Số lượng")
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
        
        # Ép Matplotlib vẽ và hiển thị
        fig.canvas.draw()
        plt.show()
        
        # Nâng cửa sổ lên trên cùng (đôi khi nó hiện đằng sau main window)
        fig.canvas.manager.window.raise_()
    def clear_all(self):
        # 1. Reset các biến dữ liệu ảnh về None
        self.cv_img_orig = None
        self.cv_img_stego = None
        self.cv_img_restored = None
        
        # 2. Xóa ảnh hiển thị trên 3 QLabel
        self.ui.img_ori.clear()
        self.ui.img_stego.clear()
        self.ui.img_restored.clear()
        
        # 3. Xóa Histogram
        self.ui.hist_ori.clear()
        self.ui.hist_stego.clear()
        self.ui.hist_restore.clear()
        
        # 4. Xóa bảng thông số (Metrics)
        self.ui.metrics.setRowCount(0) # Xóa sạch các hàng trong bảng
        
        # 6. Thông báo nhẹ cho người dùng (Tùy chọn)
        QMessageBox.information(self, "Đã xóa", "Đã xóa tất cả dữ liệu và reset giao diện!")    

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RDH_Application()
    window.show()
    sys.exit(app.exec())
    