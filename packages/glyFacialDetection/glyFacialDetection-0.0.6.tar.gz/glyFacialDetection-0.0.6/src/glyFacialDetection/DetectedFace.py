import DetectedArea

class DetectedFace(DetectedArea):
    def __init__(self, upperLeftPoint = (0,0), dimensions = (0,0), angle = None):
        """
        Create an detectedFace object that is a detectedArea object but with angle property.
            :param upperLeftPoint (x,y): the 2-tuple coordinates of the upper left point of the rectangle encapsulates detected objects.
            :param dimension (w,h): the dimension of the box encapsulates the detected object.
            :param angle: the angle of the image when the detected object was found and returned by openCV.
        """
        super().__init__(upperLeftPoint=upperLeftPoint, dimensions=dimensions)
        # face's angle is the counter clockwise angle of the right eye to the left eye
        self.counterClockwiseAngle = angle
        self.leftEye = None
        self.rightEye = None
        
    
    def copy(self):
        """
        Return a deep copy of the detectedArea caller
            :return a deep copy of itself
        """
        copyArea = DetectedFace()
        copyArea.dimensions = (self.dimensions[0], self.dimensions[1])
        copyArea.upperLeft = self.upperLeft.copy()
        copyArea.upperRight = self.upperRight.copy()
        copyArea.lowerLeft = self.lowerLeft.copy()
        copyArea.lowerRight = self.lowerRight.copy()
        copyArea.center = self.center.copy()
        copyArea.counterClockwiseAngle = self.counterClockwiseAngle
        copyArea.leftEye = self.leftEye
        copyArea.rightEye = self.rightEye
        return copyArea