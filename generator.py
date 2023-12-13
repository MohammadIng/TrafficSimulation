import numpy as np
import xlrd as xls

from Statistics import Statistics
from carIDM import Car
from vehicle import Vehicle


class Generator:
    def __init__(self, carVelocity=20):
        self.allCars = {
            "vehicle1_1_6_1": [],
            "vehicle1_2_6_2": [],
            "vehicle7_4": [],
            "vehicle5_2_2": [],
            "vehicle3_2_8": [],

            "vehicle1_1_8": [],
            "vehicle7_6_1": [],
            "vehicle5_1_4": [],
            "vehicle3_1_2": [],

            "vehicle1_2_4": [],
            "vehicle7_2": [],
            "vehicle3_2_6_2": [],
            "vehicle5_3_8": [],
        }

        self.tmpAllCars = {
            "vehicle1_1_6_1": [],
            "vehicle1_2_6_2": [],
            "vehicle7_4": [],
            "vehicle5_2_2": [],
            "vehicle3_2_8": [],

            "vehicle1_1_8": [],
            "vehicle7_6_1": [],
            "vehicle5_1_4": [],
            "vehicle3_1_2": [],

            "vehicle1_2_4": [],
            "vehicle7_2": [],
            "vehicle3_2_6_2": [],
            "vehicle5_3_8": [],
        }
        self.roads = [
            "vehicle1_2_4",
            "vehicle1_1_6_1",
            "vehicle1_2_6_2",
            "vehicle1_1_8",

            "vehicle3_1_2",
            "vehicle3_2_6_2",
            "vehicle3_2_8",

            "vehicle5_2_2",
            "vehicle5_1_4",
            "vehicle5_3_8",

            "vehicle7_2",
            "vehicle7_4",
            "vehicle7_6_1",
        ]
        self.carVelocity = carVelocity
        self.CarsData = self.getCarsTrucksData(n=1)
        self.TrucksData = self.getCarsTrucksData(n=2)

    def getCarsTrucksData(self, n):
        workbook = xls.open_workbook('TrafficData.xls')
        worksheet = workbook.sheet_by_name('Sheet2')
        times_car = [[0 for x in range(12)] for y in range(20)]
        for i in range(0, len(times_car)):
            for j in range(0, len(times_car[0])):
                y = i + 4 + j * 23
                times_car[i][j] = int(worksheet.cell(y, n).value)
        return times_car

    @staticmethod
    def getExpDistribution(time=900, numberOfCars=1):
        t0 = 0
        arrival_queue = []
        inter_arrival_times = np.random.exponential(time / numberOfCars, numberOfCars)
        for t in inter_arrival_times:
            t0 += t
            arrival_queue.append(int(t0))
        return sorted(arrival_queue)

    @staticmethod
    def object_Translate(car, x=0, y=0):
        car.currentPosition = (car.currentPosition.x + x, car.currentPosition.y + y)
        return car

    def createCar(self, vehicles, road, arrivalTime, isTruck=False):
        car = Car()
        car.currentPosition = vehicles[road].startPoint
        car.angle = vehicles[road].startAngle
        car.isTurn = vehicles[road].isTurn
        car.checkPoint = vehicles[road].checkPoint
        car.startCurvePoint = vehicles[road].startCurvePoint
        car.endCurvePoint = vehicles[road].endCurvePoint
        car.curveAngle = vehicles[road].curveAngle
        car.exitAngle = vehicles[road].exitAngle
        car.turnState = vehicles[road].turnState
        car.leftRoad = vehicles[road].leftRoad
        car.checkPointLeft = vehicles[road].checkPointLeft
        car.trafficSignalIndex = vehicles[road].trafficSignalIndex
        car = self.object_Translate(car)
        car.arrivalTime = arrivalTime
        initRoad = self.addCarToList(car, road)
        car.road = initRoad
        car.isTruck = isTruck
        car.v_max = self.carVelocity
        if isTruck:
            car.v_max = self.carVelocity - 5
            car.l = 20
            car.disCP = 10
        car.statistic = Statistics(roadID=car.road)

    def generatorCars(self, currentTime, simulationTime):
        vehicle = Vehicle()
        vehicles = vehicle.getAllRoads()

        currentCars = self.CarsData[currentTime]
        v = int(currentCars[1] / 2)
        currentCars.insert(1, v)
        currentCars[2] = currentCars[1] + v % 2

        for road in range(0, len(self.roads)):
            if currentCars[road] != 0:
                times = self.getExpDistribution(time=simulationTime, numberOfCars=currentCars[road])
                for t in times:
                    self.createCar(vehicles, self.roads[road], t)

        currentTrucks = self.TrucksData[currentTime]
        v = int(currentTrucks[1] / 2)
        currentTrucks.insert(1, v)
        currentTrucks[2] = currentTrucks[1] + v % 2
        #
        for road in range(0, len(self.roads)):
            if currentTrucks[road] != 0:
                times = self.getExpDistribution(time=simulationTime, numberOfCars=currentTrucks[road])
                for t in times:
                    self.createCar(vehicles, self.roads[road], t, isTruck=True)

        for road in self.allCars:
            self.allCars[road] = sorted(self.allCars[road], key=lambda car: car.arrivalTime)
            for car in self.allCars[road]:
                self.tmpAllCars[car.road].append(car)

        leftRoads = ["vehicle1_2_6_2", "vehicle7_4", "vehicle3_2_8", "vehicle5_3_8"]
        for road in leftRoads:
            for car in self.allCars[road]:
                for leftRoad in car.leftRoad:
                    for leftCar in self.tmpAllCars[leftRoad]:
                        car.leftCars.append(leftCar)

    def addCarToList(self, car, road):
        if road == "vehicle1_1_6_1" or road == "vehicle1_1_8":
            self.allCars["vehicle1_1_6_1"].append(car)

        elif road == "vehicle1_2_6_2" or road == "vehicle1_2_4":
            self.allCars["vehicle1_2_6_2"].append(car)

        elif road == "vehicle7_6_1" or road == "vehicle7_4" or road == "vehicle7_2":
            self.allCars["vehicle7_4"].append(car)

        elif road == "vehicle3_2_6_2" or road == "vehicle3_2_8":
            self.allCars["vehicle3_2_8"].append(car)
        else:
            self.allCars[road].append(car)
        return road
