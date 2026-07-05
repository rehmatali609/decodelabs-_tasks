import cv2


def detect_objects_by_contours(image, min_area=1000):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for contour in contours:
        if cv2.contourArea(contour) < max(min_area, 300):
            continue

        x, y, w, h = cv2.boundingRect(contour)
        shape = classify_shape(contour)
        objects.append({
            "shape": shape,
            "box": (x, y, w, h),
            "area": int(cv2.contourArea(contour)),
        })
    return objects


def classify_shape(contour):
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    vertex_count = len(approx)

    if vertex_count == 3:
        return "Triangle"
    elif vertex_count == 4:
        return "Rectangle"
    elif vertex_count > 8:
        return "Circle"
    elif vertex_count > 4:
        return "Polygon"
    return "Unknown"


def draw_object_boxes(image, objects, box_color=(255, 0, 0), thickness=2):
    annotated = image.copy()
    for obj in objects:
        x, y, w, h = obj["box"]
        label = obj.get("shape", "object")
        cv2.rectangle(annotated, (x, y), (x + w, y + h), box_color, thickness)
        cv2.putText(
            annotated,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            box_color,
            1,
            cv2.LINE_AA,
        )
    return annotated
