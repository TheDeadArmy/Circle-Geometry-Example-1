from geometryCalculator import *

class Model:
    def __init__(self, app):
        self.app = app
        self.vertexA = Vertex([0, 0])
        self.circlePQRS = Circle([-50, 0], 100)
    
    def UpdateVertexData(self):
        tangents = self.vertexA.CalcTangentToCircle(self.circlePQRS)
        if tangents == 0:
            return
        
        self.app.renderer.DrawLine(self.vertexA.position, tangents[0])
        self.app.renderer.DrawLine(self.vertexA.position, tangents[1])
        self.app.renderer.DrawLine(tangents[0], tangents[1])

        # draw line AQ
        dx = self.circlePQRS.position[0] - self.vertexA.position[0]
        dy = self.circlePQRS.position[1] - self.vertexA.position[1]
        # not efficient; should be taken from the tangent calculation
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        # normalise the vector (keep the direction, but set it's magnitude to 1)
        nx = dx / magnitude
        ny = dy / magnitude

        AQMag = magnitude + self.circlePQRS.radius
        Qpos = (self.vertexA.position[0] + AQMag * nx, self.vertexA.position[1] + AQMag * ny)

        self.app.renderer.DrawLine(self.vertexA.position, Qpos)
        # draw lines from Q to the tangents
        self.app.renderer.DrawLine(tangents[0], Qpos)
        self.app.renderer.DrawLine(tangents[1], Qpos)

        # find point S (2 times the radius behind Q in the -direction of AQ)
        Spos = (Qpos[0] - self.circlePQRS.radius * 2 * nx, Qpos[1] - self.circlePQRS.radius * 2 * ny)
        # draw lines from S to the tangents
        self.app.renderer.DrawLine(tangents[0], Spos)
        self.app.renderer.DrawLine(tangents[1], Spos)

        # calculate the intersection of the tangental lines 
        # and the lines SR and SP
        intersectionPts = []
        for i in range(2):
            tdx1 = tangents[i][0] - self.vertexA.position[0]
            tdy1 = tangents[i][1] - self.vertexA.position[1]
            tangentalMag = math.sqrt(dx ** 2 + dy ** 2)
            tnx1 = tdx1 / tangentalMag # tangental normal x 1 -- normalised
            tny1 = tdy1 / tangentalMag # tangental normal y 1

            PSx = tangents[1 - i][0] - Spos[0]
            PSy = tangents[1 - i][1] - Spos[1]
            PSMag = math.sqrt(PSx ** 2 + PSy ** 2)
            if PSMag == 0:
                PSMag = 0.0001
            PSnx = PSx / PSMag
            PSny = PSy / PSMag

            AR = LineVec(tangents[i], (-tnx1, -tny1))
            PS = LineVec(tangents[1 - i], (-PSnx, -PSny))

            intersectPt = AR.LineIntersect(PS)
            intersectionPts.append(intersectPt)

            self.app.renderer.DrawLine(Spos, intersectPt)
        
        # FINALLY CALCULATE S3 and S4!!!
        BSx = Spos[0] - intersectionPts[0][0]
        BSy = Spos[1] - intersectionPts[0][1]
        BSMag = math.sqrt(BSx ** 2 + BSy ** 2)

        Mpos = ((tangents[0][0] + tangents[1][0]) / 2, (tangents[0][1] + tangents[1][1]) / 2)
        MSx = Spos[0] - Mpos[0]
        MSy = Spos[1] - Mpos[1]
        MSMag = math.sqrt(MSx ** 2 + MSy ** 2)

        PSx = Spos[0] - tangents[0][0]
        PSy = Spos[1] - tangents[0][1]
        PSMag = math.sqrt(PSx ** 2 + PSy ** 2)
        if BSMag == 0:
            BSMag = 0.001
        if PSMag == 0:
            PSMag = 0.001
        if MSMag == 0:
            MSMag = 0.001

        S3 = math.degrees(math.acos((BSx * PSx + BSy * PSy) / (BSMag * PSMag)))
        S4 = math.degrees(math.acos((PSx * MSx + PSy * MSy) / (PSMag * MSMag)))
        print("S3: ", S3, "S4:", S4)

    def UpdateModel(self, newVertexPosition):
        self.vertexA.position = newVertexPosition
        self.UpdateVertexData()
        self.app.renderer.DrawCircle(self.circlePQRS)