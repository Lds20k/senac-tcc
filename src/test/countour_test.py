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

DIMENSION = (300, 300)

ITERATIONS_PER_POINTS = 3
QUANTITY_OF_IMAGES = 5
START_QUANTITY_POINTS = 50
END_QUANTITY_POINTS = 301
SIZE_STEPS_POINTS = 50

def test_countour_image():
    all_results = {}

    for img_num in range(1, QUANTITY_OF_IMAGES + 1):
        print(f'Imagem {img_num}')
        ground_truth = cv2.imread(f'src/test/images/test-{img_num}.png', 0)
        ground_truth_resized = cv2.resize(ground_truth, DIMENSION)

        img = cv2.cvtColor(ground_truth_resized, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        retriyng_counter = 0

        for i in range(START_QUANTITY_POINTS, END_QUANTITY_POINTS, SIZE_STEPS_POINTS):
            sum_results = 0
            sum_durations = 0
            for j in range (0, ITERATIONS_PER_POINTS):
                while True:
                    try:
                        start_time = time.time()
                        generate_map.generate(im_pil, points=i)
                        end_time = time.time()
                        break
                    except Exception as e:
                        print(f"Ocorreu um erro: {e}. Tentando novamente...")
                        retriyng_counter += 1

                sum_durations += end_time - start_time

                prediction = cv2.imread("output_3d.png", 0)
                prediction_resized = cv2.resize(prediction, DIMENSION)

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
                sum_results += result
                print(f'O resultado eh {result:.2f}%')
            if all_results.get(i) == None:
                all_results[i] = [0, 0]
            all_results[i][0] += sum_results
            all_results[i][1] += sum_durations


    for key, value in all_results.items():
        value[0] = f'{ (value[0] / (ITERATIONS_PER_POINTS * QUANTITY_OF_IMAGES)):.2f}'
        value[1] = f'{ (value[1] / (ITERATIONS_PER_POINTS * QUANTITY_OF_IMAGES)):.2f}'
    print(all_results)

    with open("latex/tabela_contorno.tex", "w", encoding='utf-8') as f:
        backreturn = "\\\\\n" + " "*8

        content = backreturn.join([
            f"{_k} & {' & '.join(_v)}"
            for _k, _v in all_results.items()
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
    test_countour_image()
