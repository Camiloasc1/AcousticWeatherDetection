class ClimbingAgent(object):
    def __init__(self, world, position, movement_range, height_threshold, hill_up=True):
        self.world = world
        self.position = position
        self.movement_range = movement_range
        self.height_threshold = height_threshold
        self.hill_up = hill_up

    def __str__(self):
        return "Agent [at: " + str(self.position) + " value: " + str(self.value) + "]"

    def climb(self):
        for i in self.range(True):
            self.position = i
        return self

    def range(self, check_climb=False):
        for i in range(max(0, self.position - self.movement_range),
                       min(self.position + self.movement_range + 1, len(self.world))):
            if check_climb:
                if self.can_move_to(i):
                    yield i
            else:
                yield i

    def can_move_to(self, i):
        return (self.hill_up and self.world[i] > self.value) or \
               (not self.hill_up and self.world[i] < self.value)

    @property
    def value(self):
        return self.world[self.position]

    @property
    def is_alive(self):
        return self.value >= self.height_threshold

    @property
    def can_move(self):
        for _ in self.range(True):
            return True
        return False

    @property
    def is_on_peak(self):
        return self.is_alive and not self.can_move
