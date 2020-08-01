
class Robot:

    def __init__(self, battery, motor, camera, behaviour):
        self.position = [19, 0]
        self.battery = battery
        self.motor = motor
        self.camera = camera
        self.behaviour = behaviour
        self.batteryLeft = (battery * 60)
        self.cost = (battery * 100) + (motor * 100) + (camera * 100)