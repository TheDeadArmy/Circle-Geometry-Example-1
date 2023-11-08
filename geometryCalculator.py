import math

class Circle:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
        # stores data that stays constant, but is calculated on run time
        self.cache = {}

class Vertex:
    def __init__(self, position):
        self.position = position
        # stores data that stays constant, but is calculated on run time
        self.cache = {}
    
    def CalcTangentToCircle(self, circle):
        dx = self.position[0] - circle.position[0] # difference in x positions
        dy = self.position[1] - circle.position[1] # difference in y positions
        magnitude = math.sqrt(dx ** 2 + dy ** 2) # pyth

        if magnitude < circle.radius:
            return 0

        # calculate the angle to the horizontal
        gradient = dy / (0.001 if dx == 0 else dx)
        angleToHorizontal = math.atan(gradient)

        if dx >= 0:  # cast diagram bug fix
            angleToHorizontal += math.pi

        # find the direction from the circle center to the tangent
        theta = math.acos(circle.radius / magnitude) # rads
        tangentMagnitude = math.sin(theta) * magnitude
        theta2 = math.pi / 2 - theta # find the second angle in the rh tri.

        # find the vertex of the tangent
        tangentP1X = self.position[0] + math.cos(angleToHorizontal + theta2) * tangentMagnitude
        tangentP1Y = self.position[1] + math.sin(angleToHorizontal + theta2) * tangentMagnitude

        tangentP2X = self.position[0] + math.cos(angleToHorizontal - theta2) * tangentMagnitude
        tangentP2Y = self.position[1] + math.sin(angleToHorizontal - theta2) * tangentMagnitude

        return [(tangentP1X, tangentP1Y), (tangentP2X, tangentP2Y)]

class LineVec:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction # normaised direction
    
    def LineIntersect(self, line):
        ptA = self.position
        ptB = (self.position[0] + 1000 * self.direction[0], self.position[1] + 1000 * self.direction[1])
        ptC = line.position
        ptD = (line.position[0] + 1000 * line.direction[0], line.position[1] + 1000 * line.direction[1])
        return self.lineLineIntersection(ptA, ptB, ptC, ptD)

    def lineLineIntersection(self, A, B, C, D): # from geeksforgeeks
        # Line AB represented as a1x + b1y = c1
        a1 = B[1] - A[1]
        b1 = A[0] - B[0]
        c1 = a1*(A[0]) + b1*(A[1])
    
        # Line CD represented as a2x + b2y = c2
        a2 = D[1] - C[1]
        b2 = C[0] - D[0]
        c2 = a2*(C[0]) + b2*(C[1])
    
        determinant = a1*b2 - a2*b1
    
        if (determinant == 0):
            # The lines are parallel. This is simplified
            # by returning a pair of FLT_MAX
            return (10**9, 10**9)
        else:
            x = (b2*c1 - b1*c2)/determinant
            y = (a1*c2 - a2*c1)/determinant
            return (x, y)
    
    # def LineIntersect(self, line): # approximation -- my method
    #     if self.direction[0] == line.direction[0] and self.direction[1] == line.direction[1]:
    #         return (0, 0)
        
    #     dx = self.position[0] - line.position[0]
    #     dy = self.position[1] - line.position[1]

    #     dot = dx * self.direction[0] + dy * self.direction[1]

    #     # vertex normal intersect
    #     vnix = self.position[0] - self.direction[0] * dot
    #     vniy = self.position[1] - self.direction[1] * dot

    #     # difference of ...
    #     dvnix = line.position[0] - vnix
    #     dvniy = line.position[1] - vniy

    #     dot = dvnix * line.direction[0] + dvniy * line.direction[1]

    #     # vertex normal intersect perpendicular intersect on 'line'
    #     pix = line.position[0] - line.direction[0] * dot
    #     piy = line.position[1] - line.direction[1] * dot

    #     piMag = math.sqrt((line.position[0] - pix) ** 2 + (line.position[1] - piy) ** 2)
    #     vniMag = math.sqrt((line.position[0] - vnix)** 2 + (line.position[1] - vniy)** 2)

    #     theta = math.acos(piMag / vniMag)

    #     distToIntersection = vniMag ** 2 / piMag
    #     intersectPtX = line.position[0] + distToIntersection * line.direction[0]
    #     intersectPtY = line.position[1] + distToIntersection * line.direction[1]

        return (intersectPtX, intersectPtY)