import math
import os
from datetime import datetime
from statistics import mean
import xlsxwriter
import matplotlib.pyplot as plt
from pygame import Vector2




class Statistics:
    def __init__(self, roadID=None):
        self.roadID = roadID
        self.stRealDriveSpan = 0
        self.velocityAverage = 0
        self.stStartPoint = Vector2(0, 0)
        self.stExitPoint = Vector2(0, 0)
        self.stArrivalTime = 0
        self.stExitTime = 0
        self.stGeneralDriveSpan = 0
        self.stCheckArrivalTime = True
        self.stCheckExitTime = True
        self.stStartStopTimes = []
        self.stEndStopTimes = []
        self.stCheckStartStopTime = True
        self.stCheckEndStopTime = False
        self.stStopSpan = 0
        self.stCheckStopAtSignal = True

        if self.roadID:
            self.setAllValues()

    def setAllValues(self):
        values = self.getAllValues()[self.roadID]
        self.stStartPoint = values["startPoint"]
        self.stExitPoint = values["exitPoint"]

    def getAllValues(self):
        dic = {
            "vehicle1_1_6_1": {
                "startPoint": (42 * 15, 0 * 15),
                "exitPoint": Vector2(42 * 15, 50 * 15)
            },
            "vehicle1_2_6_2": {
                "startPoint": Vector2(45 * 15, 0),
                "exitPoint": Vector2(45 * 15, 50 * 15)
            },
            "vehicle7_4": {
                "startPoint": Vector2(0, 30 * 15),
                "exitPoint": Vector2(100 * 15, 30 * 15)
            },
            "vehicle5_2_2": {
                "startPoint": Vector2(55 * 15, 50 * 15),
                "exitPoint": Vector2(55 * 15, 0)
            },
            "vehicle3_2_8": {
                "startPoint": Vector2(100 * 15, 25 * 15),
                "exitPoint": Vector2(0, 25 * 15)
            },

            "vehicle1_1_8": {
                "startPoint": Vector2(42 * 15, 0),
                "exitPoint": Vector2(0, 25 * 15)
            },
            "vehicle7_6_1": {
                "startPoint": Vector2(0 * 15, 30 * 15),
                "exitPoint": Vector2(42 * 15, 50 * 15)
            },
            "vehicle5_1_4": {
                "startPoint": Vector2(58 * 15, 50 * 15),
                "exitPoint": Vector2(100 * 15, 30 * 15)
            },
            "vehicle3_1_2": {
                "startPoint": Vector2(100 * 15, 20 * 15),
                "exitPoint": Vector2(55 * 15, 0)
            },

            "vehicle1_2_4": {
                "startPoint": Vector2(45 * 15, 0),
                "exitPoint": Vector2(100 * 15, 30 * 15)
            },
            "vehicle7_2": {
                "startPoint": Vector2(0, 30 * 15),
                "exitPoint": Vector2(55 * 15, 0)},
            "vehicle3_2_6_2": {
                "startPoint": Vector2(100 * 15, 25 * 15),
                "exitPoint": Vector2(45 * 15, 50 * 15)
            },
            "vehicle5_3_8": {
                "startPoint": Vector2(52 * 15, 50 * 15),
                "exitPoint": Vector2(0, 25 * 15)
            },
        }

        return dic


