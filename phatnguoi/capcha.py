from io import BytesIO
from typing import Union
from PIL import Image
import pytesseract
import numpy as np


def decode_capcha(img: Union[str, BytesIO]):
    capcha_array = np.array(Image.open(img))
    capcha_text = pytesseract.image_to_string(capcha_array)
    return capcha_text
