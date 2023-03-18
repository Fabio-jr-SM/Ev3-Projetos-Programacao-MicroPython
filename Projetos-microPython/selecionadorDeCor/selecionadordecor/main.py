#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Color Sorter Program
--------------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

# Os objetos coloridos são vermelhos, verdes, azuis ou amarelos.
POSSIBLE_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]

# Inicialize o bloco EV3.
ev3 = EV3Brick()

# Inicializar os motores que acionam a esteira e ejetar os objetos.
belt_motor = Motor(Port.D)
feed_motor = Motor(Port.A)

# Inicialize o sensor de toque. É usado para detectar quando o motor da correia
# moveu o módulo classificador totalmente para a esquerda.
touch_sensor = TouchSensor(Port.S1)

# Inicialize o sensor de cor. É usado para detectar a cor dos objetos.
color_sensor = ColorSensor(Port.S3)


# Este é o loop principal. Ele espera que você escaneie e insira 8 objetos coloridos.
# Em seguida, ele os classifica por cor. Em seguida, o processo recomeça e você pode digitalizar
# e insira o próximo conjunto de objetos coloridos.
while True:
    # Coloque o motor de alimentação na posição inicial correta.
     # Isso é feito girando o motor para frente até que ele pare. Esse
     # significa que ele não pode se mover mais. A partir deste ponto final, o motor
     # gira para trás em 180 graus. Então está na posição inicial.
    feed_motor.run_until_stalled(120, duty_limit=50)
    feed_motor.run_angle(450, -200)

    # Coloque o motor da correia transportadora na posição inicial correta.
     # Isso é feito rodando primeiro o motor da correia para trás até que o
     # sensor de toque é pressionado. Então o motor para, e o ângulo é
     # redefinir para zero. Isso significa que quando ele gira para trás para zero mais tarde
     # Acesso, ele retorna a esta posição inicial.
    belt_motor.run(-500)
    while not touch_sensor.pressed():
        pass
    belt_motor.stop()
    wait(1000)
    belt_motor.reset_angle(0)

    # Quando digitalizamos os objetos, armazenamos todos os números de cores em uma lista.
     # Começamos com uma lista vazia. Ele crescerá à medida que adicionarmos cores a ele.
    color_list = []

    # Este loop escaneia as cores dos objetos. Repete até 8 objetos
     # são escaneados e colocados no chute. Isso é feito repetindo o loop
     # enquanto o comprimento da lista ainda for menor que 8.
    while len(color_list) < 8:
        # Mostra uma seta que aponta para o sensor de cores.
        ev3.screen.load_image(ImageFile.RIGHT)

        # Mostra quantos objetos coloridos já digitalizamos.
        ev3.screen.print(len(color_list))

        # Aguarde até que o botão central seja pressionado ou uma cor seja digitalizada.
        while True:
            # Store True se o botão central for pressionado ou False se não for.
            pressed = Button.CENTER in ev3.buttons.pressed()
            # Armazene a cor medida pelo sensor de cor.
            color = color_sensor.color()
            # Se o botão central for pressionado ou uma cor for detectada,
             # sair do loop.
            if pressed or color in POSSIBLE_COLORS:
                break

        if pressed:
            # Se o botão foi pressionado, finalize o loop antecipadamente. nós não iremos mais
             # espera que quaisquer objetos restantes sejam verificados e adicionados a calha.
            break

        # Caso contrário, uma cor foi digitalizada. Portanto, adicionamos (acrescentamos) à lista.
        ev3.speaker.beep(1000, 100)
        color_list.append(color)

        # Não queremos registrar a mesma cor mais uma vez se ainda estivermos
         # olhando para o mesmo objeto. Portanto, antes de continuarmos, esperamos até que o
         # sensor não vê mais o objeto.
        while color_sensor.color() in POSSIBLE_COLORS:
            pass
        ev3.speaker.beep(2000, 100)

        # Mostrar uma seta apontando para o botão central, para perguntar se terminamos.
        ev3.screen.load_image(ImageFile.BACKWARD)
        wait(2000)

    # Toque um som e mostre uma imagem para indicar que terminamos a digitalização.
    ev3.speaker.play_file(SoundFile.READY)
    ev3.screen.load_image(ImageFile.EV3)

    # Agora classifique os tijolos de acordo com a lista de cores que armazenamos.
     # Fazemos isso examinando cada cor na lista em um loop.
    for color in color_list:
        # Aguarde um segundo entre cada ação de classificação.
        wait(1000)

        # Execute o motor da correia transportadora para a posição correta com base na cor.
        if color == Color.BLUE:
            ev3.speaker.say('blue')
            belt_motor.run_target(500, 10)
        elif color == Color.GREEN:
            ev3.speaker.say('green')
            belt_motor.run_target(500, 132)
        elif color == Color.YELLOW:
            ev3.speaker.say('yellow')
            belt_motor.run_target(500, 360)
        elif color == Color.RED:
            ev3.speaker.say('red')
            belt_motor.run_target(500, 530)

        # Agora que a correia transportadora está na posição correta, ejete o objeto colorido.
        feed_motor.run_angle(1500, 180)
        feed_motor.run_angle(1500, -180)
