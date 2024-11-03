from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

# Параметры окна и окружности
width, height = 500, 500
circle_radius = 0.5
circle_segments = 50  # Количество сегментов, чем больше, тем круглее окружность
num_circles = 1000000  # Количество окружностей для отрисовки и замера времени


def triangulate_circle_filled_efficient(x, y, radius, segments):
    glBegin(GL_TRIANGLE_FAN)

    # Центральная точка окружности
    glVertex2f(x, y)

    # Вычисляем угол поворота между сегментами
    angle_step = 2 * math.pi / segments
    cos_step = math.cos(angle_step)
    sin_step = math.sin(angle_step)

    # Начальная точка на окружности
    dx, dy = radius, 0.0

    # Триангуляция окружности с использованием итеративного вращения
    for _ in range(segments + 1):
        glVertex2f(x + dx, y + dy)

        # Обновляем dx и dy с использованием матрицы поворота
        new_dx = dx * cos_step - dy * sin_step
        new_dy = dx * sin_step + dy * cos_step
        dx, dy = new_dx, new_dy

    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Рисуем заполненную окружность
    glColor3f(0.0, 0.5, 1.0)  # Голубой цвет
    triangulate_circle_filled_efficient(0.0, 0.0, circle_radius, circle_segments)

    glFlush()


def measure_render_time():
    # Начало замера времени
    start_time = time.time()

    # Рисуем num_circles окружностей
    for _ in range(num_circles):
        triangulate_circle_filled_efficient(0.0, 0.0, circle_radius, circle_segments)

    # Окончание замера времени
    end_time = time.time()

    # Выводим затраченное время
    print(f"Time taken to render {num_circles} circles: {end_time - start_time:.2f} seconds")


# Настройка окна и запуск OpenGL
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Efficient Triangulated Filled Circle in PyOpenGL")
glutDisplayFunc(display)
glutIdleFunc(measure_render_time)  # Запускаем замер времени после инициализации
glutMainLoop()
