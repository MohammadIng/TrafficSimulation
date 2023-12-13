import math
from vehicle import Vehicle

import pygame
from math import sin, radians, degrees
from pygame.math import Vector2


class Car(Vehicle):

    def __init__(self, currentPosition=Vector2(0, 0), angle=0, length=4):
        Vehicle.__init__(self)
        self.currentPosition = currentPosition
        self.length = length
        self.turnDistance = 30
        self.ppu = 15

        # IDM parameters
        self.l = 10
        self.s0 = 4
        self.T = 1
        self.v_max = 50
        self.a_max = 50
        self.b_max = 10
        self.v = self.v_max
        self.velocity = Vector2(self.v_max, 0.0)
        self.a = 1
        self.sqrt_ab = 2 * math.sqrt(self.a_max * self.b_max)

    # car drive
    def car_Driving(self, dt, leadCar=None, leadLeftCar=None):

        if self.v + self.a * dt < 0:
            self.velocity.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.velocity.x += self.v * dt + self.a * dt * dt / 2

        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 90

        self.currentPosition += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt

        if self.isTurn and self.toTurn():
            self.steering = self.curveAngle

        alpha = self.driveCheck(leadCar, leadLeftCar)

        self.velocity.x = self.v

        self.a = self.a_max * (1 - (self.v / self.v_max) ** 10 - alpha ** 2)

    def isCarInCrossing(self, car, minX=25, maxX=80, minY=17, maxY=50):
        if not car:
            return False
        if minX * 15 <= car.currentPosition[0] * 15 <= maxX * 15 and minY * 15 <= car.currentPosition[1] * 15 <= maxY * 15:
            return True
        return False

    def isLeftCarsInCrossing(self, cars, minX=25, maxX=80, minY=17, maxY=50):
        for car in cars:
            if not car:
                return False

            if car.velocity[0] > 1 and minX * 15 <= car.currentPosition[0] * 15 <= maxX * 15 and minY * 15 <= car.currentPosition[1] * 15 <= maxY * 15:
                return True
        return False


    def driveCheck(self, leadCar,  leadLeftCar):
        alpha = 0
        lengthFactor = 0

        if leadCar:
            if not self.isTruck and leadCar.isTruck:
                lengthFactor = 5

            if math.dist(self.currentPosition, self.checkPoint) < 4 and self.trafficSignal.state != "green" and math.dist(self.currentPosition, leadCar.currentPosition) > 5 and not self.isCarInCrossing(self, minX=33, maxX=61, minY=18, maxY=35):
                delta_x = math.dist(self.checkPoint * 4, self.currentPosition * 4) - self.disCP
                delta_v = 0

            else:
                if not self.isTurn and leadCar.turnState == "left" and self.isCarInCrossing(self, minX=33, maxX=55, minY=18, maxY=35):
                    delta_x = 50
                    delta_v = self.v
                else:
                    delta_x = math.dist(leadCar.currentPosition * 4, self.currentPosition * 4) - (self.l+lengthFactor)
                    delta_v = self.v - leadCar.v

            if self.turnState == "left" and self.isCarInCrossing(self, minX=33, maxX=55, minY=18, maxY=35) and self.isLeftCarsInCrossing(self.leftCars):

                if leadLeftCar:
                    if self.isCarInCrossing(leadLeftCar):
                        delta_x = math.dist(leadLeftCar.currentPosition * 4, self.currentPosition * 4) - (self.l+lengthFactor)
                        delta_v = self.v - leadLeftCar.v
                    if math.dist(self.currentPosition * 4, leadLeftCar.currentPosition*4) > 20:
                        p1 = (self.checkPointLeft[0] * 4, self.checkPointLeft[1] * 4)
                        delta_x = math.dist(p1, self.currentPosition * 4) - self.disCP
                        delta_v = 0
                else:
                    p1 = (self.checkPointLeft[0] * 4, self.checkPointLeft[1] * 4)
                    delta_x = math.dist(p1, self.currentPosition * 4) - self.disCP
                    delta_v = 0

            self.sqrt_ab = 2 * math.sqrt(self.a_max * self.b_max)
            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        elif not self.isCarInCrossing(self, maxX=55, minY=22, maxY=25) and self.trafficSignal.state != "green":
            delta_x = math.dist(self.checkPoint * 4, self.currentPosition * 4) - self.disCP
            delta_v = self.v - 0

            self.sqrt_ab = 2 * math.sqrt(self.a_max * self.b_max)
            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        elif self.turnState == "left" and self.isCarInCrossing(self, minX=33, maxX=55, minY=18, maxY=35) and self.isLeftCarsInCrossing(self.leftCars) and self.leftCars[0].trafficSignal.state == "green":
            if self.isCarInCrossing(leadLeftCar):
                delta_x = math.dist(leadLeftCar.currentPosition * 4, self.currentPosition * 4) - (
                        self.l + lengthFactor)
                delta_v = self.v - leadLeftCar.v
            else:
                p1 = (self.checkPointLeft[0] * 4, self.checkPointLeft[1] * 4)
                delta_x = math.dist(p1, self.currentPosition * 4) - self.disCP
                delta_v = 0
            self.sqrt_ab = 2 * math.sqrt(self.a_max * self.b_max)
            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        return alpha

    # resize car image
    @staticmethod
    def resizeImage(img, new_width, new_height):
        return pygame.transform.scale(img, (new_width, new_height))

    def toTurn(self):
        distanceStart = math.dist(self.currentPosition * self.ppu, self.startCurvePoint * self.ppu)
        distanceEnd = math.dist(self.currentPosition * self.ppu, self.endCurvePoint * self.ppu)
        if distanceStart < self.turnDistance:
            return True
        if distanceEnd < self.turnDistance:
            self.steering = 360
            self.angle = self.exitAngle
            return False

        return False
