import json
import sys
import hashlib
import random
from PIL import Image
import numpy as np
import cells
from math import sqrt

def getCellDimension(config):
    resolution = config['resolution']
    grid = config['grid']
    x = resolution[0]/grid[0]
    y = resolution[1]/grid[1]
    if x != y:
        raise Exception("Cells must be square!")
    return int(x)

def getGridDimensions(config):
    grid = config['grid']
    return (int(grid[0]), int(grid[1]))

def seedRng(config):
    seed = hashlib.md5(config["name"].encode('utf-8')).hexdigest()
    random.seed(seed)

def getCell(config):
    for lifeform in config:
        if lifeform['shape'] == 'circle':
            rand = random.random()
            if rand <= lifeform['density']:
                return cells.Circle(lifeform)
        else:
            raise Exception("Unrecognized Shape!")
    return None

def generateGrid(config):
    gridDimensions = getGridDimensions(config)
    seedRng(config)
    grid = []
    # probs flip dimensions
    for x in range(gridDimensions[0]):
        gridRow = []
        for y in range(gridDimensions[1]):
             gridRow.append(getCell(config['lifeforms']))
        grid.append(gridRow)
    return grid

def getInitialImage(config):
    resolution = config['resolution']
    resolutionTup = (int(resolution[0]), int(resolution[1]))
    backgroundHex = int(config['background'], 16)
    backgroundColor = [((backgroundHex >> 16) & 0xFF), ((backgroundHex >> 8) & 0xFF), (backgroundHex & 0xFF)]
    image = np.zeros((resolutionTup[0], resolutionTup[1], 3), dtype=np.uint8)
    for x in range(resolutionTup[0]):
        for y in range(resolutionTup[1]):
            image[x][y] = backgroundColor
    return image

def renderImage(config, grid):
    image = getInitialImage(config)
    cellDimension = getCellDimension(config)
    gridDimensions = getGridDimensions(config)

    for x in range(gridDimensions[0]):
        for y in range(gridDimensions[1]):
            if grid[x][y] != None:
                grid[x][y].draw(image, (x, y), cellDimension)

    img = Image.fromarray(image)
    img.save(config['target'])

def getConfig():
    myArgs = sys.argv
    if len(myArgs) < 2:
        raise Exception("Must provide a json config file!")
    config_fd = open(myArgs[1])
    config = json.load(config_fd)
    return config

config = getConfig()
grid = generateGrid(config)
renderImage(config, grid)
