import numpy as np
import cv2 as cv
import cv2

def display_midpoint(fitted_line, color, image_circles):
    if fitted_line is not None:
        vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
        print(x0, y0)
        cv.circle(image_circles, (x0, y0), 5, color, 4)
def arsenyCode(image):
    # Capture frame-by-frame
    points = []
    # if frame is read correctly ret is True
    if image is None:
        print("Can't receive frame (stream end?). Exiting ...")
        return image
    w, h = image.shape[:2]
    height, width = image.shape[:2]
    image_lines = np.zeros((height, width, 3), dtype=np.uint8)
    image_circles = np.zeros((height, width, 3), dtype=np.uint8)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blur, 50, 150)

    lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180, threshold=100, minLineLength=100, maxLineGap=50)

    def draw_extended_line(fitted_line, color):
        if fitted_line is not None:
            vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
            #print(fitted_line[0, 0], fitted_line[1, 0], fitted_line[2, 0], fitted_line[3, 0])
            if vx != 0:
                lefty = int((-x0 * vy / vx) + y0)
                righty = int(((width - x0) * vy / vx) + y0)

                cv.line(image, (width - 1, righty), (0, lefty), color, 2)
                return (int(x0), int(y0))
                #cv.circle(image, (x0, y0), 5, (0, 0, 255), 4)
            # midpoint_x = (vx + x0) // 2
            # midpoint_y = (vy + y0) // 2
            # cv2.circle(image_lines, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            midpoint_x = (x1 + x2) // 2

            midpoint_y = (y1 + y2) // 2

            #cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 4)
            #cv2.line(image_lines, (x1, y1), (x2, y2), (255, 0, 255), 4)
            edges_blur = cv2.GaussianBlur(image_lines, (7, 7), 10)
            cv2.line(edges_blur, (x1, y1), (x2, y2), (255, 0, 0), 4)

            cv2.circle(image_lines, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
            points.append((midpoint_x, midpoint_y))
    right_points = []
    left_points = []

    for x, y in points:
        if x > w // 2:
            right_points.append((x, y))
        else:
            left_points.append((x, y))
    # numpy array
    right_points_np = np.array(right_points)
    left_points_np = np.array(left_points)
    try:
        right_line = cv.fitLine(right_points_np, cv.DIST_L1, 1, 0.01, 0.01)
        left_line = cv.fitLine(left_points_np, cv.DIST_L1, 1, 0.01, 0.01)
        #draw_extended_line(right_line, (0, 255, 255))
        #draw_extended_line(left_line, (0, 255, 0))
        centroid_r = draw_extended_line(right_line, (0, 255,  255))
        centroid_l = draw_extended_line(left_line, (0, 255, 0))
        if centroid_r is not None:
            # Draw the centroid circle for the right line on its overlay
            cv.circle(image, centroid_r, 5, (0, 0, 255), 4) # RED
        if centroid_l is not None:
            # Draw the centroid circle for the right line on its overlay
            cv.circle(image, centroid_l, 5, (0, 0, 255), 4) # RED

        cv2.line(image, centroid_r, centroid_l, (255, 100, 100), 4)

        x1, y1 = centroid_r[0], centroid_r[1]
        x2, y2= centroid_l[0], centroid_l[1]

        midpoint_x = (x1 + x2) // 2

        midpoint_y = (y1 + y2) // 2

        cv2.circle(image, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
        

        # display_midpoint(right_line, (0, 255, 0), image_circles)
        # display_midpoint(left_line, (0, 255, 0), image_circles)

    except:
        print("Can't find right line")
      
    return image
