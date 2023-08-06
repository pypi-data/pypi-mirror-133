from wand.image import Image as WImage
from PIL import Image as PImage
from io import StringIO, BytesIO
import requests

def pngify(image):
    """Converts image files to png format - intended to deal with flag svgs from wikipedia
    
    :param image: A bytes-like object containing the image. It could be loaded from file using open
        with 'b' in the mode string (e.g open('path.svg', 'rb')) or created by calling BytesIO on 
        some object in memory (e.g BytesIO(request.content) where request is a Request object 
        resulting from requesting to the image's url)
    :type image: Bytes-like object
    
    :returns: The input image as a Pillow image in png format
    :rtype: PIL.Image
    """
    wand_img = WImage(file=image).convert('png')
    pil_image = PImage.open(BytesIO(wand_img.make_blob('png'))).convert(mode='RGB')
    return pil_image