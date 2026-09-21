import sys
import cv2
import numpy as np

IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else "objects.jpg"
MIN_AREA = 500          # ignore specks / noise

img = cv2.imread(IMAGE_PATH)
if img is None:
    raise SystemExit(f"Could not load '{IMAGE_PATH}'")

# keep it a sane size on screen
if img.shape[1] > 1000:
    scale = 1000 / img.shape[1]
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

blurred = cv2.GaussianBlur(img, (5, 5), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

state = {"target": None, "count": 0, "label": "none"}


def make_mask(h, s, v, h_tol, s_tol, v_tol):
    """Build a mask, splitting the range in two if the hue wraps past 0/180."""
    lo_s, hi_s = max(0, s - s_tol), min(255, s + s_tol)
    lo_v, hi_v = max(0, v - v_tol), min(255, v + v_tol)
    lo_h, hi_h = h - h_tol, h + h_tol

    if lo_h < 0:                       # wraps below 0
        m1 = cv2.inRange(hsv, np.array([0, lo_s, lo_v]), np.array([hi_h, hi_s, hi_v]))
        m2 = cv2.inRange(hsv, np.array([180 + lo_h, lo_s, lo_v]), np.array([179, hi_s, hi_v]))
        mask = cv2.bitwise_or(m1, m2)
    elif hi_h > 179:                   # wraps above 179
        m1 = cv2.inRange(hsv, np.array([lo_h, lo_s, lo_v]), np.array([179, hi_s, hi_v]))
        m2 = cv2.inRange(hsv, np.array([0, lo_s, lo_v]), np.array([hi_h - 180, hi_s, hi_v]))
        mask = cv2.bitwise_or(m1, m2)
    else:
        mask = cv2.inRange(hsv, np.array([lo_h, lo_s, lo_v]), np.array([hi_h, hi_s, hi_v]))

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    return mask


def get_tol():
    return (cv2.getTrackbarPos("H tol", "Result"),
            cv2.getTrackbarPos("S tol", "Result"),
            cv2.getTrackbarPos("V tol", "Result"))


def analyze():
    """Threshold on the current target, box every blob, update the count."""
    if state["target"] is None:
        return img.copy(), np.zeros(img.shape[:2], np.uint8)

    h, s, v = state["target"]
    mask = make_mask(h, s, v, *get_tol())

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = [c for c in contours if cv2.contourArea(c) >= MIN_AREA]

    out = img.copy()
    for i, c in enumerate(objects, 1):
        x, y, w, h_box = cv2.boundingRect(c)
        cv2.rectangle(out, (x, y), (x + w, y + h_box), (0, 255, 0), 2)
        cv2.putText(out, str(i), (x, y - 6), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 255, 0), 2, cv2.LINE_AA)

    state["count"] = len(objects)

    banner = f"{state['label']} -> {state['count']} object(s)"
    cv2.rectangle(out, (0, 0), (out.shape[1], 34), (30, 30, 30), -1)
    cv2.putText(out, banner, (10, 23), cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 1, cv2.LINE_AA)
    return out, mask


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        h, s, v = hsv[y, x]
        state["target"] = (int(h), int(s), int(v))
        state["label"] = f"HSV({h},{s},{v})"
        out, mask = analyze()
        print(f"Picked {state['label']} at ({x},{y})  ->  {state['count']} object(s)")
        cv2.imshow("Result", out)
        cv2.imshow("Mask", mask)


def manual_entry():
    """Type HSV bounds instead of clicking."""
    try:
        raw = input("Enter target H S V (0-179 0-255 0-255): ").split()
        h, s, v = (int(n) for n in raw)
    except ValueError:
        print("Invalid input — expected three integers.")
        return
    state["target"] = (h, s, v)
    state["label"] = f"HSV({h},{s},{v})"
    out, mask = analyze()
    print(f"{state['label']}  ->  {state['count']} object(s)")
    cv2.imshow("Result", out)
    cv2.imshow("Mask", mask)


cv2.namedWindow("Result")
cv2.namedWindow("Mask")
cv2.createTrackbar("H tol", "Result", 10, 90, lambda v: None)
cv2.createTrackbar("S tol", "Result", 80, 255, lambda v: None)
cv2.createTrackbar("V tol", "Result", 90, 255, lambda v: None)
cv2.setMouseCallback("Result", on_mouse)

print("Click any object to count its color | h = enter HSV manually | "
      "r = reset | q = quit")
cv2.imshow("Result", img)

while True:
    key = cv2.waitKey(60) & 0xFF

    # live re-threshold as the tolerance sliders move
    if state["target"] is not None:
        out, mask = analyze()
        cv2.imshow("Result", out)
        cv2.imshow("Mask", mask)

    if key == ord('q'):
        break
    elif key == ord('h'):
        manual_entry()
    elif key == ord('r'):
        state["target"], state["count"], state["label"] = None, 0, "none"
        cv2.imshow("Result", img)
        cv2.imshow("Mask", np.zeros(img.shape[:2], np.uint8))
        print("Reset — pick a new color.")

cv2.destroyAllWindows()