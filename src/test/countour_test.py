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

    ground_truth = cv2.imread("output_croped.png",0)
    ground_truth_resized = cv2.resize(ground_truth, dimension)

    prediction = cv2.imread("output_3d_m.png", 0)
    prediction_resized = cv2.resize(prediction, dimension)

    color_map = np.array([[0.5,0.5,0.5],
                          [  0,  1,  0],
                          [  1,  0,  0],
                          [  1,  1,  1]])

    _, thresh_gt = cv2.threshold(ground_truth_resized, 1, 1, 0)
    _, thresh_prediction = cv2.threshold(prediction_resized, 1, 2, 0)

    # Visualize mask
    _, mask = cv2.threshold(prediction_resized, 1, 255, 0)
    cv2.imwrite("map_mask.png", mask)

    # Create new image as numpy matrix with sum of two masks
    result_set = color_map[thresh_gt + thresh_prediction]

    # Modiffy to counterer occurrences
    result_set_reshaped = result_set.reshape(-1, result_set.shape[-1])
    result_set_tuples =  [tuple(x) for x in result_set_reshaped]
    result_set_counter = Counter(result_set_tuples)

    # True Positive
    counter_TP = result_set_counter[tuple([1, 1, 1])]

    # False Negative
    counter_FN = result_set_counter[tuple([0, 1, 0])]

    # False Positive
    counter_FP = result_set_counter[tuple([1, 0, 0])]

    # Correction plus errors occurrences
    counterer_TP_FN_FP = counter_TP + counter_FN + counter_FP

    # Visualize result set
    result_set_image = numpytoimage(result_set)
    result_set_image.save("result_set.png")

    result = (counter_TP / counterer_TP_FN_FP) * 100
    print(f'O resultado eh {result:.2f}%')
