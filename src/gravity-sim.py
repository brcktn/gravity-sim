from system import System
import math
import os

import cairo
import cv2
import numpy as np

FPS = 60
VIDEO_LENGTH_SECONDS = 5
VIDEO_WIDTH = 500
VIDEO_HEIGHT = 500

SIMULATION_CALC_PER_FRAME = 1000

SIMULATION_WIDTH = 10
SIMULATION_HEIGHT = 10

PX_PER_MASS = 5


def main():
    system = System()
    system.add_object(1, 1, 0, 0, 0)
    system.add_object(1, 2, 0, 0, 0)
    system.add_object(1, 3, 0, 0, 0)
    system.add_object(1, -3, 0, 0, 0)
    system.add_object(1, -2, 0, 0, 0)
    system.add_object(1, -1, 0, 0, 0)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter("output.mp4", fourcc, FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))

    for i in range(FPS * VIDEO_LENGTH_SECONDS * SIMULATION_CALC_PER_FRAME):
        system.update(1 / FPS / SIMULATION_CALC_PER_FRAME)
        if i % SIMULATION_CALC_PER_FRAME == 0:
            frame = render_frame(system)
            video.write(frame)

    video.release()


def render_frame(system: System):
    surface = cairo.ImageSurface(cairo.Format.RGB24, VIDEO_WIDTH, VIDEO_HEIGHT)
    context = cairo.Context(surface)

    context.set_source_rgb(0.1, 0.1, 0.1)
    context.paint()

    for object in system.objects:
        context.set_source_rgb(*object.color)
        x = (object.x + SIMULATION_WIDTH / 2) / SIMULATION_WIDTH * VIDEO_WIDTH
        y = (object.y + SIMULATION_HEIGHT / 2) / SIMULATION_HEIGHT * VIDEO_HEIGHT
        context.arc(x, y, object.mass * PX_PER_MASS, 0, 2 * math.pi)
        context.fill()

    buffer = surface.get_data()
    img = np.ndarray(
        shape=(VIDEO_HEIGHT, VIDEO_WIDTH, 4), dtype=np.uint8, buffer=buffer
    )

    return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)


if __name__ == "__main__":
    main()
