import pygame


class TrafficSignal:

    def __init__(self, position=(0, 0), time=100, redTime=200, yellowTime=50, greenTime=130, state="red",
                 lastState="yellow"):
        self.position = position
        self.time = time
        self.redTime = redTime
        self.yellowTime = yellowTime
        self.greenTime = greenTime
        self.state = state
        self.lastState = lastState
        self.redRounds = 0 if self.state != "red" else 1

    def trafficSignalDraw(self, surface):
        width = 10
        height = 20
        points = [(self.position[0] + width, self.position[1] + height),
                  (self.position[0] + width, self.position[1] - height),
                  (self.position[0] - width, self.position[1] - height),
                  (self.position[0] - width, self.position[1] + height)]

        p1 = points[0]
        p2 = points[1]
        p3 = points[2]
        p4 = points[3]

        width = 3
        pygame.draw.line(surface, "black", p1, p2, width)
        pygame.draw.line(surface, "black", p2, p3, width)
        pygame.draw.line(surface, "black", p3, p4, width)
        pygame.draw.line(surface, "black", p4, p1, width)

        stateDraw = {"yellow": ["yellow", self.position], "red": ["red", (self.position[0], self.position[1] - 12)],
                     "green": ["green", (self.position[0], self.position[1] + 12)]}
        pygame.draw.circle(surface, stateDraw[self.state][0], stateDraw[self.state][1], 5)

    def trafficSignalUpdate(self, time):
        if self.state == "red":
            if time <= 0:
                self.time = self.yellowTime
                self.state = "yellow"
                self.lastState = "red"

            else:
                self.time -= 1

        elif self.state == "yellow":
            if time <= 0 and self.lastState == "red":
                self.time = self.greenTime
                self.state = "green"
                self.lastState = "yellow"
            elif time <= 0 and self.lastState == "green":
                self.time = self.redTime
                self.state = "red"
                self.lastState = "yellow"
                self.redRounds += 1
            else:
                self.time -= 1


        elif self.state == "green":
            if time <= 0:
                self.time = self.yellowTime
                self.state = "yellow"
                self.lastState = "green"
            else:
                self.time -= 1
