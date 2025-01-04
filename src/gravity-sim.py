from system import System
import cairo
import math

FPS = 120
VIDEO_WIDTH = 512
VIDEO_HEIGHT = 512

SIMULATION_WIDTH = 5
SIMULATION_HEIGHT = 5

PX_PER_MASS = 5


def main():
    system = System()
    system.add_object(1, 1, 0)
    system.add_object(1, -1, 0)
    system.add_object(1, 0, 1)
    system.add_object(2, 0, 2.5)

    render_frame(system)

    for _ in range(10000):
        system.update(0.0001)




def render_frame(system: System):
    surface = cairo.ImageSurface(cairo.Format.RGB24, VIDEO_WIDTH, VIDEO_HEIGHT)
    context = cairo.Context(surface)

    context.set_source_rgb(0.1, 0.1, 0.1)
    context.paint()

    context.set_source_rgb(1, 1, 1)
    for object in system.objects:
        x = (object.x + SIMULATION_WIDTH / 2) / SIMULATION_WIDTH * VIDEO_WIDTH
        y = (object.y + SIMULATION_HEIGHT / 2) / SIMULATION_HEIGHT * VIDEO_HEIGHT
        context.arc(x, y, object.mass*PX_PER_MASS, 0, 2 * math.pi)
        context.fill()

    surface.write_to_png("frame.png")


if __name__ == "__main__":
    main()