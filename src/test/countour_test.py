from PIL import Image
import numpy as np
import cv2

def numpytoimage(numpy):
    numpy = numpy * 255
    image= Image.fromarray(numpy.astype(np.uint8))
    return image


if __name__ == '__main__':
    reference = cv2.imread("output_croped.png",0)

    extract = cv2.imread("output_2d.png")

    height = extract.shape[0]
    width = extract.shape[1]
    image = Image.new('RGB', (width, height))

    for x_in in range(width):
        for y_in in range(height):
            pixel_color = extract[y_in, x_in]

            if pixel_color[0] == 255 and pixel_color[1] == 191 and pixel_color[2] == 0:
                image.putpixel((x_in, y_in), (0, 0, 0))
            else:
                image.putpixel((x_in, y_in), (255, 255, 255))

    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("map_mas.png", gray)

    # lut = [[  1,  1,  1],
    #     [  1,  0,  0],
    #     [  0,  1,  0],
    #     [0.5,0.5,0.5]]

    # _, thresh_ref = cv2.threshold(reference, 75, 1, 0)
    # _, thresh_extract = cv2.threshold(gray, 75, 2, 0)
    # C = lut[thresh_ref + thresh_extract]


    _, thresh_ref = cv2.threshold(reference, 75, 255, 0)
    _, thresh_extract = cv2.threshold(gray, 75, 255, 0)
    C = np.zeros(shape=(len(thresh_ref), len(thresh_ref[0]), 3))

    counter_correct = 0
    counter_correct_and_errors = 0

    for i in range (0, thresh_ref.shape[0],1):
        for j in range(0, thresh_ref.shape[1], 1):
            if thresh_ref[i][j] == thresh_extract[i][j] and thresh_ref[i][j] == 0:
                # sem nada nos dois

                C[i][j][0] = 0.5
                C[i][j][1] = 0.5
                C[i][j][2] = 0.5
            elif thresh_ref[i][j] == 0:
                C[i][j][0] = 1
                C[i][j][1] = 0
                C[i][j][2] = 0
                counter_correct_and_errors += 1
            elif np.any(thresh_extract[i][j]) == 0:
                C[i][j][0] = 0
                C[i][j][1] = 1
                C[i][j][2] = 0
                counter_correct_and_errors += 1
            else:
                # igual nos dois
                counter_correct += 1
                counter_correct_and_errors += 1
                C[i][j] = 1


    C_image = numpytoimage(C)
    C_image.save("quality.png")

    result = (counter_correct / counter_correct_and_errors) * 100
    print(f'O resultado eh {result}%')
