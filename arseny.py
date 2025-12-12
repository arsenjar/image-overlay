# # import numpy as np
# # import cv2 as cv
# # import cv2
# #
# # def display_midpoint(fitted_line, color, image_circles):
# #     if fitted_line is not None:
# #         vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
# #         print(x0, y0)
# #         cv.circle(image_circles, (x0, y0), 5, color, 4)
# # def arsenyCode(image):
# #     # Capture frame-by-frame
# #     points = []
# #     # if frame is read correctly ret is True
# #     if image is None:
# #         print("Can't receive frame (stream end?). Exiting ...")
# #         return image
# #     w, h = image.shape[:2]
# #     height, width = image.shape[:2]
# #     image_lines = np.zeros((height, width, 3), dtype=np.uint8)
# #     image_circles = np.zeros((height, width, 3), dtype=np.uint8)
# #     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# #     blur = cv.GaussianBlur(gray, (5, 5), 0)
# #     edges = cv.Canny(blur, 50, 150)
# #
# #     lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180, threshold=100, minLineLength=100, maxLineGap=50)
# #
# #     def draw_extended_line(fitted_line, color):
# #         if fitted_line is not None:
# #             vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
# #             #print(fitted_line[0, 0], fitted_line[1, 0], fitted_line[2, 0], fitted_line[3, 0])
# #             if vx != 0:
# #                 lefty = int((-x0 * vy / vx) + y0)
# #                 righty = int(((width - x0) * vy / vx) + y0)
# #
# #                 cv.line(image, (width - 1, righty), (0, lefty), color, 2)
# #                 return (int(x0), int(y0))
# #                 #cv.circle(image, (x0, y0), 5, (0, 0, 255), 4)
# #             # midpoint_x = (vx + x0) // 2
# #             # midpoint_y = (vy + y0) // 2
# #             # cv2.circle(image_lines, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
# #
# #     if lines is not None:
# #         for line in lines:
# #             x1, y1, x2, y2 = line[0]
# #
# #             midpoint_x = (x1 + x2) // 2
# #
# #             midpoint_y = (y1 + y2) // 2
# #
# #             #cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 4)
# #             #cv2.line(image_lines, (x1, y1), (x2, y2), (255, 0, 255), 4)
# #             edges_blur = cv2.GaussianBlur(image_lines, (7, 7), 10)
# #             cv2.line(edges_blur, (x1, y1), (x2, y2), (255, 0, 0), 4)
# #
# #             cv2.circle(image_lines, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
# #             points.append((midpoint_x, midpoint_y))
# #     right_points = []
# #     left_points = []
# #
# #     for x, y in points:
# #         if x > w // 2:
# #             right_points.append((x, y))
# #         else:
# #             left_points.append((x, y))
# #     # numpy array
# #     right_points_np = np.array(right_points)
# #     left_points_np = np.array(left_points)
# #     try:
# #         right_line = cv.fitLine(right_points_np, cv.DIST_L1, 1, 0.01, 0.01)
# #         left_line = cv.fitLine(left_points_np, cv.DIST_L1, 1, 0.01, 0.01)
# #         #draw_extended_line(right_line, (0, 255, 255))
# #         #draw_extended_line(left_line, (0, 255, 0))
# #         centroid_r = draw_extended_line(right_line, (0, 255,  255))
# #         centroid_l = draw_extended_line(left_line, (0, 255, 0))
# #         if centroid_r is not None:
# #             # Draw the centroid circle for the right line on its overlay
# #             cv.circle(image, centroid_r, 5, (0, 0, 255), 4) # RED
# #         if centroid_l is not None:
# #             # Draw the centroid circle for the right line on its overlay
# #             cv.circle(image, centroid_l, 5, (0, 0, 255), 4) # RED
# #
# #         cv2.line(image, centroid_r, centroid_l, (255, 100, 100), 4)
# #
# #         x1, y1 = centroid_r[0], centroid_r[1]
# #         x2, y2= centroid_l[0], centroid_l[1]
# #
# #         midpoint_x = (x1 + x2) // 2
# #
# #         midpoint_y = (y1 + y2) // 2
# #
# #         cv2.circle(image, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
# #
# #
# #         # display_midpoint(right_line, (0, 255, 0), image_circles)
# #         # display_midpoint(left_line, (0, 255, 0), image_circles)
# #
# #     except:
# #         print("Can't find right line")
# #
# #     return image
# import numpy as np
# import cv2 as cv
# import cv2
#
#
# def display_midpoint(fitted_line, color, image_circles):
#     if fitted_line is not None:
#         vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
#         print(x0, y0)
#         cv.circle(image_circles, (x0, y0), 5, color, 4)
#
# def arsenyCode(image):
#     points = []
#
#     # Check if camera properly loaded.
#     if image is None:
#         print("Can't receive frame (stream end?). Exiting ...")
#         return image
#     # w, h = image.shape[:2]
#
#     height, width = image.shape[:2]
#     output = image.copy()
#
#     #creating matrix's
#     image_lines = np.zeros((height, width, 3), dtype=np.uint8)
#     image_circles = np.zeros((height, width, 3), dtype=np.uint8)
#
#     #preporation for line detection
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#     blur = cv.GaussianBlur(gray, (9, 9), 0)
#     _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
#     kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
#     closed = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
#     edges = cv.Canny(closed, 20, 80)
#
#     # Line detection
#     lines = cv2.HoughLinesP(
#         edges,
#         rho=1,
#         theta=np.pi / 180,
#         threshold=40,
#         minLineLength=200,
#         maxLineGap=120
#     )
#
#
#     def draw_extended_line(fitted_line, color):
#         if fitted_line is not None:
#             vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
#             #print(fitted_line[0, 0], fitted_line[1, 0], fitted_line[2, 0], fitted_line[3, 0])
#             if vx != 0:
#                 lefty = int((-x0 * vy / vx) + y0)
#                 righty = int(((width - x0) * vy / vx) + y0)
#
#                 cv.line(output, (width - 1, righty), (0, lefty), color, 2)
#                 return (int(x0), int(y0))
#                 #cv.circle(image, (x0, y0), 5, (0, 0, 255), 4)
#             # midpoint_x = (vx + x0) // 2
#             # midpoint_y = (vy + y0) // 2
#             # cv2.circle(image_lines, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
#         return None
#
#     if lines is not None:
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#
#             midpoint_x = (x1 + x2) // 2
#
#             midpoint_y = (y1 + y2) // 2
#
#             edges_blur = cv2.GaussianBlur(image_lines, (7, 7), 10)
#             cv2.line(edges_blur, (x1, y1), (x2, y2), (255, 0, 0), 4)
#             cv2.circle(image_lines, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
#             points.append((midpoint_x, midpoint_y))
#
#     # right_points = []
#     # left_points = []
#
#     points_np = np.float32(points)
#
#     if len(points_np) >= 2:
#         try:
#
#             criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
#             K = 2
#             ret, labels, centers = cv2.kmeans(points_np, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
#
#             group1_points = points_np[labels.ravel() == 0]
#             group2_points = points_np[labels.ravel() == 1]
#
#             centroids = []
#
#             if len(group1_points) > 1:
#                 line1 = cv2.fitLine(group1_points, cv2.DIST_L1, 1, 0.01, 0.01)
#                 centroid1 = draw_extended_line(line1, (255, 255, 0))  # Cyan
#                 if centroid1 is not None:
#                     centroids.append(centroid1)
#                     # Draw centroid circle on the main image of first group
#                     cv2.circle(output, centroid1, 7, (255, 0, 0), 4)  # Blue
#
#             if len(group2_points) > 1:
#                 line2 = cv2.fitLine(group2_points, cv2.DIST_L1, 1, 0.01, 0.01)
#                 centroid2 = draw_extended_line(line2, (0, 255, 255))  # Yellow
#                 if centroid2 is not None:
#                     centroids.append(centroid2)
#                     # Draw centroid circle on the main image
#                     cv2.circle(output, centroid2, 7, (255, 0, 255), 4)
#
#             if len(centroids) == 2:
#                 (x1, y1), (x2, y2) = centroids
#
#                 mx = (x1 + x2) // 2
#                 my = (y1 + y2) // 2
#
#                 vx, vy = line1[0], line1[1]
#
#                 if vx != 0:
#                     lefty = int((-mx * vy / vx) + my)
#                     righty = int(((width - mx) * vy / vx) + my)
#
#                     cv.line(output, (width - 1, righty), (0, lefty), (0, 0, 255), 3)
#                     cv.circle(output, (mx, my), 7, (0, 0, 255), 4)
#
#
#
#         except cv2.error as e:
#             print(e)
#         return output
#     # for x, y in points:
#     #     if x > w // 2:
#     #         right_points.append((x, y))
#     #     else:
#     #         left_points.append((x, y))
#     # # numpy array
#     # right_points_np = np.array(right_points)
#     # left_points_np = np.array(left_points)
#     # try:
#     #     right_line = cv.fitLine(right_points_np, cv.DIST_L1, 1, 0.01, 0.01)
#     #     left_line = cv.fitLine(left_points_np, cv.DIST_L1, 1, 0.01, 0.01)
#     #     #draw_extended_line(right_line, (0, 255, 255))
#     #     #draw_extended_line(left_line, (0, 255, 0))
#     #     centroid_r = draw_extended_line(right_line, (0, 255,  255))
#     #     centroid_l = draw_extended_line(left_line, (0, 255, 0))
#     #     if centroid_r is not None:
#     #         # Draw the centroid circle for the right line on its overlay
#     #         cv.circle(image, centroid_r, 5, (0, 0, 255), 4) # RED
#     #     if centroid_l is not None:
#     #         # Draw the centroid circle for the right line on its overlay
#     #         cv.circle(image, centroid_l, 5, (0, 0, 255), 4) # RED
#     #
#     #     #cv2.line(image, centroid_r, centroid_l, (255, 100, 100), 4)
#     #
#     #     x1, y1 = centroid_r[0], centroid_r[1]
#     #     x2, y2= centroid_l[0], centroid_l[1]
#     #
#     #     midpoint_x = (x1 + x2) // 2
#     #
#     #     midpoint_y = (y1 + y2) // 2
#     #
#     #
#     #     cv2.circle(image, (midpoint_x, midpoint_y), radius=5, color=(0, 0, 255), thickness=4)
#     #     cv2.line(image, (midpoint_x, 0), (midpoint_x, 1280), (255, 0, 0), 4)
#     #
#     #     # display_midpoint(right_line, (0, 255, 0), image_circles)
#     #     # display_midpoint(left_line, (0, 255, 0), image_circles)
#     #
#     # except:
#     #     print("Can't find right line")



