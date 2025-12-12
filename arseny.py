import numpy as np
import cv2 as cv
import cv2


def display_midpoint(fitted_line, color, image_circles):
    if fitted_line is not None:
        vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
        print(x0, y0)
        cv.circle(image_circles, (x0, y0), 5, color, 4)


def arsenyCode(image):
    image = image
    points = []

    if image is None:
        print("Can't receive frame (stream end?). Exiting ...")
        return image

    height, width = image.shape[:2]

    image_lines = np.zeros((height, width, 3), dtype=np.uint8)
    image_circles = np.zeros((height, width, 3), dtype=np.uint8)

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 0)
    _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    closed = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
    edges = cv.Canny(closed, 20, 80)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=40,
        minLineLength=200,
        maxLineGap=120
    )

    def draw_extended_line(fitted_line, color):
        if fitted_line is not None:
            vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
            # print(fitted_line[0, 0], fitted_line[1, 0], fitted_line[2, 0], fitted_line[3, 0])
            if vx != 0:
                lefty = int((-x0 * vy / vx) + y0)
                righty = int(((width - x0) * vy / vx) + y0)

                cv.line(image, (width - 1, righty), (0, lefty), color, 2)
                return (int(x0), int(y0))
        return None

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            midpoint_x = (x1 + x2) // 2
            midpoint_y = (y1 + y2) // 2

            edges_blur = cv2.GaussianBlur(image_lines, (7, 7), 10)
            cv2.line(edges_blur, (x1, y1), (x2, y2), (255, 0, 0), 4)
            cv2.circle(image_lines, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
            points.append((midpoint_x, midpoint_y))

    points_np = np.float32(points)

    if len(points_np) >= 2:
        try:
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            K = 2
            ret, labels, centers = cv2.kmeans(points_np, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

            group1_points = points_np[labels.ravel() == 0]
            group2_points = points_np[labels.ravel() == 1]

            centroids = []

            if len(group1_points) > 1:
                line1 = cv2.fitLine(group1_points, cv2.DIST_L1, 1, 0.01, 0.01)
                centroid1 = draw_extended_line(line1, (255, 255, 0))  # Cyan
                if centroid1 is not None:
                    centroids.append(centroid1)
                    cv2.circle(image, centroid1, 7, (255, 0, 0), 4)  # Blue

            if len(group2_points) > 1:
                line2 = cv2.fitLine(group2_points, cv2.DIST_L1, 1, 0.01, 0.01)
                centroid2 = draw_extended_line(line2, (0, 255, 255))  # Yellow
                if centroid2 is not None:
                    centroids.append(centroid2)
                    cv2.circle(image, centroid2, 7, (255, 0, 255), 4)

            if len(centroids) == 2:
                (x1, y1), (x2, y2) = centroids

                mx = (x1 + x2) // 2
                my = (y1 + y2) // 2

                vx, vy = line1[0], line1[1]

                if vx != 0:
                    lefty = int((-mx * vy / vx) + my)
                    righty = int(((width - mx) * vy / vx) + my)

                    cv.line(image, (width - 1, righty), (0, lefty), (0, 0, 255), 3)
                    cv.circle(image, (mx, my), 7, (0, 0, 255), 4)

        except cv2.error as e:
            print(e)

    return image
