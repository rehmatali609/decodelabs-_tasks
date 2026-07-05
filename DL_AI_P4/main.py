import argparse
import time
import os
import cv2

from image_loader import load_image, resize_image
from preprocessing import preprocess_image, detect_edges
from ocr_engine import extract_text_from_image, extract_text_from_preprocessed, draw_text_boxes
from object_detector import detect_objects_by_contours, draw_object_boxes
from utils import save_json, save_text, format_duration, timestamped_filename, ensure_folder


def count_text_blocks(ocr_data):
    return sum(1 for text in ocr_data.get("text", []) if isinstance(text, str) and text.strip())


def generate_report(image_path, detected_text, confidence, objects, processing_time, image_size, text_blocks, status, output_folder):
    return {
        "image_path": image_path,
        "image_size": image_size,
        "text_detected": detected_text,
        "text_blocks": text_blocks,
        "ocr_confidence": round(confidence, 2),
        "objects_detected": len(objects),
        "processing_time": format_duration(processing_time),
        "status": status,
        "output_folder": output_folder,
        "object_details": objects,
    }


def save_results(base_path, original_image, processed_image, text_overlay_image, detected_text, report):
    ensure_folder(base_path)
    original_path = os.path.join(base_path, timestamped_filename("original", "png"))
    processed_path = os.path.join(base_path, timestamped_filename("processed", "png"))
    overlay_path = os.path.join(base_path, timestamped_filename("annotated", "png"))
    text_path = os.path.join(base_path, timestamped_filename("recognized_text", "txt"))
    report_path = os.path.join(base_path, timestamped_filename("report", "json"))

    cv2.imwrite(original_path, original_image)
    cv2.imwrite(processed_path, processed_image)
    cv2.imwrite(overlay_path, text_overlay_image)
    save_text(text_path, detected_text)
    save_json(report_path, report)

    return {
        "original": original_path,
        "processed": processed_path,
        "annotated": overlay_path,
        "text": text_path,
        "report": report_path,
    }


def run_pipeline(image_path, output_folder):
    start_time = time.time()
    print("=========================================")
    print("AI Vision Recognition System")
    print("=========================================\n")

    print("Loading image...")
    image = load_image(image_path)
    image = resize_image(image)
    print("✓ Image Loaded")

    print("Preprocessing...")
    stages = preprocess_image(image)
    print("✓ Grayscale Applied")
    print("✓ Noise Removed")
    print("✓ CLAHE Applied")
    print("✓ Blur Applied")
    print("✓ Adaptive Threshold Applied")
    print("✓ Morphology Close Applied")

    print("Running OCR...")
    try:
        detected_text, confidence, ocr_data, source = extract_text_from_preprocessed(stages)
        if detected_text:
            print(f"✓ Text Detected from {source}")
        else:
            print("✓ OCR Completed (no text found)")
    except RuntimeError as err:
        detected_text = ""
        confidence = 0.0
        ocr_data = {"text": [], "left": [], "top": [], "width": [], "height": []}
        print(f"✗ OCR skipped: {err}")

    print("Running Object Detection...")
    objects = detect_objects_by_contours(image)
    print(f"✓ {len(objects)} objects found")

    text_overlay_image = draw_text_boxes(image, ocr_data)
    object_overlay_image = draw_object_boxes(text_overlay_image, objects)

    processing_time = time.time() - start_time
    image_size = f"{image.shape[1]} × {image.shape[0]}"
    text_blocks = count_text_blocks(ocr_data)
    report = generate_report(
        image_path,
        detected_text,
        confidence,
        objects,
        processing_time,
        image_size,
        text_blocks,
        "SUCCESS",
        output_folder,
    )

    output_paths = save_results(output_folder, image, stages["thresholded"], object_overlay_image, detected_text, report)

    print("\n=========================================")
    print("AI Vision Recognition Report")
    print("=========================================")
    print(f"Image Size: {image_size}")
    print(f"Objects Detected: {len(objects)}")
    print(f"Text Blocks: {text_blocks}")
    print(f"OCR Confidence: {confidence:.2f} %")
    print(f"Processing Time: {format_duration(processing_time)}")
    print(f"Output Folder: {output_folder}")
    print("Status: SUCCESS")
    print("\nOCR RESULTS")
    print(detected_text or "No text recognized.")
    print("\nDetected Objects")
    print(", ".join([obj["shape"] for obj in objects]) if objects else "No objects detected.")
    print("\nResults saved successfully.")
    print("Saved files:")
    print("-", output_paths["original"])
    print("-", output_paths["processed"])
    print("-", output_paths["annotated"])
    print("-", output_paths["text"])
    print("-", output_paths["report"])

    return output_paths


def parse_args():
    parser = argparse.ArgumentParser(description="AI Vision Engine: OCR and Object Detection Pipeline")
    parser.add_argument("image_path", help="Path to an input image file")
    parser.add_argument("--output", default="output", help="Folder where results will be saved")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        run_pipeline(args.image_path, args.output)
    except Exception as err:
        print(f"\nError: {err}")
        print("Please install or configure any missing dependencies and try again.")
