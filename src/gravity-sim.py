from system import System
import math
import os

import cairo
import cv2

FPS = 60
VIDEO_WIDTH = 500
VIDEO_HEIGHT = 500

SIMULATION_WIDTH = 5
SIMULATION_HEIGHT = 5

PX_PER_MASS = 5


def main():
    system = System()
    system.add_object(4, 0, 0, 0, 0)
    system.add_object(1, 2, 0, 0, -1)


    if not os.path.exists("frames"):
        os.makedirs("frames")

    frame_count = 0

    for i in range (100000):
        system.update(0.0001)
        if i % 200 == 0:
            render_frame(system, frame_count)
            frame_count += 1

    if frame_count > 0:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter("output.mp4", fourcc, FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))

        for i in range(frame_count):
            frame = cv2.imread(f"frames/frame_{i:05d}.png")
            video.write(frame)

        video.release()

        for i in range(frame_count):
            os.remove(f"frames/frame_{i:05d}.png")
        
    os.rmdir("frames")




def render_frame(system: System, frame_count: int):
    surface = cairo.ImageSurface(cairo.Format.RGB24, VIDEO_WIDTH, VIDEO_HEIGHT)
    context = cairo.Context(surface)

    context.set_source_rgb(0.1, 0.1, 0.1)
    context.paint()

    for object in system.objects:
        context.set_source_rgb(*object.color)
        x = (object.x + SIMULATION_WIDTH / 2) / SIMULATION_WIDTH * VIDEO_WIDTH
        y = (object.y + SIMULATION_HEIGHT / 2) / SIMULATION_HEIGHT * VIDEO_HEIGHT
        context.arc(x, y, object.mass*PX_PER_MASS, 0, 2 * math.pi)
        context.fill()

    surface.write_to_png(f"frames/frame_{frame_count:05d}.png")


if __name__ == "__main__":
    main()