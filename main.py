from PyQt5 import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget,
                             QPushButton, QLabel, QFileDialog, QDialog, QDialogButtonBox, QShortcut, QInputDialog,
                             QFontDialog, QColorDialog, QFormLayout, QGridLayout)
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageFont, ImageDraw
import os

from rembg import remove
from io import BytesIO

import numpy as np

import random


folder_path = None
current_image = None
history = []

def apply_stylesheet(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #1E1E1E;
            color: white;
            font-family: Arial, sans-serif;
        }
        QPushButton {
            background-color: #3A3F44;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
            color: white;
        }
        QPushButton:hover {
            background-color: #50555B;
        }
        QPushButton:pressed {
            background-color: #60666D;
        }
        QListWidget {
            background-color: #252526;
            border-radius: 8px;
            padding: 5px;
            border: 1px solid #3A3F44;
        }
        QListWidget:item {
            padding: 5px;
        }
        QLabel {
            background-color: #252526;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            font-size: 16px;
        }
        QDialog {
            background-color: #1E1E1E;
        }
    """)

def open_folder():
    global folder_path
    try:
        folder_path = QFileDialog.getExistingDirectory()
        file_list.clear()
        for file in os.listdir(folder_path):
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                file_list.addItem(file)
    except Exception as e:
        print(e)

def open_image():
    global folder_path, current_image, history
    try:
        file_path, _ = QFileDialog.getOpenFileName(None, "Вибрати зображення", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            folder_path = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            file_list.addItem(file_name)
            show_image(file_name)
    except Exception as e:
        print(e)

def show_image(file_name):
    global folder_path, current_image, history
    try:
        image_path = os.path.join(folder_path, file_name)
        current_image = Image.open(image_path).convert("RGB")
        history.clear()
        history.append(current_image.copy())
        display_image(current_image)
    except Exception as e:
        print(e)

def display_image(img):
    img = img.convert("RGB")
    img.thumbnail((500, 500))
    img_qt = QImage(img.tobytes(), img.width, img.height, img.width * 3, QImage.Format_RGB888)
    img_label.setPixmap(QPixmap.fromImage(img_qt))

def rotate_image():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        current_image = current_image.rotate(-90, expand=True)
        display_image(current_image)

def enhance_contrast():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        enhancer = ImageEnhance.Contrast(current_image)
        current_image = enhancer.enhance(1.5)
        display_image(current_image)

def convert_to_bw():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        current_image = current_image.convert("L")
        display_image(current_image)

def enhance_sharpness():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        enhancer = ImageEnhance.Sharpness(current_image)
        current_image = enhancer.enhance(2.0)
        display_image(current_image)

def enhance_brightness():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        enhancer = ImageEnhance.Brightness(current_image)
        current_image = enhancer.enhance(1.5)
        display_image(current_image)

def apply_blur():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        current_image = current_image.filter(ImageFilter.GaussianBlur(radius=5))
        display_image(current_image)

def flip_vertical():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        current_image = current_image.transpose(Image.FLIP_TOP_BOTTOM)
        display_image(current_image)

def flip_horizontal():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        current_image = current_image.transpose(Image.FLIP_LEFT_RIGHT)
        display_image(current_image)

def remove_bg():
    global current_image, history
    if current_image:

        history.append(current_image.copy())

        img_byte_array = BytesIO()
        current_image.save(img_byte_array, format='PNG')

        input_data = img_byte_array.getvalue()
        output_data = remove(input_data)

        output_image = Image.open(BytesIO(output_data)).convert("RGBA")

        datas = output_image.getdata()
        new_data = []
        for item in datas:
            if all([x > 200 for x in item[:3]]):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        output_image.putdata(new_data)

        current_image = output_image
        display_image(current_image)

def resize_img():
    global current_image, history
    if current_image:
        try:
            width, height = current_image.size
            new_width, new_height = 800, 600
            history.append(current_image.copy())
            current_image = current_image.resize((new_width, new_height))
            display_image(current_image)
        except Exception as e:
            print(e)

def save_image():
    global current_image
    if current_image:
        file_path, _ = QFileDialog.getSaveFileName(None, "Зберегти зображення", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            current_image.save(file_path)

def undo_action():
    global current_image, history
    if len(history) > 1:
        history.pop()
        current_image = history[-1].copy()
        display_image(current_image)

def add_border():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        border_color = (255, 0, 0)
        border_width = 20
        current_image = ImageOps.expand(current_image, border=border_width, fill=border_color)
        display_image(current_image)

def invert_colors():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        current_image = ImageOps.invert(current_image.convert("RGB"))
        display_image(current_image)

def enhance_saturation():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        enhancer = ImageEnhance.Color(current_image)
        current_image = enhancer.enhance(1.5)
        display_image(current_image)

def apply_smoothing():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        current_image = current_image.filter(ImageFilter.SMOOTH)
        display_image(current_image)

def apply_warp():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()

        for x in range(width):
            for y in range(height):
                offset_x = int(10 * np.sin(y / 20.0))
                new_x = max(0, min(width - 1, x + offset_x))
                pixels[x, y] = pixels[new_x, y]

        display_image(current_image)

def apply_sepia():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))

        display_image(current_image)

def apply_glitch():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()

        for y in range(height):
            if random.random() < 0.1:
                shift = random.randint(-10, 10)
                for x in range(width):
                    new_x = max(0, min(width - 1, x + shift))
                    pixels[x, y] = pixels[new_x, y]

        display_image(current_image)

def add_custom_border():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        color = QColorDialog.getColor()
        if color.isValid():
            border_width, ok = QInputDialog.getInt(None, "Вибір товщини", "Товщина рамки:", 10, 1, 100)
            if ok:
                current_image = ImageOps.expand(current_image, border=border_width, fill=color.getRgb()[:3])
                display_image(current_image)

def add_noise():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()
        noise_factor = 0.05

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                r = min(255, max(0, r + random.randint(-int(255 * noise_factor), int(255 * noise_factor))))
                g = min(255, max(0, g + random.randint(-int(255 * noise_factor), int(255 * noise_factor))))
                b = min(255, max(0, b + random.randint(-int(255 * noise_factor), int(255 * noise_factor))))
                pixels[x, y] = (r, g, b)

        display_image(current_image)


def add_vignette():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()

        max_radius = min(width, height) // 2
        for x in range(width):
            for y in range(height):
                dist = np.sqrt((x - width / 2)**2 + (y - height / 2)**2)
                factor = 1 - min(dist / max_radius, 1)
                r, g, b = pixels[x, y]
                r = int(r * factor)
                g = int(g * factor)
                b = int(b * factor)
                pixels[x, y] = (r, g, b)

        display_image(current_image)

def apply_mosaic():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        block_size, ok = QInputDialog.getInt(None, "Розмір блоку пікселя", "Розмір блоку (пікселі):", 10, 1, 100)
        if ok:
            width, height = current_image.size
            pixels = current_image.load()

            for x in range(0, width, block_size):
                for y in range(0, height, block_size):
                    r_total, g_total, b_total = 0, 0, 0
                    count = 0

                    for dx in range(block_size):
                        for dy in range(block_size):
                            if x + dx < width and y + dy < height:
                                r, g, b = pixels[x + dx, y + dy]
                                r_total += r
                                g_total += g
                                b_total += b
                                count += 1

                    avg_r = r_total // count
                    avg_g = g_total // count
                    avg_b = b_total // count

                    for dx in range(block_size):
                        for dy in range(block_size):
                            if x + dx < width and y + dy < height:
                                pixels[x + dx, y + dy] = (avg_r, avg_g, avg_b)

            display_image(current_image)


def apply_color_explosion():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()

        center_x, center_y = width // 2, height // 2

        for x in range(width):
            for y in range(height):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                max_distance = ((width // 2) ** 2 + (height // 2) ** 2) ** 0.5

                r, g, b = pixels[x, y]
                r = int(r + (255 - r) * (distance / max_distance))
                g = int(g + (255 - g) * (distance / max_distance))
                b = int(b + (255 - b) * (distance / max_distance))

                pixels[x, y] = (min(r, 255), min(g, 255), min(b, 255))

        display_image(current_image)


def apply_gravitational_field():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()


        center_x, center_y = width // 2, height // 2

        for x in range(width):
            for y in range(height):

                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                factor = max(0, 1 - distance / max(width, height))

                r, g, b = pixels[x, y]
                r = int(r * factor)
                g = int(g * factor)
                b = int(b * factor)

                pixels[x, y] = (r, g, b)

        display_image(current_image)

def apply_retro_effect():
    global current_image, history
    if current_image:
        history.append(current_image.copy())
        width, height = current_image.size
        pixels = current_image.load()

        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                r = int(r * 1.1)
                g = int(g * 0.9)
                b = int(b * 0.8)
                pixels[x, y] = (min(r, 255), min(g, 255), min(b, 255))

        noise_factor = 0.05
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                r = min(255, max(0, r + random.randint(-int(255 * noise_factor), int(255 * noise_factor))))
                g = min(255, max(0, g + random.randint(-int(255 * noise_factor), int(255 * noise_factor))))
                b = min(255, max(0, b + random.randint(-int(255 * noise_factor), int(255 * noise_factor))))
                pixels[x, y] = (r, g, b)

        display_image(current_image)


def apply_cartoon_effect():
    global current_image, history
    if current_image:
        history.append(current_image.copy())

        enhancer = ImageEnhance.Contrast(current_image)
        current_image = enhancer.enhance(4.0)

        current_image = current_image.filter(ImageFilter.CONTOUR)
        display_image(current_image)

def open_settings_menu():
    settings_menu = SettingsMenu()
    settings_menu.exec_()

class SettingsMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Меню налаштувань")
        self.setGeometry(500, 500, 500, 600)

        layout = QGridLayout()

        rotate_button = QPushButton("Повернути на 90°")
        rotate_button.clicked.connect(rotate_image)
        layout.addWidget(rotate_button)

        contrast_button = QPushButton("Підвищити контраст")
        contrast_button.clicked.connect(enhance_contrast)
        layout.addWidget(contrast_button)

        bw_button = QPushButton("Чорно-білий")
        bw_button.clicked.connect(convert_to_bw)
        layout.addWidget(bw_button)

        sharpness_button = QPushButton("Збільшити різкість")
        sharpness_button.clicked.connect(enhance_sharpness)
        layout.addWidget(sharpness_button)

        brightness_button = QPushButton("Збільшити яскравість")
        brightness_button.clicked.connect(enhance_brightness)
        layout.addWidget(brightness_button)

        saturation_button = QPushButton('Збільшити насиченості')
        saturation_button.clicked.connect(enhance_brightness)
        layout.addWidget(saturation_button)

        invert_colors_button = QPushButton('Інвертувати кольори')
        invert_colors_button.clicked.connect(invert_colors)
        layout.addWidget(invert_colors_button)

        sepia_button = QPushButton('Сепія')
        sepia_button.clicked.connect(apply_sepia)
        layout.addWidget(sepia_button)

        warp_button = QPushButton('Викривлення')
        warp_button.clicked.connect(apply_warp)
        layout.addWidget(warp_button)

        smoothing_button = QPushButton('Сгладжування')
        smoothing_button.clicked.connect(apply_smoothing)
        layout.addWidget(smoothing_button)

        glitch_button = QPushButton('Глітч ефект')
        glitch_button.clicked.connect(apply_glitch)
        layout.addWidget(glitch_button)

        cartoon_button = QPushButton('Ефект глову')
        cartoon_button.clicked.connect(apply_cartoon_effect)
        layout.addWidget(cartoon_button)

        blur_button = QPushButton("Розмити фото")
        blur_button.clicked.connect(apply_blur)
        layout.addWidget(blur_button)

        flip_vertical_button = QPushButton("Відзеркалити вертикально")
        flip_vertical_button.clicked.connect(flip_vertical)
        layout.addWidget(flip_vertical_button)

        flip_horizontal_button = QPushButton("Відзеркалити горизонтально")
        flip_horizontal_button.clicked.connect(flip_horizontal)
        layout.addWidget(flip_horizontal_button)

        remove_bg_button = QPushButton("Видалити фон")
        remove_bg_button.clicked.connect(remove_bg)
        layout.addWidget(remove_bg_button)

        resize_button = QPushButton("Змінити розмір")
        resize_button.clicked.connect(resize_img)
        layout.addWidget(resize_button)

        mozaik_button = QPushButton('Ефект пікселей')
        mozaik_button.clicked.connect(apply_mosaic)
        layout.addWidget(mozaik_button)

        gravity_button = QPushButton('Мале затемненя')
        gravity_button.clicked.connect(apply_gravitational_field)
        layout.addWidget(gravity_button)

        retro_button = QPushButton('Ефект ретро')
        retro_button.clicked.connect(apply_retro_effect)
        layout.addWidget(retro_button)

        explosion_button = QPushButton('Вибух кольорів')
        explosion_button.clicked.connect(apply_color_explosion)
        layout.addWidget(explosion_button)

        noise_button = QPushButton('Ефект погрози')
        noise_button.clicked.connect(add_noise)
        layout.addWidget(noise_button)

        board_button = QPushButton('Додати рамку')
        board_button.clicked.connect(add_custom_border)
        layout.addWidget(board_button)

        vignette_button = QPushButton('Ефект Поляризація')
        vignette_button.clicked.connect(add_vignette)
        layout.addWidget(vignette_button)

        undo_action_button = QPushButton('Відмінити дію(ї)')
        undo_action_button.clicked.connect(undo_action)
        layout.addWidget(undo_action_button)

        close_button = QDialogButtonBox(QDialogButtonBox.Close)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

app = QApplication([])
window = QWidget()
window.resize(1000, 700)

main_layout = QVBoxLayout()

content_layout = QHBoxLayout()
left_layout = QVBoxLayout()
content_layout.addLayout(left_layout, 1)
right_layout = QVBoxLayout()
content_layout.addLayout(right_layout, 2)

file_list = QListWidget()
left_layout.addWidget(file_list)

undo_action_shortcut = QShortcut(QKeySequence("Z"), window)
undo_action_shortcut.activated.connect(undo_action)

img_label = QLabel('Тут буде твоє зображення')
right_layout.addWidget(img_label)

button_layout = QVBoxLayout()

open_image_button = QPushButton("Відкрити зображення")
open_image_button.clicked.connect(open_image)
button_layout.addWidget(open_image_button)

save_button = QPushButton("Зберегти зображення")
save_button.clicked.connect(save_image)
button_layout.addWidget(save_button)

functions_button = QPushButton("Функції")
functions_button.clicked.connect(open_settings_menu)
button_layout.addWidget(functions_button)

left_layout.addLayout(button_layout)

file_list.itemClicked.connect(show_image)

main_layout.addLayout(content_layout)

window.setLayout(main_layout)

apply_stylesheet(app)

window.show()
app.exec()
