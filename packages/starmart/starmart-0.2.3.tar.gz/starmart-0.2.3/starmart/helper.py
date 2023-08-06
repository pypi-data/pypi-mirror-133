import re
import cv2
import base64
import numpy as np


class Typed(object):
    def type(self):
        raise NotImplementedError(f'type() not implemented on {self.__name__}')


class Validatable(object):
    def validate_data(self, data) -> bool:
        raise NotImplementedError(f'validate_data not implemented on {self.__name__}')


class ImageUtils(object):
    @classmethod
    def from_cv2_image(cls, cv2_image):
        _, buffer = cv2.imencode('.jpg', cv2_image)
        return cls(base64.b64encode(buffer).decode('utf-8'))

    @classmethod
    def from_pillow_image(cls, pillow_image):
        open_cv_image = np.array(pillow_image)
        cv2_image = open_cv_image[:, :, ::-1].copy()
        return cls.from_cv2_image(cv2_image)

    def validate_base64_image(self, data: str):
        m = re.search('^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$', data)
        return m is not None
