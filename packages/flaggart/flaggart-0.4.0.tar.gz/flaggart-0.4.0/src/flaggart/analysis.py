from PIL import Image

# TODO Implement this in a more powerful manner using traditional clustering
def getdominantcolors(img):
    """Returns the dominant colors in a flag image. Specifically, all colors that make up more than
        1% of all pixels. Not suitable for flags with gradients yet.

    :param img: A Pillow Image object containing the flag to be analysed.
    :type img: PIL.Image

    :returns: A list of dicts. Each dict contains the colour's rgb values under the key 'rgb' as a 
        triple, and the number of times that colour appears under the key 'count' (e.g 
        [{'count': 246410, 'rgb': (255, 255, 255)}, {'count': 350526, 'rgb': (0, 94, 184)}] )
    :rtype: [{string: int, string:(int, int, int)}]
    """
    colors = img.getcolors(img.size[0]*img.size[1])
    colors = sorted(colors, key=lambda x: x[0])
    totalpix = sum([x[0] for x in colors])
    dominantcolors = [x for x in colors if x[0]/totalpix > 0.01]
    dominantcolors = [{'count': x[0], 'rgb': x[1]} for x in dominantcolors]
    return dominantcolors