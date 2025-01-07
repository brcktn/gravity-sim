from random import randint, shuffle
import itertools

DEFAULT_SETTINGS = {
    "gravitational_constant": 100,
    "collisions combine": True,
}


class Object:
    color_gen = None

    def __init__(self, mass, x, y, x_prime=0, y_prime=0):
        self.mass = mass
        self.radius = mass**0.5  # radius is proportional to the square root of mass
        self.x = x
        self.y = y
        self.x_prime = x_prime
        self.y_prime = y_prime
        self.y_force = 0
        self.x_force = 0
        if Object.color_gen is None:
            Object.color_gen = self.generate_color()
        self.color = next(self.color_gen)

    """
    Get the distance between this object and another object.
    object: The other object.
    return: The distance between the two objects.
    """

    def get_distance(self, object) -> float:
        x_distance = object.x - self.x
        y_distance = object.y - self.y
        return (x_distance**2 + y_distance**2) ** 0.5

    def generate_color(self):
        colors = [
            (1, 1, 1),
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 1, 0),
            (1, 0, 1),
            (0, 1, 1),
        ]
        shuffle(colors)
        counter = 0
        while True:
            yield colors[counter % len(colors)]
            counter += 1


class System:
    def __init__(self, settings=DEFAULT_SETTINGS):
        self.objects: list[Object] = []
        self.G = settings["gravitational_constant"]
        self.settings = settings

    """
    Add an object to the system.
    mass: The mass of the object.
    x: The x position of the object.
    y: The y position of the object.
    x_prime: The initial x velocity of the object.
    y_prime: The initial y velocity of the object.
    """

    def add_object(self, mass, x, y, x_prime=0, y_prime=0):
        object = Object(mass, x, y, x_prime, y_prime)
        self.objects.append(object)

    def update(self, delta_time):
        self.update_forces()
        self.update_velocities(delta_time)
        self.update_positions(delta_time)
        if self.settings["collisions combine"]:
            self.calculate_collisions()

    def update_forces(self):
        for i in range(len(self.objects)):
            self.objects[i].x_force = 0
            self.objects[i].y_force = 0
            for j in range(len(self.objects)):
                if i != j:
                    x_force, y_force = self.calculate_force(
                        self.objects[i], self.objects[j]
                    )

                    self.objects[i].x_force += x_force
                    self.objects[i].y_force += y_force

    def update_velocities(self, delta_time):
        for object in self.objects:
            object.x_prime += object.x_force * delta_time / object.mass
            object.y_prime += object.y_force * delta_time / object.mass

    def update_positions(self, delta_time):
        for object in self.objects:
            object.x += object.x_prime * delta_time
            object.y += object.y_prime * delta_time

    def calculate_force(self, object1, object2):
        x_distance = object2.x - object1.x
        y_distance = object2.y - object1.y
        distance = (x_distance**2 + y_distance**2) ** 0.5

        force = self.G * object1.mass * object2.mass / distance**2
        x_force = force * x_distance / distance
        y_force = force * y_distance / distance

        return x_force, y_force

    def calculate_collisions(self):
        for object1, object2 in itertools.combinations(self.objects, 2):
            if object1.get_distance(object2) < object1.radius + object2.radius:
                new_mass = object1.mass + object2.mass
                new_x = (object1.x * object1.mass + object2.x * object2.mass) / new_mass
                new_y = (object1.y * object1.mass + object2.y * object2.mass) / new_mass
                new_x_prime = (
                    object1.x_prime * object1.mass + object2.x_prime * object2.mass
                ) / new_mass
                new_y_prime = (
                    object1.y_prime * object1.mass + object2.y_prime * object2.mass
                ) / new_mass
                self.objects.remove(object1)
                self.objects.remove(object2)
                self.add_object(new_mass, new_x, new_y, new_x_prime, new_y_prime)
