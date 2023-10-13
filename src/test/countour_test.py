from PIL import Image
import numpy as np
import cv2
from collections import Counter

def numpytoimage(numpy):
    numpy = numpy * 255
    image= Image.fromarray(numpy.astype(np.uint8))
    return image

dimension = (300, 300)

if __name__ == '__main__':

    reference = cv2.imread("output_croped.png",0)
    reference_resized = cv2.resize(reference, dimension)


    # extract = cv2.imread("output_2d.png")

    extract = cv2.imread("output_3d.png", 0)
    extract_resized = cv2.resize(extract, dimension)


    # height = extract.shape[0]
    # width = extract.shape[1]
    # image = Image.new('RGB', (width, height))

    # for x_in in range(width):
    #     for y_in in range(height):
    #         pixel_color = extract[y_in, x_in]

    #         if pixel_color[0] == 255 and pixel_color[1] == 191 and pixel_color[2] == 0:
    #             image.putpixel((x_in, y_in), (0, 0, 0))
    #         else:
    #             image.putpixel((x_in, y_in), (255, 255, 255))

    # open_cv_image = np.array(image)
    # open_cv_image = open_cv_image[:, :, ::-1].copy()
    # gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # cv2.imwrite("map_mask.png", gray)

    lut = np.array([[0.5,0.5,0.5],
        [  0,  1,  0],
        [  1,  0,  0],
        [  1,  1,  1]])

    _, thresh_ref = cv2.threshold(reference_resized, 75, 1, 0)

    # _, thresh_extract = cv2.threshold(gray, 75, 2, 0)
    _, thresh_extract = cv2.threshold(extract_resized, 1, 2, 0)

    _, mask_example = cv2.threshold(extract_resized, 1, 255, 0)
    cv2.imwrite("map_mask.png", mask_example)

    C = lut[thresh_ref + thresh_extract]

    C_reshaped = C.reshape(-1, C.shape[-1])
    C_tuples =  [tuple(x) for x in C_reshaped]

    C_counter = Counter(C_tuples)
    counter_correct = C_counter[tuple([1, 1, 1])]
    count_error_1 = C_counter[tuple([0, 1, 0])]
    count_error_2 = C_counter[tuple([1, 0, 0])]

    counter_correct_and_errors = counter_correct + count_error_1 + count_error_2

    C_image = numpytoimage(C)
    C_image.save("quality.png")

    result = (counter_correct / counter_correct_and_errors) * 100
    print(f'O resultado eh {result}%')
