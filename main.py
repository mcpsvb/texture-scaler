# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QSpinBox, QFrame,
    QSizePolicy
)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize
from PIL import Image

# Отключаем ограничение на размер изображения в Pillow для обработки больших текстур
Image.MAX_IMAGE_PIXELS = None

class MinecraftUpscaler(QWidget):
    def __init__(self):
        super().__init__()
        self.original_image = None
        self.upscaled_image = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MCTextureScaler')
        self.setGeometry(200, 200, 800, 600)
        self.setWindowIcon(self.create_icon())

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        controls_layout = QHBoxLayout()
        self.btn_open = QPushButton('Open Texture...')
        self.btn_open.clicked.connect(self.open_image)

        lbl_scale = QLabel('multiplier:')
        self.scale_spinner = QSpinBox()
        self.scale_spinner.setRange(2, 64)
        self.scale_spinner.setValue(4)
        self.scale_spinner.setSuffix('x')

        self.btn_upscale = QPushButton('Upscale')
        self.btn_upscale.clicked.connect(self.upscale_image)
        self.btn_upscale.setEnabled(False)

        self.btn_save = QPushButton('Save Result...')
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)

        controls_layout.addWidget(self.btn_open)
        controls_layout.addStretch(1)
        controls_layout.addWidget(lbl_scale)
        controls_layout.addWidget(self.scale_spinner)
        controls_layout.addWidget(self.btn_upscale)
        controls_layout.addStretch(1)
        controls_layout.addWidget(self.btn_save)

        images_layout = QHBoxLayout()
        
        original_layout = QVBoxLayout()
        lbl_original_title = QLabel('Original')
        lbl_original_title.setAlignment(Qt.AlignCenter)
        self.lbl_original_size = QLabel('Size: -')
        self.lbl_original_size.setAlignment(Qt.AlignCenter)
        self.img_original_label = QLabel('Load Image')
        self.img_original_label.setAlignment(Qt.AlignCenter)
        self.img_original_label.setFrameShape(QFrame.StyledPanel)
        self.img_original_label.setMinimumSize(300, 300)
        self.img_original_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        original_layout.addWidget(lbl_original_title)
        original_layout.addWidget(self.img_original_label)
        original_layout.addWidget(self.lbl_original_size)

        upscaled_layout = QVBoxLayout()
        lbl_upscaled_title = QLabel('Result')
        lbl_upscaled_title.setAlignment(Qt.AlignCenter)
        self.lbl_upscaled_size = QLabel('Size: -')
        self.lbl_upscaled_size.setAlignment(Qt.AlignCenter)
        self.img_upscaled_label = QLabel('There will be an enlarged image here')
        self.img_upscaled_label.setAlignment(Qt.AlignCenter)
        self.img_upscaled_label.setFrameShape(QFrame.StyledPanel)
        self.img_upscaled_label.setMinimumSize(300, 300)
        self.img_upscaled_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        upscaled_layout.addWidget(lbl_upscaled_title)
        upscaled_layout.addWidget(self.img_upscaled_label)
        upscaled_layout.addWidget(self.lbl_upscaled_size)

        images_layout.addLayout(original_layout)
        images_layout.addLayout(upscaled_layout)

        self.status_label = QLabel('ready for work!')
        self.status_label.setAlignment(Qt.AlignCenter)

        # Добавляем все в основной макет
        main_layout.addLayout(controls_layout)
        main_layout.addLayout(images_layout)
        main_layout.addWidget(self.status_label)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #3c3c3c;
                color: #f0f0f0;
                font-size: 14px;
            }
            QPushButton {
                background-color: #5a5a5a;
                border: 1px solid #6a6a6a;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #6a6a6a;
            }
            QPushButton:pressed {
                background-color: #4a4a4a;
            }
            QPushButton:disabled {
                background-color: #4f4f4f;
                color: #888;
            }
            QLabel {
                background-color: transparent;
            }
            QSpinBox {
                background-color: #2c2c2c;
                padding: 5px;
                border-radius: 4px;
                border: 1px solid #6a6a6a;
            }
            QFrame {
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #2c2c2c;
            }
        """)

    def open_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Texture", "", "Image Files (*.png *.jpg *.bmp *.gif);;All Files (*)", options=options)
        if file_name:
            try:
                self.original_image = Image.open(file_name)
                self.display_image(self.original_image, self.img_original_label, self.lbl_original_size)
                self.btn_upscale.setEnabled(True)
                self.btn_save.setEnabled(False) # blocking button
                self.img_upscaled_label.clear()
                self.img_upscaled_label.setText('Press "upscale"')
                self.lbl_upscaled_size.setText('Size: -')
                self.status_label.setText(f'Working File: {file_name}')
            except Exception as e:
                self.status_label.setText(f'Error while opening the file: {e}')
                self.btn_upscale.setEnabled(False)

    def upscale_image(self):
        if not self.original_image:
            self.status_label.setText('Open the image first!')
            return

        scale_factor = self.scale_spinner.value()
        original_size = self.original_image.size
        new_size = (original_size[0] * scale_factor, original_size[1] * scale_factor)

        self.status_label.setText('Working...')
        QApplication.processEvents() # Обновляем интерфейс

        self.upscaled_image = self.original_image.resize(new_size, Image.Resampling.NEAREST)

        self.display_image(self.upscaled_image, self.img_upscaled_label, self.lbl_upscaled_size)
        self.btn_save.setEnabled(True)
        self.status_label.setText(f'Texture upscaled by {scale_factor} times.')

    def save_image(self):
        if not self.upscaled_image:
            self.status_label.setText('No image for saving!')
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Result", "", "PNG file (*.png);;All Files (*)", options=options)
        if file_name:
            try:
                if not file_name.lower().endswith('.png'):
                    file_name += '.png'
                
                self.upscaled_image.save(file_name, "PNG")
                self.status_label.setText(f'Result saved to: {file_name}')
            except Exception as e:
                self.status_label.setText(f'Error while saving the file: {e}')

    def display_image(self, pil_image, label_widget, size_label_widget):
        try:
            image_qt = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, pil_image.width * len(pil_image.getbands()), QImage.Format_RGBA8888 if pil_image.mode == 'RGBA' else QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image_qt)
        
            scaled_pixmap = pixmap.scaled(label_widget.size(), Qt.KeepAspectRatio, Qt.FastTransformation)
            label_widget.setPixmap(scaled_pixmap)
            
            size_label_widget.setText(f'Size: {pil_image.width}x{pil_image.height}px')
        except Exception as e:
            self.status_label.setText(f"Display Error: {e}")


    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.original_image:
            self.display_image(self.original_image, self.img_original_label, self.lbl_original_size)
        if self.upscaled_image:
            self.display_image(self.upscaled_image, self.img_upscaled_label, self.lbl_upscaled_size)

    def create_icon(self):
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        from PyQt5.QtGui import QPainter, QColor, QBrush
        painter = QPainter(pixmap)
        
        painter.fillRect(4, 12, 24, 16, QColor('#8B4513')) # Коричневая земля
        painter.fillRect(4, 4, 24, 8, QColor('#228B22')) # Зеленая трава
        painter.setPen(QColor('#3c3c3c'))
        
        for i in range(4, 29, 4):
            painter.drawLine(i, 4, i, 28)
            painter.drawLine(4, i, 28, i)

        painter.end()
        return QIcon(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinecraftUpscaler()
    ex.show()
    sys.exit(app.exec_())
