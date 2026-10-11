from io import BytesIO
from PIL import Image, ImageOps, UnidentifiedImageError

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}
class InvalidImage(ValueError): pass

def read_valid_image(upload, max_bytes):
    data = upload.stream.read(max_bytes + 1)
    if not data: raise InvalidImage("The selected file is empty.")
    if len(data) > max_bytes: raise InvalidImage("Image is too large. Choose an image under 10 MB.")
    try:
        image = Image.open(BytesIO(data))
        image.verify()
        image = Image.open(BytesIO(data))
        if image.width * image.height > 25_000_000:
            raise InvalidImage("Image dimensions are too large to process safely.")
        image.load()
    except InvalidImage:
        raise
    except (UnidentifiedImageError, OSError, ValueError):
        raise InvalidImage("This file is not a valid image. Choose a JPEG, PNG, or WebP image.")
    if image.format not in ALLOWED_FORMATS:
        raise InvalidImage("Unsupported image type. Choose a JPEG, PNG, or WebP image.")
    return ImageOps.exif_transpose(image).convert("RGB")
