from numpy import testing
from numpy.lib.type_check import imag
import pygame
import sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2

BOUNDRYINC = 5
WINDOWSIZEX = 640
WINDOWSIZEY = 480

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
IMAGESAVE = False


MODEL = load_model(
    "C://Users//Dell//OneDrive//Desktop//Mini Project//best_model.h5")
LABELS = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four",
          5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
FONT = pygame.font.Font(
    "C://Users//Dell//OneDrive//Desktop//Mini Project//FreeSansBold.ttf", 18)
WHITE_INT = DISPLAYSURF.map_rgb(WHITE)
pygame.display.set_caption("Digit Board")
number_xcord = []
number_ycord = []
isWriting = False
img_cnt = 1
PREDICT = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and isWriting:
            x_cord, y_cord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (x_cord, y_cord), 4, 0)
            number_xcord.append(x_cord)
            number_ycord.append(y_cord)
        if event.type == MOUSEBUTTONDOWN:
            isWriting = True
        if event.type == MOUSEBUTTONUP:
            isWriting = False
            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)
            rect_min_x, rect_max_x = max(
                number_xcord[0]-BOUNDRYINC, 0), min(WINDOWSIZEX, number_xcord[-1]+BOUNDRYINC)

            rect_min_Y, rect_max_Y = max(
                number_ycord[0]-BOUNDRYINC, 0), min(number_ycord[-1]+BOUNDRYINC, WINDOWSIZEY)

            number_xcord = []
            number_ycord = []

            img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[
                rect_min_x:rect_max_x, rect_min_Y: rect_max_Y].T.astype(np.float32)

            if IMAGESAVE:
                cv2.imwrite("image.png")
                img_cnt += 1

            if PREDICT:
                image = cv2.resize(img_arr, (28, 28))
                image = np.pad(image, (10, 10), 'constant', constant_values=0)
                image = cv2.resize(image, (28, 28))/255
                label = str(
                    LABELS[np.argmax(MODEL.predict(image.reshape(1, 28, 28, 1)))])
                testSurface = FONT.render(label, True, RED, WHITE)
                testRecObj = testSurface.get_rect()
                testRecObj.left, testRecObj.bottom = rect_min_x, rect_min_Y
                DISPLAYSURF.blit(testSurface, testRecObj)

        if event.type == KEYDOWN:
            if event.unicode == "n":
                DISPLAYSURF.fill(BLACK)
    pygame.display.update()
