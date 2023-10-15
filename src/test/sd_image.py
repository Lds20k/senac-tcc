import numpy as np
import cv2

dimension = (300, 300)

if __name__ == '__main__':
    extract = cv2.imread("output_2d.png", 0)
    extract_resized = cv2.resize(extract, dimension)

    std_before = np.std(extract_resized)

    ksize = (40, 40)
    blur_image = cv2.blur(extract_resized, ksize)

    std_after = np.std(blur_image)

    std_diff = std_before - std_after

    cv2.imshow("Window", blur_image)
    cv2.waitKey(0)