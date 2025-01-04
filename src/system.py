import math

class Object:
    def __init__(self, mass, x, y, x_prime=0, y_prime=0):
        self.mass = mass
        self.x = x
        self.y = y
        self.x_prime = x_prime
        self.y_prime = y_prime
        self.y_force = 0
        self.x_force = 0

class System:
    G = 1

    def __init__(self):
        self.objects: list[Object] = []

    def add_object(self, mass, x, y, x_prime=0, y_prime=0):
        object = Object(mass, x, y, x_prime, y_prime)
        self.objects.append(object)

    def update(self, delta_time):
        self.update_forces()
        self.update_velocities(delta_time)
        self.update_positions(delta_time)

    def update_forces(self):
        for i in range(len(self.objects)):
            self.objects[i].x_force = 0
            self.objects[i].y_force = 0
            for j in range(len(self.objects)):
                if i != j:
                    x_force, y_force = self.calculate_force(self.objects[i], self.objects[j])

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
        distance = (x_distance ** 2 + y_distance ** 2) ** 0.5

        force = self.G * object1.mass * object2.mass / distance ** 2
        x_force = force * x_distance / distance
        y_force = force * y_distance / distance

        return x_force, y_force