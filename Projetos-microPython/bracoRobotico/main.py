#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Arm Program
-----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

# Inicialize o Bloco EV3
ev3 = EV3Brick()

# Configure o motor da garra na Porta A com as configurações padrão.
gripper_motor = Motor(Port.A)

# Configure o motor do cotovelo. Tem uma engrenagem de 8 dentes e uma de 40 dentes
# conectado a ele. Gostaríamos de valores de velocidade positivos para tornar o
# braço para cima. Isso corresponde à rotação no sentido anti-horário
# do motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure o motor que gira a base. Tem 12 dentes e um
# Engrenagem de 36 dentes conectada a ela. Gostaríamos de valores de velocidade positivos
# para afastar o braço do sensor de toque. Isso corresponde
# para rotação anti-horária do motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limite as acelerações do cotovelo e da base. Isto resulta em
# movimento muito suave. Como um robô industrial.
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Configure o sensor de toque. Ele atua como um interruptor final na base
# do braço do robô. Define o ponto inicial da base.
base_switch = TouchSensor(Port.S1)

# Configure o sensor de cores. Este sensor detecta quando o cotovelo
# está na posição inicial. É quando o sensor vê o
# feixe branco de perto.
elbow_sensor = ColorSensor(Port.S3)

# Inicialize o cotovelo. Primeiro, faça-o descer por um segundo.
# Em seguida, faça-o subir lentamente (15 graus por segundo) até
# o sensor de cor detecta o feixe branco. Em seguida, reinicie o motor
# ângulo para tornar este o ponto zero. Finalmente, segure o motor
# no lugar para que não se mova.
elbow_motor.run_time(-30, 1000)
elbow_motor.run(15)
while elbow_sensor.reflection() < 32:
    wait(10)
elbow_motor.reset_angle(0)
elbow_motor.hold()

# Inicializa a base. Primeiro gire-o até que o sensor de toque
# na base é pressionado. Redefina o ângulo do motor para fazer isso
# o ponto zero. Em seguida, segure o motor no lugar para que ele não se mova.
base_motor.run(-60)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# Inicialize a garra. Primeiro gire o motor até que ele pare.
# Stalling significa que ele não pode se mover mais. Este cargo
# corresponde à posição fechada. Em seguida, gire o motor
# em 90 graus de modo que a pinça esteja aberta.
gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)


def robot_pick(position):
    # Esta função faz a base do robô girar para o indicado
    # posição. Lá ele abaixa o cotovelo, fecha a pinça e
    # levanta o cotovelo para pegar o objeto.

    # Gire para a posição de coleta.
    base_motor.run_target(60, position)
    # Abaixe o braço.
    elbow_motor.run_target(60, -40)
    # Feche a pinça para agarrar a pilha de rodas.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Levante o braço para levantar a pilha de rodas.
    elbow_motor.run_target(60, 0)


def robot_release(position):
    # Esta função faz a base do robô girar para o indicado
    # posição. Ali abaixa o cotovelo, abre a pinça para
    # solte o objeto. Em seguida, levanta o braço novamente.

    # Gire para a posição de queda.
    base_motor.run_target(60, position)
    # Abaixe o braço para colocar a pilha de rodas no chão.
    elbow_motor.run_target(60, -40)
    # Abra a garra para liberar a pilha de rodas.
    gripper_motor.run_target(200, -90)
    # Levante o braço.
    elbow_motor.run_target(60, 0)


# Toque três bipes para indicar que a inicialização foi concluída.
for i in range(3):
    ev3.speaker.beep()
    wait(100)

# Defina os três destinos para pegar e mover as pilhas de rodas.
LEFT = 160
MIDDLE = 100
RIGHT = 40

# Esta é a parte principal do programa. É um loop que se repete infinitamente.
#
# Primeiro, o robô move o objeto à esquerda em direção ao meio.
# Segundo, o robô move o objeto da direita para a esquerda.
# Finalmente, o robô move o objeto que agora está no meio, para a direita.
#
# Agora temos uma pilha de rodas à esquerda e à direita como antes, mas elas
# trocou de lugar. Em seguida, o loop se repete para fazer isso indefinidamente.
while True:
    # Mova uma pilha de rodas da esquerda para o meio.
    robot_pick(LEFT)
    robot_release(MIDDLE)

    # Mova uma pilha de rodas da direita para a esquerda.
    robot_pick(RIGHT)
    robot_release(LEFT)

    # Mova uma pilha de rodas do meio para a direita.
    robot_pick(MIDDLE)
    robot_release(RIGHT)