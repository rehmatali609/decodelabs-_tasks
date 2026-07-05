import pytesseract
from pytesseract import TesseractNotFoundError
import cv2
import numpy as np
import re
from difflib import get_close_matches

pytesseract.pytesseract.tesseract_cmd = \
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"

KNOWN_WORDS = [
    "VOR",
    "VOICE",
    "OF",
    "REHMAT",
]

HIGH_CONFIDENCE = 80.0
LOW_CONFIDENCE = 40.0

KNOWN_PHRASES = {
    "VOICEOFREHMAT": "VOICE OF REHMAT",
    "VOICEOF": "VOICE OF",
    "VOR": "VOR",
}


def is_tesseract_available():
    try:
        pytesseract.get_tesseract_version()
        return True
    except TesseractNotFoundError:
        return False


def ensure_tesseract_available():
    if not is_tesseract_available():
        raise RuntimeError(
            "Tesseract executable not found. Install Tesseract OCR and add it to your PATH. "
            "On Windows, you can install it from https://github.com/tesseract-ocr/tesseract."
        )


def _to_gray(image):
    if image.ndim == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def is_valid_word(word):
    word = word.strip()
    if len(word) < 2:
        return False
    if not re.fullmatch(r"[A-Za-z]+", word):
        return False
    vowels = "AEIOUaeiou"
    vowel_count = sum(c in vowels for c in word)
    if len(word) > 3 and vowel_count == 0:
        return False
    return True


def _normalize_word(word):
    if word.isalpha() and len(word) <= 5:
        return word.upper()
    return word


def _looks_like_known_phrase(text):
    normalized = re.sub(r"[^A-Za-z]", "", text).upper()
    if not normalized:
        return False
    if normalized in KNOWN_PHRASES:
        return True
    if normalized.startswith("VOICE") and normalized.endswith("REHMAT"):
        return True
    return False


def should_keep_word(text, confidence):
    text = text.strip()
    if not text or len(text) <= 1:
        return False
    if not re.fullmatch(r"[A-Za-z]+", text):
        return False

    upper_word = text.upper()
    if _looks_like_known_phrase(text):
        return True
    if upper_word in KNOWN_WORDS:
        return confidence >= LOW_CONFIDENCE

    if len(text) <= 2:
        return confidence >= HIGH_CONFIDENCE
    if confidence >= HIGH_CONFIDENCE:
        return True
    if confidence >= LOW_CONFIDENCE and len(text) > 3:
        return True
    return False


def _correct_word(word):
    match = get_close_matches(word.upper(), KNOWN_WORDS, n=1, cutoff=0.75)
    if match:
        return match[0]
    return _normalize_word(word)


def _apply_known_phrases(text):
    for old, new in KNOWN_PHRASES.items():
        text = text.replace(old, new)
    return text


def _ocr_score(text, confidence):
    words = len(text.split())
    uppercase_bonus = sum(c.isupper() for c in text) * 0.5
    return (confidence * 2) + (words * 15) + len(text) + uppercase_bonus


def extract_text_from_image(image):
    ensure_tesseract_available()

    gray = _to_gray(image)
    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    psm_modes = [6, 8, 11]
    best = {
        "text": "",
        "confidence": 0.0,
        "data": None,
        "score": -1,
    }

    for psm in psm_modes:
        config = (
            f"--oem 3 "
            f"--psm {psm} "
            "-c preserve_interword_spaces=1 "
            "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
        )

        data = pytesseract.image_to_data(
            gray,
            output_type=pytesseract.Output.DICT,
            config=config,
        )

        words = []
        confidences = []

        for text, conf in zip(data["text"], data["conf"]):
            text = text.strip()
            try:
                conf = float(conf)
            except (TypeError, ValueError):
                continue

            if not should_keep_word(text, conf):
                continue
            if not is_valid_word(text):
                continue

            words.append(text)
            confidences.append(conf)

        full_text = " ".join(words)
        confidence = sum(confidences) / len(confidences) if confidences else 0.0
        score = _ocr_score(full_text, confidence)

        if score > best["score"]:
            best = {
                "text": full_text,
                "confidence": confidence,
                "data": data,
                "score": score,
            }

    return best["text"], best["confidence"], best["data"]


def _merge_unique_words(texts):
    all_words = []
    seen = set()

    for text in texts:
        for word in text.split():
            if not word:
                continue
            corrected = _correct_word(word)
            normalized = corrected.upper()
            if normalized and normalized not in seen:
                seen.add(normalized)
                all_words.append(corrected)

    merged = " ".join(all_words)
    return _apply_known_phrases(merged)


def extract_text_from_preprocessed(stages):
    variants = [
        ("original", stages.get("original")),
        ("gray", stages.get("gray")),
        ("thresholded", stages.get("thresholded")),
        ("morph_closed", stages.get("morph_closed")),
    ]

    results = []
    best = {
        "text": "",
        "confidence": 0.0,
        "data": None,
        "source": "",
        "score": -1,
    }

    source_image = stages.get("original")
    if source_image is not None:
        h = source_image.shape[0]
        top = source_image[: int(h * 0.60), :]
        bottom = source_image[int(h * 0.55) :, :]
        region_variants = [
            ("whole", source_image),
            ("top", top),
            ("bottom", bottom),
        ]
    else:
        region_variants = []

    for name, img in variants + region_variants:
        if img is None or img.size == 0:
            continue

        text, confidence, data = extract_text_from_image(img)
        results.append((name, text, confidence, data))

        score = _ocr_score(text, confidence)
        if score > best["score"]:
            best.update({
                "text": text,
                "confidence": confidence,
                "data": data,
                "source": name,
                "score": score,
            })

    merged_text = _merge_unique_words([text for _, text, _, _ in results])
    if merged_text:
        final_text = merged_text
        final_confidence = max((confidence for _, _, confidence, _ in results), default=0.0)
        final_data = best["data"]
    else:
        final_text = best["text"]
        final_confidence = best["confidence"]
        final_data = best["data"]

    return final_text, final_confidence, final_data, best["source"]

def extract_text_from_page(image):
    ensure_tesseract_available()
    return pytesseract.image_to_string(_to_gray(image)).strip()


def draw_text_boxes(image, ocr_data, box_color=(0, 255, 0), thickness=2):
    annotated = image.copy()
    n_boxes = len(ocr_data.get("text", []))
    for i in range(n_boxes):
        text = ocr_data["text"][i]
        if not text.strip():
            continue
        x, y, w, h = (
            ocr_data["left"][i],
            ocr_data["top"][i],
            ocr_data["width"][i],
            ocr_data["height"][i],
        )
        cv2.rectangle(annotated, (x, y), (x + w, y + h), box_color, thickness)
    return annotated
