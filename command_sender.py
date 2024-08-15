import math
import socket
from dataclasses import asdict
from typing import Iterable
from protobufs import (
    grSim_Commands_pb2,
    grSim_Packet_pb2,
    ssl_vision_detection_pb2,
)

from data_classes import RobotCommand

import json
class CommandsSender:
    UDP_IP = "172.16.41.67"
    UDP_PORT = 20010

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    is_yellow_team = True

    my_robots_team = "robots_blue" if not is_yellow_team else "robots_yellow"
    enemies_robots_team = "robots_blue" if is_yellow_team else "robots_yellow"

    balls = dict()
    my_robots = dict()
    enemies_robots = dict()

    @classmethod
    def send(cls, robot_commands: list[RobotCommand]):
        robot_commands_proto = [
            grSim_Commands_pb2.grSim_Robot_Command(**asdict(command))
            for command in robot_commands
        ]

        commands = grSim_Commands_pb2.grSim_Commands()
        commands.timestamp = 0
        commands.isteamyellow = cls.is_yellow_team
        commands.robot_commands.extend(robot_commands_proto)
        print(commands.robot_commands)
        packet = grSim_Packet_pb2.grSim_Packet()
        packet.commands.CopyFrom(commands)

        serialized_packet = packet.SerializeToString()

        cls.sock.sendto(json.dumps([asdict(command) for command in robot_commands]).encode('utf-8'), (cls.UDP_IP, cls.UDP_PORT))

    @classmethod
    def update_my_team(
        cls, robots_data: Iterable[ssl_vision_detection_pb2.SSL_DetectionRobot]
    ):
        for robot in robots_data:
            cls.my_robots[robot.robot_id] = robot

    @classmethod
    def update_enemy_team(
        cls, robots_data: Iterable[ssl_vision_detection_pb2.SSL_DetectionRobot]
    ):
        for robot in robots_data:
            cls.enemies_robots[robot.robot_id] = robot

    @classmethod
    def update_data(cls, data: ssl_vision_detection_pb2.SSL_DetectionFrame):
        if data.balls:
            cls.balls = data.balls
        cls.update_my_team(getattr(data, cls.my_robots_team))
        cls.update_enemy_team(getattr(data, cls.enemies_robots_team))

    @classmethod
    def gerar_comando_robo(
        cls, id_robo, x_robo, y_robo, orientacao_robo, x_bola, y_bola, v_constante=1.0
    ):
        # Calcular o ângulo de orientação
        theta = math.atan2(y_bola - y_robo, x_bola - x_robo)

        # Calcular a diferença angular
        delta_orientacao = theta - orientacao_robo

        # Normalizar o ângulo para o intervalo [-pi, pi]
        delta_orientacao = (delta_orientacao + math.pi) % (2 * math.pi) - math.pi

        # Criar comando do robô
        comando = RobotCommand(id=id_robo)

        # Se o robô não estiver orientado corretamente, ajustar a orientação
        if abs(delta_orientacao) > 0.3:  # Pode ajustar o limite conforme necessário
            comando.velangular = delta_orientacao
        else:
            # Se estiver orientado corretamente, seguir em frente
            comando.veltangent = v_constante
        comando.kickspeedx = 3
        return comando

    @classmethod
    def run(cls):
        while True:
            if not all([cls.balls, cls.my_robots, cls.enemies_robots]):
                continue

            robot_commands = list()
            for robot in cls.my_robots.values():
                robot_commands.append(
                    cls.gerar_comando_robo(
                        robot.robot_id,
                        robot.x,
                        robot.y,
                        robot.orientation,
                        cls.balls[0].x,
                        cls.balls[0].y,
                    )
                )
            cls.send(robot_commands)
