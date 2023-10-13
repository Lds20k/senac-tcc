from PIL import Image
import numpy as np
import cv2

def numpytoimage(numpy):
    numpy = numpy * 255
    image= Image.fromarray(numpy.astype(np.uint8))
    return image


if __name__ == '__main__':
    reference = cv2.imread("output_croped.png",0)
    _, thresh_ref = cv2.threshold(reference, 75, 255, 0)

    extract = cv2.imread("output_2d.png")

    height = extract.shape[0]
    width = extract.shape[1]

    image = Image.new('RGB', (width, height))

    flag = False
    for x_in in range(width):
        for y_in in range(height):
            pixel_color = extract[y_in, y_in]

            if not flag:
                print(pixel_color)
                flag = True

            if pixel_color[0] == 255 and pixel_color[1] ==  191 and pixel_color[2] == 0:
                image.putpixel((x_in, y_in), (255, 255, 255))
            else:
                image.putpixel((x_in, y_in), (0, 0, 0))

    open_cv_image = np.array(image) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    _, thresh_extract = cv2.threshold(open_cv_image, 75, 255, 0)


    C = np.zeros(shape=(len(thresh_ref), len(thresh_ref[0]), 3))

    for i in range (0, thresh_ref.shape[0],1):
        for j in range(0, thresh_ref.shape[1], 1):
            if np.all(thresh_ref[i][j] == thresh_extract[i][j]) and thresh_ref[i][j] == 0:
                C[i][j] = 1
            elif thresh_ref[i][j] == 0:
                C[i][j][0] = 0
                C[i][j][1] = 1
                C[i][j][2] = 0
            elif np.any(thresh_extract[i][j]) == 0:
                C[i][j][0] = 1
                C[i][j][1] = 0
                C[i][j][2] = 0
            else:
                C[i][j][0] = 0.5
                C[i][j][1] = 0.5
                C[i][j][2] = 0.5

    C_image = numpytoimage(C)
    C_image.save("quality.png")
