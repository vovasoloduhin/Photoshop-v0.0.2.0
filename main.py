from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget,
                             QPushButton, QLabel, QFileDialog, QMenuBar, QAction, QShortcut)
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PIL import Image, ImageEnhance
import os

folder_path = None
current_image = None
history = []

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
        file_path, _ = QFileDialog.getOpenFileName(None, "Вибрати зображення", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
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
        image_path = os.path.join(folder_path, file_name.text())
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

app = QApplication([])
window = QWidget()
window.resize(1000, 700)

main_layout = QVBoxLayout()
menu_bar = QMenuBar()

# Меню "Файл"
file_menu = menu_bar.addMenu("Файл")
open_folder_action = QAction("Відкрити папку", window)
open_folder_action.triggered.connect(open_folder)
file_menu.addAction(open_folder_action)

open_image_action = QAction("Відкрити зображення", window)
open_image_action.triggered.connect(open_image)
file_menu.addAction(open_image_action)

save_image_action = QAction("Зберегти зображення", window)
save_image_action.triggered.connect(save_image)
file_menu.addAction(save_image_action)

# Меню "Редагування"
edit_menu = menu_bar.addMenu("Редагування")
rotate_action = QAction("Повернути на 90°", window)
rotate_action.triggered.connect(rotate_image)
edit_menu.addAction(rotate_action)

contrast_action = QAction("Підвищити контраст", window)
contrast_action.triggered.connect(enhance_contrast)
edit_menu.addAction(contrast_action)

bw_action = QAction("Чорно-білий", window)
bw_action.triggered.connect(convert_to_bw)
edit_menu.addAction(bw_action)

sharpness_action = QAction("Збільшити різкість", window)
sharpness_action.triggered.connect(enhance_sharpness)
edit_menu.addAction(sharpness_action)

brightness_action = QAction("Збільшити яскравість", window)
brightness_action.triggered.connect(enhance_brightness)
edit_menu.addAction(brightness_action)

undo_action_shortcut = QShortcut(QKeySequence("Z"), window)
undo_action_shortcut.activated.connect(undo_action)

main_layout.setMenuBar(menu_bar)

content_layout = QHBoxLayout()
left_layout = QVBoxLayout()
content_layout.addLayout(left_layout, 1)
right_layout = QVBoxLayout()
content_layout.addLayout(right_layout, 2)

file_list = QListWidget()
left_layout.addWidget(file_list)

img_label = QLabel('Тут буде твоє зображення')
right_layout.addWidget(img_label)

main_layout.addLayout(content_layout)

file_list.itemClicked.connect(show_image)

window.setLayout(main_layout)
window.show()
app.exec()
