from math import sqrt
import os
import sys
from PIL import Image
import numpy as np
import cv2
from collections import Counter
import time
import re

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import generate_map

def numpytoimage(numpy):
    numpy = numpy * 255
    image= Image.fromarray(numpy.astype(np.uint8))
    return image

def get_char_for_number(i):
    return chr(i + 64)

DIMENSION = (300, 300)

# Cases 1 to 3
CASE_ID = 1
METRICS_QUANTITY = 5

ITERATIONS_PER_POINTS = 3
QUANTITY_OF_IMAGES = 5
START_KERNEL_SIZE = 0
END_KERNEL_SIZE = 101
SIZE_STEPS = 10

def measureBlur(img):
    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img,  cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    return np.std(grad_mag)

def find_best_blur():
    all_results = {}

    for img_num in range(1, QUANTITY_OF_IMAGES + 1):
        print(f'Imagem {img_num}')
        ground_truth = cv2.imread(f'src/test/images/test-{img_num}.png', 0)
        ground_truth_resized = cv2.resize(ground_truth, DIMENSION)

        img = cv2.cvtColor(ground_truth_resized, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        retriyng_counter = 0

        for i in range(START_KERNEL_SIZE, END_KERNEL_SIZE, SIZE_STEPS):
            metrics = np.zeros(METRICS_QUANTITY)
            for j in range (0, ITERATIONS_PER_POINTS):
                while True:
                    try:
                        generate_map.generate(im_pil, points=150, mode=3, kernel_size=75)
                        break
                    except Exception as e:
                        print(f"Ocorreu um erro: {e}. Tentando novamente...")
                        retriyng_counter += 1

                map_2d = cv2.imread("output_2d.png")
                ocean_color = (255,191,0)
                mask = cv2.inRange(map_2d, ocean_color, ocean_color)
                map_2d = cv2.bitwise_not(mask)
                map_2d_resized = cv2.resize(map_2d, DIMENSION)

                prediction = cv2.imread("output_3d.png", 0)
                prediction_resized = cv2.resize(prediction, DIMENSION)

                color_map = np.array([[0.5,0.5,0.5],
                                    [  0,  1,  0],
                                    [  1,  0,  0],
                                    [  1,  1,  1]])

                _, thresh_gt = cv2.threshold(map_2d_resized, 1, 1, 0)
                _, thresh_prediction = cv2.threshold(prediction_resized, 1, 2, 0)

                # Create new image as numpy matrix with sum of two masks
                result_set = color_map[thresh_gt + thresh_prediction]

                # Modiffy to counterer occurrences
                result_set_reshaped = result_set.reshape(-1, result_set.shape[-1])
                result_set_tuples =  [tuple(x) for x in result_set_reshaped]
                result_set_counter = Counter(result_set_tuples)

                # True Positive
                counter_TP = result_set_counter[tuple([1, 1, 1])]

                # True Negative
                counter_TN = result_set_counter[tuple([0.5, 0.5, 0.5])]

                # False Negative
                counter_FN = result_set_counter[tuple([0, 1, 0])]

                # False Positive
                counter_FP = result_set_counter[tuple([1, 0, 0])]

                # evaulate metrics
                sm = measureBlur(prediction_resized)
                metrics[0] += sm

                iou = counter_TP / (counter_TP + counter_FP + counter_FN)
                metrics[1] += iou

                fdr = counter_FP / (counter_TP + counter_FP)
                metrics[2] += fdr

                fnr = counter_FN / (counter_TP + counter_FN)
                metrics[3] += fnr

                acc = (counter_TP + counter_TN) / (counter_TP + counter_TN + counter_FP + counter_FN)
                metrics[4] += acc

                # Visualize result set
                result_set_image = numpytoimage(result_set)
                result_set_image.save("result_set.png")

            if not isinstance(all_results.get(i), np.ndarray):
                all_results[i] = np.zeros(METRICS_QUANTITY)
            all_results[i] += metrics

    sorted_dict = all_results
    sorted_dict = dict(sorted(all_results.items(), key=lambda x: x[1][0], reverse=False))

    for key, value in sorted_dict.items():
        for i in range(len(value)):
            value[i] = f'{ (value[i] / (ITERATIONS_PER_POINTS * QUANTITY_OF_IMAGES)):.5f}'
        sorted_dict[key] = value.astype(str)

    print(sorted_dict)

    with open(f'latex/table_find_best_blur.tex', "w", encoding='utf-8') as f:
        backreturn = "\\\\\n" + " "*8

        content = backreturn.join([
            f"{_k} & {' & '.join(_v)}"
            for _k, _v in sorted_dict.items()
        ])

        f.write(re.sub(r"\s{16}(?=\{|\d|\\)", "",
                f"""
                \\begin{{table}}[h]
                    \\centering
                    \\caption{{Resultados dos testes de contorno}}
                    \\label{{tab:resultados-contorno}}
                    \\begin{{tabular}}{{|l|c|c|}}
                        \\hline
                        {{Pontos}} & {{Média da porcentagem}} & {{Média da duração em segundos}} \\\\
                        \\hline
                        {content}\\\\
                        \\hline
                    \\end{{tabular}}
                \\end{{table}}
                """.strip()))

if __name__ == '__main__':
    find_best_blur()
