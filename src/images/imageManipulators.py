import io
from PIL import Image


async def convertImage(image: bytes) -> Image:
    """

    @param image:
    @return:
    """
    cardImage = io.BytesIO(image)
    return Image.open(cardImage)


async def combineImagePairHorizontal(im1, im2) -> Image:
    """
    Combines a pair of images horizontally into a single image.
    Saves the combined image as .jpg
    :param im1: Pillow Image object
    :param im2: Pillow Image object
    """
    imagePair = Image.new('RGB', (im1.width + im2.width, im1.height))
    imagePair.paste(im1, (0, 0))
    imagePair.paste(im2, (im1.width, 0))
    return imagePair


async def combineImageListHorizontal(imList) -> Image:
    _im = imList.pop(0)
    for im in imList:
        _im = await combineImagePairHorizontal(_im, im)
    return _im
