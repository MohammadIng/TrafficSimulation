from threading import Thread
from time import sleep



class UpdateTime:

    def __init__(self, sim, simulationTime, cars, trafficSignals, statisticsHandler,  simulationProperties):
        self.toSimulation = True
        self.duration = 0
        self.simulationTime = simulationTime
        self.thread = Thread(target=self.update, args=(sim, cars, trafficSignals))
        self.thread.start()
        self.statisticsHandler = statisticsHandler
        self.simulationProperties = simulationProperties

    def stop(self):
        self.toSimulation = False
        self.thread.join()

    def update(self, sim, cars=None, trafficSignals=None):
        while self.toSimulation:
            self.allTrafficSignalUpdate(trafficSignals)
            for road in cars:
                for car in cars[road]:
                    if car.arrivalTime > 1:
                        car.arrivalTime -= 1
            self.duration += 1
            if self.duration >= self.simulationTime and self.toSimulation:
                sim.exit = True
                self.statisticsHandler.calculateStatistics(cars, self.simulationProperties)
                break
            sleep(1)

    def allTrafficSignalUpdate(self, trafficSignals):
        for index in range(len(trafficSignals)):
            ts = trafficSignals[index]
            ts.trafficSignalUpdate(ts.time)