import numpy as np
import cv2 as cv
import cv2


def display_midpoint(fitted_line, color, image_circles):
    if fitted_line is not None:
        vx, vy, x0, y0 = fitted_line[0], fitted_line[1], fitted_line[2], fitted_line[3]
        print(x0, y0)
        cv.circle(image_circles, (x0, y0), 5, color, 4)

def arsenyCode(image):
    points = []
    #checking captured frames
    if image is None:
        return image

    height, width = image.shape[:2]
    output = image.copy()
    #image processing for bold lines
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (9, 9), 0)
    _, thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    closed = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
    edges = cv.Canny(closed, 20, 80)

    #line detection
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi / 180,threshold=40,minLineLength=200,
        maxLineGap=120
    )
    #function to draw extended lines
    def draw_extended_line(fitted_line, color):
        if fitted_line is not None:
            vx, vy, x0, y0 = fitted_line[0,0], fitted_line[1,0], fitted_line[2,0], fitted_line[3,0]
            if vx != 0:
                lefty = int((-x0 * vy / vx) + y0)
                righty = int(((width - x0) * vy / vx) + y0)
                cv.line(output, (width - 1, righty), (0, lefty), color, 2)
                return (int(x0), int(y0))
        return None

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            midpoint_x = (x1 + x2) // 2
            midpoint_y = (y1 + y2) // 2
            points.append((midpoint_x, midpoint_y))
    #making numpy array from points
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
                centroid1 = draw_extended_line(line1, (255, 255, 0))
                if centroid1 is not None:
                    centroids.append(centroid1)
                    cv2.circle(output, centroid1, 7, (255, 0, 0), 4)

            if len(group2_points) > 1:
                line2 = cv2.fitLine(group2_points, cv2.DIST_L1, 1, 0.01, 0.01)
                centroid2 = draw_extended_line(line2, (0, 255, 255))
                if centroid2 is not None:
                    centroids.append(centroid2)
                    cv2.circle(output, centroid2, 7, (255, 0, 255), 4)

            if len(centroids) == 2:
                (x1, y1), (x2, y2) = centroids
                mx = (x1 + x2) // 2
                my = (y1 + y2) // 2

                vx, vy = line1[0], line1[1]

                if vx != 0:
                    lefty = int((-mx * vy / vx) + my)
                    righty = int(((width - mx) * vy / vx) + my)
                    cv.line(output, (width - 1, righty), (0, lefty), (0, 0, 255), 3)
                    cv.circle(output, (mx, my), 7, (0, 0, 255), 4)

        except:
            pass

    return output