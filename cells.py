from math import sqrt, pi

class Circle:
    def __init__(self, config):
        self.config = config

    def draw(self, image,  gridPosition, cellDimension):
        size = int(self.config['size'])
        center = float(cellDimension*size)/2
        radius = size * cellDimension * 0.5
        colorHex = int(self.config['color'], 16)
        color = [((colorHex >> 16) & 0xFF), ((colorHex >> 8) & 0xFF), (colorHex & 0xFF)]
        imageOffset = (gridPosition[0] * cellDimension, gridPosition[1] * cellDimension)
        for x in range(cellDimension*size):
            for y in range(cellDimension*size):
                x1 = x - center;
                y1 = y - center;
                isInCircle = sqrt((x1*x1) + (y1*y1)) <= radius
                imgX = int(imageOffset[0] + x1)
                imgY = int(imageOffset[1] + y1)
                if isInCircle and imgX < len(image) and imgY < len(image[0]):
                    image[imgX][imgY] = color
