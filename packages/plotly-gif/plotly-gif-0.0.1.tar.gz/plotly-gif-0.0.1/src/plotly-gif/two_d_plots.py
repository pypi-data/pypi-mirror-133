from io import BytesIO
from functools import wraps

from PIL import Image


def capture(func):
    @wraps(func)
    def _capture(*args, **kwargs):
        buffer = BytesIO()
        fig = func(*args, **kwargs)
        fig.write_image(buffer, format="png", **kwargs)
        buffer.seek(0)
        image = Image.open(buffer)
        return image
    return _capture

