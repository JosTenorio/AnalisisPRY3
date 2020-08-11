import pygame as py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg

# matplotlib setup
fig = plt.figure()
ax = fig.add_subplot(111)
canvas = agg.FigureCanvasAgg(fig)

# pygame setup
WIDTH = 1300
HEIGHT = 800
SQUARE = 25
py.init()
WINDOW = py.display.set_mode([WIDTH, HEIGHT])
py.display.set_caption("Genetic Path Solver")
CLOCK = py.time.Clock()

# colors
COLOR_CREAM = (255, 230, 208)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (154,205,50)
COLOR_YELLOW = (255,215,0)
COLOR_RED = (220,20,60)
COLOR_BLUE = (30,144,255)
COLOR_PURPLE = (147,112,219)
COLOR_BROWN = (205,133,63)
COLOR_WHITE = (255, 255, 255)

# fonts
FONT = "arial"

class Button:

    def __init__(self, color, x, y, width, height, textSize, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textSize = textSize

    def draw(self, outline = None):
        if outline:
            py.draw.rect(WINDOW, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        py.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = py.font.SysFont(FONT, self.textSize)
            text = font.render(self.text, 1, (0, 0, 0))
            WINDOW.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

def drawMatrix(matrix, posX, posY, square):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row, col] == 0:
                py.draw.rect(WINDOW, COLOR_BLACK, (col * square + posX, row * square + posY, square, square))
            if matrix[row, col] == 1:
                py.draw.rect(WINDOW, COLOR_GREEN, (col * square + posX, row * square + posY, square, square))
            if matrix[row, col] == 2:
                py.draw.rect(WINDOW, COLOR_YELLOW, (col * square + posX, row * square + posY, square, square))
            if matrix[row, col] == 3:
                py.draw.rect(WINDOW, COLOR_RED, (col * square + posX, row * square + posY, square, square))
            if matrix[row, col] == 4:
                py.draw.rect(WINDOW, COLOR_BLUE, (col * square + posX, row * square + posY, square, square))
            if matrix[row, col] == 5:
                py.draw.rect(WINDOW, COLOR_PURPLE, (col * square + posX, row * square + posY, square, square))

def drawText(text, textSize, posX, posY):
    font = py.font.SysFont(FONT, textSize)
    text = font.render(text, 1, (0, 0, 0))
    WINDOW.blit(text, (posX, posY))

def plot(xAxis, yAxis, color):
    ax.plot(xAxis, yAxis, color=color)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    return py.image.fromstring(raw_data, size, "RGB")
