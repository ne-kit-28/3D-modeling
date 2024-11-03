from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time

# Размер изображения
width, height = 500, 500
num_circles = 100  # Количество окружностей для отрисовки и замера времени

def draw_circle_bresenham(x_center, y_center, radius):
    """Рисуем окружность с помощью алгоритма Брезенхема."""
    x = 0
    y = radius
    d = 3 - 2 * radius

    pixels = set()

    def plot_circle_points(x_center, y_center, x, y):
        """Отмечаем симметричные точки окружности."""
        points = [
            (x_center + x, y_center + y), (x_center - x, y_center + y),
            (x_center + x, y_center - y), (x_center - x, y_center - y),
            (x_center + y, y_center + x), (x_center - y, y_center + x),
            (x_center + y, y_center - x), (x_center - y, y_center - x)
        ]
        for point in points:
            pixels.add(point)

    while y >= x:
        plot_circle_points(x_center, y_center, x, y)
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6

    return pixels


def flood_fill_stack(image, x, y, fill_color):
    """Затравочный алгоритм заполнения (flood fill) с использованием стека."""
    height, width, _ = image.shape
    target_color = image[y, x].copy()
    if np.array_equal(target_color, fill_color):
        return

    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if cx < 0 or cy < 0 or cx >= width or cy >= height:
            continue
        if not np.array_equal(image[cy, cx], target_color):
            continue

        image[cy, cx] = fill_color
        stack.extend([(cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)])


def display():
    """Функция отрисовки одного круга."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Создаем пустое черно-белое изображение
    image = np.zeros((height, width, 3), dtype=np.uint8)

    # Рисуем окружность белым цветом
    circle_pixels = draw_circle_bresenham(width // 2, height // 2, 110)
    for (x, y) in circle_pixels:
        if 0 <= x < width and 0 <= y < height:
            image[y, x] = (255, 255, 255)  # Белый цвет

    # Заполняем окружность зеленым цветом
    flood_fill_stack(image, width // 2, height // 2, (0, 255, 0))

    # Отображаем изображение
    glDrawPixels(width, height, GL_RGB, GL_UNSIGNED_BYTE, image)

    glutSwapBuffers()


def measure_render_time():
    # Начало замера времени
    start_time = time.time()

    # Рисуем num_circles окружностей
    for _ in range(num_circles):
        display()

    # Окончание замера времени
    end_time = time.time()

    # Выводим затраченное время
    print(f"Время на отрисовку {num_circles} окружностей: {end_time - start_time:.2f} секунд")


def init():
    """Инициализация."""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Черный фон


# Настройка окна и запуск OpenGL
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutCreateWindow(b"Filled Circle with Bresenham and Flood Fill")

init()
glutDisplayFunc(display)
glutIdleFunc(measure_render_time)  # Запускаем замер времени после инициализации
glutMainLoop()
