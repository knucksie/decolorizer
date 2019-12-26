import cv2 as cv
import numpy
from PIL import Image

GREEN = (0, 255, 0)


class Decolorizer:
    @staticmethod
    def apply_watershed(image):
        _img = image.copy()

        gray_image = cv.cvtColor(_img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray_image, 127, 255, 0)

        kernel = numpy.ones((3, 3), numpy.uint8)
        opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
        sure_bg = cv.dilate(opening, kernel, iterations=3)

        dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
        ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        sure_fg = numpy.uint8(sure_fg)
        unknown = cv.subtract(sure_bg, sure_fg)

        ret, markers = cv.connectedComponents(sure_fg)

        markers = markers + 1

        markers[unknown == 255] = 0
        markers = cv.watershed(_img, markers)
        _img[markers == -1] = [255, 0, 0]

        return _img

    @staticmethod
    def apply_contours(image):
        _img = image.copy()

        gray_image = cv.cvtColor(_img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray_image, 127, 255, 0)

        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(_img, contours, -1, GREEN, 3)
        return _img

    @staticmethod
    def to_black_white(image, contour_color):
        _img = image.copy()
        for i in range(len(_img)):
            for j in range(len(_img[0])):
                r, g, b = _img[i, j]
                if (r, g, b) == contour_color:
                    _img[i, j] = (0, 0, 0)
                else:
                    _img[i, j] = (255, 255, 255)
        return _img

    @staticmethod
    def decolorize(image_src, destination_name):
        image = cv.imread(image_src)
        image = Decolorizer.apply_watershed(image)
        image = Decolorizer.apply_contours(image)
        image = Decolorizer.to_black_white(image, GREEN)
        Image.fromarray(image).save(destination_name)
