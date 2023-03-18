
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

# Inicializa o EV3 Brick.
ev3 = EV3Brick()

# Inicializa os motores.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Inicializa o drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Anda a uma distancia de 1000mm e depois retorna.
robot.straight(1000)
ev3.speaker.beep()

robot.straight(-1000)
ev3.speaker.beep()

# Gira em um angulo de 360 graus.
robot.turn(360)
ev3.speaker.beep()

robot.turn(-360)
ev3.speaker.beep()
