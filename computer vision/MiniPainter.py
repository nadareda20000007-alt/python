import cv2
import numpy as np

W, H = 900, 600
CANVAS_BG = (255, 255, 255)

# 5 predefined BGR colors
COLORS = {
    ord('1'): ("Red",    (0, 0, 255)),
    ord('2'): ("Green",  (0, 200, 0)),
    ord('3'): ("Blue",   (255, 0, 0)),
    ord('4'): ("Yellow", (0, 255, 255)),
    ord('5'): ("Purple", (200, 0, 200)),
}

MODES = {ord('c'): "circle", ord('r'): "rectangle", ord('p'): "polygon"}

RADIUS = 45          # circle radius / polygon circumradius
RECT_W, RECT_H = 100, 70
POLY_SIDES = 5

state = {
    "mode": "circle",
    "color": (0, 0, 255),
    "color_name": "Red",
}

canvas = np.full((H, W, 3), CANVAS_BG, dtype=np.uint8)
saved_count = 0




#This function generates the 2D vertex coordinates for a regular polygon

#cx, cy: Center coordinates of the polygon in pixels.rotation: Angle offset in radians (default: $-90^\circ$).
#r: Radius (distance from the center to each corner).
#sides: Number of vertices/edges (e.g., 3 for triangle, 4 for square, 5 for pentagon, 6 for hexagon).
#rotation: Angle offset in radians (default: $-90^\circ$).

def regular_polygon(cx, cy, r, sides, rotation=-np.pi / 2):
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False) + rotation
    pts = np.stack([cx + r * np.cos(angles), cy + r * np.sin(angles)], axis=1)
    return pts.astype(np.int32).reshape(-1, 1, 2)


#This function draws a specific geometric shape onto an OpenCV image (canvas) at position (x, y) based on the active settings stored in a global state dictionary.
def draw_shape(x, y):
    mode, color = state["mode"], state["color"]
    if mode == "circle":
        cv2.circle(canvas, (x, y), RADIUS, color, -1, cv2.LINE_AA)
    elif mode == "rectangle":
        p1 = (x - RECT_W // 2, y - RECT_H // 2)
        p2 = (x + RECT_W // 2, y + RECT_H // 2)
        cv2.rectangle(canvas, p1, p2, color, -1, cv2.LINE_AA)
    elif mode == "polygon":
        cv2.fillPoly(canvas, [regular_polygon(x, y, RADIUS, POLY_SIDES)],
                     color, cv2.LINE_AA)


#it detects when you click the left mouse button and calls your draw_shape(x, y) function
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        draw_shape(x, y)

#instruction bar / Heads-Up Display (HUD) overlay
def render_hud(img):
    view = img.copy()
    text = f"Mode: {state['mode'].upper()}   Color: {state['color_name']}"
    cv2.rectangle(view, (0, 0), (430, 60), (30, 30, 30), -1)
    cv2.putText(view, text, (12, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(view, "c/r/p shape | 1-5 color | w save | q quit",
                (12, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                (180, 180, 180), 1, cv2.LINE_AA)
    # color swatch
    cv2.rectangle(view, (390, 12), (420, 42), state["color"], -1)
    cv2.rectangle(view, (390, 12), (420, 42), (255, 255, 255), 1)
    return view


cv2.namedWindow("Mini Painter")
cv2.setMouseCallback("Mini Painter", on_mouse)

while True:
    cv2.imshow("Mini Painter", render_hud(canvas))
    key = cv2.waitKey(20) & 0xFF

    if key == 255:
        continue
    if key == ord('q'):
        break
    if key in MODES:
        state["mode"] = MODES[key]
    elif key in COLORS:
        state["color_name"], state["color"] = COLORS[key]
    elif key == ord('w'):
        saved_count += 1
        filename = f"painting_{saved_count:02d}.png"
        cv2.imwrite(filename, canvas)
        print(f"Saved {filename}")

cv2.destroyAllWindows()