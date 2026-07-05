import cv2
import pytesseract
from image_loader import load_image, resize_image
from preprocessing import preprocess_image
from ocr_engine import extract_text_from_image, _to_gray

img = load_image('images/logo.jpeg')
img = resize_image(img)
stages = preprocess_image(img)
regions = {
    'whole': img,
    'top': img[:int(img.shape[0]*0.65), :],
    'bottom': img[int(img.shape[0]*0.55):, :],
}
images = {
    'orig': img,
    'gray': stages['gray'],
    'threshold': stages['thresholded'],
}

for region_name, region in regions.items():
    print('REGION', region_name)
    for image_name, image in images.items():
        gray = _to_gray(image)
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        for psm in [6, 8, 11, 13]:
            config = f'--oem 3 --psm {psm} -c preserve_interword_spaces=1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, config=config)
            tokens = [(t, c) for t, c in zip(data['text'], data['conf']) if t and t.strip()]
            print(' ', image_name, 'psm', psm, '=>', tokens[:10])
    print('---')
