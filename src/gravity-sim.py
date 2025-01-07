from system import System
import math

import cairo
import cv2
import numpy as np

FPS = 60
VIDEO_LENGTH_SECONDS = 10
VIDEO_WIDTH = 500
VIDEO_HEIGHT = 500

SIMULATION_CALC_PER_FRAME = 1000

SIMULATION_WIDTH = 120
SIMULATION_HEIGHT = SIMULATION_WIDTH * VIDEO_HEIGHT / VIDEO_WIDTH

PX_PER_UNIT_DIST = VIDEO_WIDTH / SIMULATION_WIDTH

SETTINGS = {
    "gravitational_constant": 1000,
    "collisions combine": True,
}


def main():
    system = System(settings=SETTINGS)
    system.add_object(30, 20, 0, -1, -20)
    system.add_object(20, -20, 0, -1, 20)
    system.add_object(10, 0, 20, 20, 0)

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
        context.arc(x, y, object.radius * PX_PER_UNIT_DIST, 0, 2 * math.pi)
        context.fill()

    buffer = surface.get_data()
    img = np.ndarray(
        shape=(VIDEO_HEIGHT, VIDEO_WIDTH, 4), dtype=np.uint8, buffer=buffer
    )

    return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)


if __name__ == "__main__":
    main()