class StatisticsHandler:

    def __init__(self):
        self.allRoads = [
            "vehicle1_1_6_1",
            "vehicle1_2_6_2",
            "vehicle7_4",
            "vehicle5_2_2",
            "vehicle3_2_8",

            "vehicle1_1_8",
            "vehicle7_6_1",
            "vehicle5_1_4",
            "vehicle3_1_2",

            "vehicle1_2_4",
            "vehicle7_2",
            "vehicle3_2_6_2",
            "vehicle5_3_8"]

        self.newAllCars = {}
        for road in self.allRoads:
            self.newAllCars[road] = []

        self.driveTimes = {}
        self.numberOfCarsAtTrafficSignal = {0: [], 1: [], 2: [], 3: [], 4: []}

        self.allDrivesTime = {}
        for road in self.allRoads:
            data = {"numberOfCars": 0, "generalDriveSpan": 0, "stopSpan": 0, "realStopSpan": 0, "realDriveSpan": 0}
            self.allDrivesTime[road] = data

    def calculateTrafficStatistics(self, car):
        index = len(self.numberOfCarsAtTrafficSignal[car.trafficSignalIndex]) - 1
        if car.trafficSignal.redRounds != len(self.numberOfCarsAtTrafficSignal[car.trafficSignalIndex]):
            self.numberOfCarsAtTrafficSignal[car.trafficSignalIndex].append(0)

        if not car.statistic.stCheckArrivalTime and car.statistic.stCheckExitTime and car.steering != car.curveAngle and car.v < 1 and car.trafficSignal.state == "red":
            if car.statistic.stCheckStopAtSignal:
                self.numberOfCarsAtTrafficSignal[car.trafficSignalIndex][index] += 1
                car.statistic.stCheckStopAtSignal = False

    def calculateCarStatistics(self, car):
        pos = (car.currentPosition[0] * 15, car.currentPosition[1] * 15)

        if math.dist(pos, car.statistic.stStartPoint) < 10 and car.statistic.stCheckArrivalTime:
            car.statistic.stCheckArrivalTime = False
            car.statistic.stArrivalTime = datetime.now()

        if math.dist(pos, car.statistic.stExitPoint) < 10 and car.statistic.stCheckExitTime:
            car.statistic.stExitTime = datetime.now()
            car.statistic.stCheckExitTime = False
            car.statistic.stGeneralDriveSpan = (car.statistic.stExitTime - car.statistic.stArrivalTime).total_seconds()
            for i in range(len(car.statistic.stStartStopTimes)):
                d = (car.statistic.stEndStopTimes[i] - car.statistic.stStartStopTimes[i]).total_seconds()
                car.statistic.stStopSpan += d
            car.statistic.stRealDriveSpan = car.statistic.stGeneralDriveSpan - car.statistic.stStopSpan

        if not car.statistic.stCheckArrivalTime and car.statistic.stCheckExitTime:
            if car.v < 1 and car.statistic.stCheckStartStopTime:
                car.statistic.stCheckStartStopTime = False
                car.statistic.stCheckEndStopTime = True
                car.statistic.stStartStopTimes.append(datetime.now())


            elif car.v > 1 and car.statistic.stCheckEndStopTime:
                car.statistic.stCheckStartStopTime = True
                car.statistic.stCheckEndStopTime = False
                car.statistic.stEndStopTimes.append(datetime.now())

    def calculateStatistics(self, allCars, simulationProperties):

        for road in allCars:
            for car in allCars[road]:
                self.newAllCars[car.road].append(car)

        for road in self.newAllCars:
            generalDriveSpan = []
            stopSpan = []
            realStopSpan = []
            realDriveSpan = []
            avgGeneralDriveSpan = 0
            avgStopSpan = 0
            avgRealStopSpan = 0
            avgRealDriveSpan = 0
            if len(self.newAllCars[road]) != 0:
                for car in self.newAllCars[road]:
                    generalDriveSpan.append(car.statistic.stGeneralDriveSpan)
                    stopSpan.append(car.statistic.stStopSpan)
                    realDriveSpan.append(car.statistic.stRealDriveSpan)
                    if car.statistic.stStopSpan != 0:
                        realStopSpan.append(car.statistic.stStopSpan)
                avgGeneralDriveSpan = mean(generalDriveSpan)
                avgStopSpan = mean(stopSpan)
                if len(realStopSpan) != 0:
                    avgRealStopSpan = mean(realStopSpan)
                avgRealDriveSpan = mean(realDriveSpan)
            times = {"numberOfCars": len(self.newAllCars[road]), "generalDriveSpan": round(avgGeneralDriveSpan, 2),
                     "stopSpan": round(avgStopSpan, 2), "realStopSpan": round(avgRealStopSpan, 2),
                     "realDriveSpan": round(avgRealDriveSpan, 2)}

            self.driveTimes[road] = times

        self.saveDateInExcel(simulationProperties)
        self.barDigramDraw(path="output/" + str(simulationProperties["trafficTime"]) + "/" + str(
            simulationProperties["currentTime"]) + "/numberOfCars.png", title="numberOfCars", xLabel="road",
                           yLabel="numberOfCars", data=self.getDriveData("numberOfCars"))
        self.barDigramDraw(path="output/" + str(simulationProperties["trafficTime"]) + "/" + str(
            simulationProperties["currentTime"]) + "/generalDriveSpan.png", title="generalDriveSpan", xLabel="road",
                           yLabel="average of generalDriveSpan in S ", data=self.getDriveData("generalDriveSpan"))
        self.barDigramDraw(path="output/" + str(simulationProperties["trafficTime"]) + "/" + str(
            simulationProperties["currentTime"]) + "/stopSpan.png", title="stopSpan", xLabel="road",
                           yLabel="average of stopSpan in S", data=self.getDriveData("stopSpan"))
        self.barDigramDraw(path="output/" + str(simulationProperties["trafficTime"]) + "/" + str(
            simulationProperties["currentTime"]) + "/realStopSpan.png", title="realStopSpan", xLabel="road",
                           yLabel="average of realStopSpan in S", data=self.getDriveData("realStopSpan"))
        self.barDigramDraw(path="output/" + str(simulationProperties["trafficTime"]) + "/" + str(
            simulationProperties["currentTime"]) + "/realDriveSpan.png", title="realDriveSpan", xLabel="road",
                           yLabel="average of realDriveSpan in S", data=self.getDriveData("realDriveSpan"))

    def getDriveData(self, key):
        l1 = []
        data = [key]
        l2 = []
        for road in self.allRoads:
            l1.append(self.driveTimes[road][key])
            r = road.replace("vehicle", "road")
            l2.append(r)

        data.append(l2)
        data.append(l1)
        return data

    def printData(self):
        print(self.driveTimes)
        print(self.numberOfCarsAtTrafficSignal)
        pass

    def saveDateInExcel(self, simulationProperties):
        if not os.path.isdir(
                'output/' + str(simulationProperties["trafficTime"]) + "/" + str(simulationProperties['currentTime'])):
            os.makedirs(
                'output/' + str(simulationProperties["trafficTime"]) + "/" + str(simulationProperties['currentTime']))

        workbook = xlsxwriter.Workbook('output/' + str(simulationProperties["trafficTime"]) + "/" + str(
            simulationProperties['currentTime']) + '/statisticsResult.xlsx')
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, "Simulation Output")
        worksheet.write(2, 0)

        i1 = 3
        j1 = 0

        for k in (simulationProperties.keys()):
            worksheet.write(i1, j1, k)
            j1 += 1
            worksheet.write(i1, j1, simulationProperties[k])
            i1 += 1
            j1 = 0

        worksheet.write(len(simulationProperties.keys()) + 5, 1, "numberOfCars")
        worksheet.write(len(simulationProperties.keys()) + 5, 2, "generalDriveSpan")
        worksheet.write(len(simulationProperties.keys()) + 5, 3, "stopSpan")
        worksheet.write(len(simulationProperties.keys()) + 5, 4, "realStopSpan")
        worksheet.write(len(simulationProperties.keys()) + 5, 5, "realDriveSpan")
        i1 = len(simulationProperties.keys()) + 6
        j1 = 1
        for i in self.driveTimes:
            worksheet.write(i1, 0, i)
            for j in self.driveTimes[i]:
                worksheet.write(i1, j1, self.driveTimes[i][j])
                j1 += 1
                if j1 == len(self.driveTimes[i]) + 1:
                    j1 = 1
            i1 += 1

        index_round = len(self.driveTimes) + len(simulationProperties.keys()) + 10
        maxCarLen = 0
        for i in self.numberOfCarsAtTrafficSignal:
            if (len(self.numberOfCarsAtTrafficSignal[i]) > maxCarLen):
                maxCarLen = len(self.numberOfCarsAtTrafficSignal[i])
        worksheet.write(index_round, 0, "index/round")
        worksheet.write(index_round, maxCarLen + 2, "max")
        worksheet.write(index_round, maxCarLen + 3, "min")
        worksheet.write(index_round, maxCarLen + 4, "avg")

        car_i = len(self.driveTimes) + len(simulationProperties.keys()) + 11

        for i in self.numberOfCarsAtTrafficSignal:
            worksheet.write(car_i, 0, i)
            car_j = 1

            for j in self.numberOfCarsAtTrafficSignal[i]:
                worksheet.write(car_i, car_j, j)
                car_j += 1
            worksheet.write(car_i, maxCarLen + 2, max(self.numberOfCarsAtTrafficSignal[i]) if len(
                self.numberOfCarsAtTrafficSignal[i]) != 0 else None)
            worksheet.write(car_i, maxCarLen + 3, min(self.numberOfCarsAtTrafficSignal[i]) if len(
                self.numberOfCarsAtTrafficSignal[i]) != 0 else None)
            worksheet.write(car_i, maxCarLen + 4, mean(self.numberOfCarsAtTrafficSignal[i]) if len(
                self.numberOfCarsAtTrafficSignal[i]) != 0 else None)
            car_i += 1
        for i in range(maxCarLen):
            worksheet.write(index_round, i + 1, i)

        workbook.close()

    def barDigramDraw(self, path="output/test/path.png", title="test", xLabel="x", yLabel="y", data=[]):
        plt.bar(data[1], data[2])
        plt.title(title)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.xticks(range(len(data[1])), data[1], rotation=90)
        plt.subplots_adjust(bottom=0.25)
        if title == "numberOfCars":
            plt.yticks(range(0, 180, 10))

        def addLabels(x, y):
            for i in range(len(x)):
                plt.text(i, y[i], y[i])

        addLabels(data[1], data[2])
        plt.savefig(path)
        plt.show()
