import os

import pygame
from generator import Generator
from trafficSignal import TrafficSignal
from carIDM import Car
from UpdateTime import UpdateTime
from Statistics import StatisticsHandler


class Simulation:
    def __init__(self, width=1500, height=750, visualization=pygame.SHOWN, carVelocity=20, trafficTimes="realTime"):
        pygame.init()
        pygame.display.set_caption("Traffic Simulation")
        self.screen = pygame.display.set_mode((width, height), flags=visualization)
        self.backGroundRoad = pygame.image.load('street.png')
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.ppu = 15
        self.exit = False
        self.visualization = visualization
        self.carVelocity = carVelocity
        self.simulationTime = 900
        self.simulationProperties = None
        self.simulationProperties = {"Simulation Time": self.simulationTime, "Simulation Sort": "with visualization"}
        if visualization == pygame.HIDDEN:
            self.simulationProperties = {"Simulation Time": self.simulationTime,
                                         "Simulation Sort": "without visualization"}
        self.trafficTimes = trafficTimes

    def getAllTrafficSignal(self):
        ts1 = TrafficSignal((725, 175), state="red", lastState="yellow", redTime=55, yellowTime=3, greenTime=61,
                            time=39)

        ts2 = TrafficSignal((910, 175), state="green", lastState="yellow", redTime=103, yellowTime=3, greenTime=13,
                            time=9)

        ts3 = TrafficSignal((500, 520), state="green", lastState="yellow", redTime=103, yellowTime=3, greenTime=13,
                            time=9)

        ts4 = TrafficSignal((725, 550), state="red", lastState="yellow", redTime=105, yellowTime=3, greenTime=11,
                            time=18)

        ts5 = TrafficSignal((930, 540), state="red", lastState="yellow", redTime=37, yellowTime=3, greenTime=79,
                            time=19)

        self.trafficTimes = "realTime"

        return ts1, ts2, ts3, ts4, ts5

    def getAllTrafficSignalHalfTimes(self):
        ts1 = TrafficSignal((725, 175), state="red", lastState="yellow", redTime=25, yellowTime=3, greenTime=32,
                            time=20)

        ts2 = TrafficSignal((910, 175), state="green", lastState="yellow", redTime=48, yellowTime=3, greenTime=9,
                            time=5)

        ts3 = TrafficSignal((500, 520), state="green", lastState="yellow", redTime=48, yellowTime=3, greenTime=9,
                            time=5)

        ts4 = TrafficSignal((725, 550), state="red", lastState="yellow", redTime=50, yellowTime=3, greenTime=7,
                            time=10)

        ts5 = TrafficSignal((930, 540), state="red", lastState="yellow", redTime=19, yellowTime=3, greenTime=38,
                            time=10)

        self.trafficTimes = "halfTime"

        return ts1, ts2, ts3, ts4, ts5

    def getAllTrafficSignalQuarterTimes(self):
        ts1 = TrafficSignal((725, 175), state="red", lastState="yellow", redTime=15, yellowTime=2, greenTime=23,
                            time=10)

        ts2 = TrafficSignal((910, 175), state="green", lastState="yellow", redTime=25, yellowTime=2, greenTime=13,
                            time=5)

        ts3 = TrafficSignal((500, 520), state="green", lastState="yellow", redTime=25, yellowTime=2, greenTime=13,
                            time=5)

        ts4 = TrafficSignal((725, 550), state="red", lastState="yellow", redTime=31, yellowTime=2, greenTime=7,
                            time=1)

        ts5 = TrafficSignal((930, 540), state="red", lastState="yellow", redTime=11, yellowTime=2, greenTime=27,
                            time=7)

        self.trafficTimes = "quarterTime"

        return ts1, ts2, ts3, ts4, ts5

    @staticmethod
    def allTrafficSignalDraw(surface, trafficSignals):
        for ts in trafficSignals:
            ts.trafficSignalDraw(surface)

    def getInitAllTrafficSignal(self):
        if self.trafficTimes == "quarterTime":
            return self.getAllTrafficSignalQuarterTimes()
        elif self.trafficTimes == "halfTime":
            return self.getAllTrafficSignalHalfTimes()
        return self.getAllTrafficSignal()

    def run(self, round=0):

        window = pygame.display.set_mode((self.width, self.height), flags=self.visualization)

        car_image = pygame.image.load(os.path.join(os.getcwd(), "car.png"))
        car_image = Car.resizeImage(car_image, 50, 50)

        truck_image = pygame.image.load(os.path.join(os.getcwd(), "truck.png"))
        truck_image = Car.resizeImage(truck_image, 80, 30)

        image = {False: car_image, True: truck_image}
        gen = Generator(self.carVelocity)
        trafficSignals = self.getInitAllTrafficSignal()
        print(self.trafficTimes)

        currentTime = round
        self.simulationTime = 900
        gen.generatorCars(currentTime, self.simulationTime)
        statisticsHandler = StatisticsHandler()
        self.simulationProperties["currentTime"] = currentTime
        self.simulationProperties["trafficTime"] = self.trafficTimes

        updateTime = UpdateTime(self, self.simulationTime + 420, gen.allCars, trafficSignals, statisticsHandler,
                                self.simulationProperties)

        print("Simulation at ", currentTime + 1, " Time with ", self.trafficTimes, " as trafficProgram")
        while not self.exit:
            dt = self.clock.get_time() / 1000

            # events in pygame
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    self.exit = True

            background_Color = (255, 255, 255)
            self.screen.fill(background_Color)

            # road show on the screen
            window.blit(self.backGroundRoad, (0, 0))

            int(self.clock.tick(self.ticks) / 100)

            self.allTrafficSignalDraw(self.screen, trafficSignals)

            for road in gen.allCars:
                left = 0
                for index in range(len(gen.allCars[road])):
                    car = gen.allCars[road][index]
                    if car.arrivalTime <= 1:
                        leadCar = None
                        leadLeftCar = None
                        if index > 0:
                            leadCar = gen.allCars[road][index - 1]
                            if car.turnState == "left":
                                leadLeftCar = gen.allCars[road][left]
                                left = index

                        car.car_Driving(dt, leadCar=leadCar, leadLeftCar=leadLeftCar)
                        car.trafficSignal = trafficSignals[car.trafficSignalIndex]
                        rotated = pygame.transform.rotate(image[car.isTruck], car.angle)
                        rect = rotated.get_rect()
                        self.screen.blit(rotated, pygame.Vector2(car.currentPosition) * self.ppu - (
                        rect.width / 2, rect.height / 2))

                        statisticsHandler.calculateCarStatistics(car)
                        statisticsHandler.calculateTrafficStatistics(car)

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()
        updateTime.stop()


def getSimulationProperties():
    trafficTime = int(input("wich trafficProgram: 0 realTime, 1 halfTime, 2 quarterTime?       "))

    if trafficTime == 1:
        trafficTime = "halfTime"
    elif trafficTime == 2:
        trafficTime = "quarterTime"
    else:
        trafficTime = "realTime"
    return trafficTime


# Run the code
if __name__ == '__main__':

    trafficTime = getSimulationProperties()
    for i in range(0, 20):
        simulation = Simulation(width=1500, height=750, trafficTimes=trafficTime)
        simulation.run(i)
