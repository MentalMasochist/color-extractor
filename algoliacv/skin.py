import cv2
import numpy as np

from .task import Task


class Skin(Task):
    def __init__(self, settings={}):
        """
        Skin is detected using color ranges.

        The possible settings are:
            - skin_type: The type of skin most expected in the given images.
              the value can be 'general', '1-2', '3-4' or '5-6'.
              The thresholds refer to the Fitzpatrick scale.
              (default: 'general')
        """
        super(Skin, self).__init__(settings)
        self._k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        t = self.settings['skin_type']
        if t == 'general':
            self._lo = np.array([0, 48, 80], np.uint8)
            self._up = np.array([20, 255, 255], np.uint8)
        else:
            raise NotImplementedError('Only general type is implemented')

    def get(self, img):
        t = self.settings['skin_type']
        if t == 'general':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        else:
            raise NotImplementedError('Only general type is implemented')

        return self._range_mask(img)

    def _range_mask(self, img):
        mask = cv2.inRange(img, self._lo, self._up)

        # Smooth the mask.
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self._k)
        return cv2.GaussianBlur(mask, (3, 3), 0) != 0

    @staticmethod
    def _default_settings():
        return {
            'skin_type': 'general',
        }
