import cv2
import numpy as np


def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(gray_image):
    return cv2.fastNlMeansDenoising(gray_image, None, 30, 7, 21)


def apply_clahe(gray_image, clip_limit=3.0, tile_grid_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(gray_image)


def blur_image(image, kernel_size=(5, 5)):
    return cv2.GaussianBlur(image, kernel_size, 0)


def adaptive_threshold(image):
    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )


def morphological_close(binary_image, kernel_size=(5, 5), iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    return cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=iterations)


def preprocess_image(image, target_width=1200, target_height=1200):
    resized = image
    height, width = image.shape[:2]
    if width > target_width or height > target_height:
        scale = min(target_width / width, target_height / height)
        new_dimensions = (int(width * scale), int(height * scale))
        resized = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_AREA)

    gray = to_grayscale(resized)
    denoised = remove_noise(gray)
    clahe = apply_clahe(denoised)
    blurred = blur_image(clahe)
    thresholded = adaptive_threshold(blurred)
    morph_closed = morphological_close(thresholded)

    return {
        "original": resized,
        "gray": gray,
        "denoised": denoised,
        "clahe": clahe,
        "blurred": blurred,
        "thresholded": thresholded,
        "morph_closed": morph_closed,
    }


def detect_edges(gray_image, low_threshold=50, high_threshold=150):
    return cv2.Canny(gray_image, low_threshold, high_threshold)
