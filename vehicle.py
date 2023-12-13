from pygame import Vector2
from trafficSignal import TrafficSignal
from Statistics import Statistics


class Vehicle:

    def __init__(self, startPoint=Vector2(0, 0), startAngle=90, exitAngle=0, steering=360,
                 isTurn=False,
                 startCurvePoint=Vector2(0, 0), endCurvePoint=Vector2(0, 0), checkPoint=Vector2(0, 0), curveAngle=0,
                 trafficSignalIndex=0, trafficSignal=TrafficSignal(), turnState="right", leftRoad=[],
                 checkPointLeft=(0, 0), statistic=Statistics()):
        self.startPoint = startPoint
        self.startAngle = startAngle
        self.exitAngle = exitAngle
        self.steering = steering
        self.isTurn = isTurn
        self.turnState = turnState
        self.startCurvePoint = startCurvePoint
        self.endCurvePoint = endCurvePoint
        self.curveAngle = curveAngle
        self.checkPoint = checkPoint
        self.trafficSignalIndex = trafficSignalIndex
        self.trafficSignal = trafficSignal
        self.arrivalTime = 0
        self.road = ""
        self.leftRoad = leftRoad
        self.leftCars = []
        self.checkPointLeft = checkPointLeft
        self.image = "car.png"
        self.isTruck = False
        self.disCP = 1
        self.statistic = statistic

    @staticmethod
    def getAllRoads():
        startPoint1_1 = Vector2(42, -50)
        startPoint1_2 = Vector2(45, -50)

        startPoint3_1 = Vector2(150, 20)
        startPoint3_2 = Vector2(150, 25)

        startPoint5_1 = Vector2(58, 150)
        startPoint5_2 = Vector2(55, 150)
        startPoint5_3 = Vector2(52, 150)

        startPoint7 = Vector2(-50, 30)

        checkPoint1_1 = Vector2(42, 18)
        startCurvePoint1_1 = Vector2(42, 20)

        checkPoint1_2 = Vector2(45, 18)
        startCurvePoint1_2 = Vector2(45, 18)

        endCurvePoint2Right = Vector2(55, 10)
        endCurvePoint2Left = Vector2(55, 10)

        checkPoint3_1 = Vector2(61, 20)
        startCurvePoint3_1 = Vector2(62, 20)
        checkPoint3_2 = Vector2(61, 25)
        startCurvePoint3_2 = Vector2(56, 25)

        endCurvePoint4Right = Vector2(66, 30)
        endCurvePoint4Left = Vector2(61, 30)

        checkPoint5_1 = Vector2(58, 35)
        startCurvePoint5_1 = Vector2(58, 35)
        checkPoint5_2 = Vector2(55, 35)
        checkPoint5_3 = Vector2(52, 35)
        startCurvePoint5_3 = Vector2(52, 33)

        endCurvePoint6_1 = Vector2(42, 42)
        endCurvePoint6_2 = Vector2(45, 39)

        checkPoint7 = Vector2(33, 30)
        startCurvePoint7Left = Vector2(38, 30)
        startCurvePoint7Right = Vector2(33, 30)

        endCurvePoint8Right = Vector2(33, 25)
        endCurvePoint8Left = Vector2(40, 25)

        # straight Roads
        vehicle1_1_6_1 = Vehicle(startPoint=startPoint1_1, startAngle=-90, isTurn=False,
                                 checkPoint=checkPoint1_1, trafficSignalIndex=0)
        vehicle1_2_6_2 = Vehicle(startPoint=startPoint1_2, startAngle=-90, isTurn=False,
                                 checkPoint=checkPoint1_2, trafficSignalIndex=0)
        vehicle7_4 = Vehicle(startPoint=startPoint7, startAngle=0, isTurn=False,
                             checkPoint=checkPoint7, trafficSignalIndex=2)
        vehicle5_2_2 = Vehicle(startPoint=startPoint5_2, startAngle=90, isTurn=False,
                               checkPoint=checkPoint5_2, trafficSignalIndex=4)
        vehicle3_2_8 = Vehicle(startPoint=startPoint3_2, startAngle=180, isTurn=False,
                               checkPoint=checkPoint3_2, trafficSignalIndex=1)

        # curved right Roads
        vehicle1_1_8 = Vehicle(startPoint=startPoint1_1, startAngle=-90, isTurn=True,
                               startCurvePoint=startCurvePoint1_1, endCurvePoint=endCurvePoint8Right,
                               checkPoint=checkPoint1_1, curveAngle=-35, exitAngle=180, trafficSignalIndex=0)
        vehicle7_6_1 = Vehicle(startPoint=startPoint7, startAngle=0, isTurn=True,
                               startCurvePoint=startCurvePoint7Right, endCurvePoint=endCurvePoint6_1,
                               checkPoint=checkPoint7, curveAngle=-22, exitAngle=-90, trafficSignalIndex=2)
        vehicle5_1_4 = Vehicle(startPoint=startPoint5_1, startAngle=90, isTurn=True,
                               startCurvePoint=startCurvePoint5_1, endCurvePoint=endCurvePoint4Right,
                               checkPoint=checkPoint5_1, curveAngle=-35, exitAngle=0, trafficSignalIndex=4)
        vehicle3_1_2 = Vehicle(startPoint=startPoint3_1, startAngle=180, isTurn=True,
                               startCurvePoint=startCurvePoint3_1, endCurvePoint=endCurvePoint2Right,
                               checkPoint=checkPoint3_1, curveAngle=-27, exitAngle=90, trafficSignalIndex=1)

        # curved left Roads
        vehicle1_2_4 = Vehicle(startPoint=startPoint1_2, startAngle=-90, isTurn=True,
                               startCurvePoint=startCurvePoint1_2, endCurvePoint=endCurvePoint4Left,
                               checkPoint=checkPoint1_2, curveAngle=17, exitAngle=0, trafficSignalIndex=0,
                               turnState="left", leftRoad=["vehicle5_2_2", "vehicle5_1_4"], checkPointLeft=(50, 27))
        vehicle7_2 = Vehicle(startPoint=startPoint7, startAngle=0, isTurn=True,
                             startCurvePoint=startCurvePoint7Left, endCurvePoint=endCurvePoint2Left,
                             checkPoint=checkPoint7, curveAngle=12.4, exitAngle=90, trafficSignalIndex=2,
                             turnState="left", leftRoad=["vehicle3_2_8", "vehicle3_1_2"], checkPointLeft=(45, 28))
        vehicle3_2_6_2 = Vehicle(startPoint=startPoint3_2, startAngle=180, isTurn=True,
                                 startCurvePoint=startCurvePoint3_2, endCurvePoint=endCurvePoint6_2,
                                 checkPoint=checkPoint3_2, curveAngle=18.5, exitAngle=-90, trafficSignalIndex=1,
                                 turnState="left", leftRoad=["vehicle7_4"], checkPointLeft=(49, 28))
        vehicle5_3_8 = Vehicle(startPoint=startPoint5_3, startAngle=90, isTurn=True,
                               startCurvePoint=startCurvePoint5_3, endCurvePoint=endCurvePoint8Left,
                               checkPoint=checkPoint5_3, curveAngle=24.5, exitAngle=180, trafficSignalIndex=3,
                               turnState="left", leftRoad=[], checkPointLeft=(0, 0))

        vehicles = {
            "vehicle1_1_6_1": vehicle1_1_6_1,
            "vehicle1_2_6_2": vehicle1_2_6_2,
            "vehicle7_4": vehicle7_4,
            "vehicle5_2_2": vehicle5_2_2,
            "vehicle3_2_8": vehicle3_2_8,

            "vehicle1_1_8": vehicle1_1_8,
            "vehicle7_6_1": vehicle7_6_1,
            "vehicle5_1_4": vehicle5_1_4,
            "vehicle3_1_2": vehicle3_1_2,

            "vehicle1_2_4": vehicle1_2_4,
            "vehicle7_2": vehicle7_2,
            "vehicle3_2_6_2": vehicle3_2_6_2,
            "vehicle5_3_8": vehicle5_3_8,
        }
        return vehicles
