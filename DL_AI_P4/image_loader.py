import os
import cv2

SUPPORTED_EXTENSIONS = {"jpg", "jpeg", "png", "bmp"}


def validate_image_path(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    extension = os.path.splitext(image_path)[1].lower().strip('.')
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported image format: {extension}. Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")


def load_image(image_path):
    validate_image_path(image_path)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read image file: {image_path}")
    return image


def resize_image(image, max_width=1200, max_height=1200):
    height, width = image.shape[:2]
    if width <= max_width and height <= max_height:
        return image

    scale = min(max_width / width, max_height / height)
    new_size = (int(width * scale), int(height * scale))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
