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
    G = 6.67430e-11

    def __init__(self):
        self.objects: list[Object] = []

    def add_object(self, object: Object):
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
                    self.objects[i].x_force += self.calculate_force_x(self.objects[i], self.objects[j])
                    self.objects[i].y_force += self.calculate_force_y(self.objects[i], self.objects[j])

    def update_velocities(self, delta_time):
        for object in self.objects:
            object.x_prime += object.x_force * delta_time / object.mass
            object.y_prime += object.y_force * delta_time / object.mass

    def update_positions(self, delta_time):
        for object in self.objects:
            object.x += object.x_prime * delta_time
            object.y += object.y_prime * delta_time

    def calculate_force_x(self, object1: Object, object2: Object):
        distance = object2.x - object1.x
        return self.G * object1.mass * object2.mass / distance ** 2
    
    def calculate_force_y(self, object1: Object, object2: Object):
        distance = object2.y - object1.y
        return self.G * object1.mass * object2.mass / distance ** 2