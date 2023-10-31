from utils import testCase, IMAGES, GENERATE_PARAM, SORT_METHOD
from metrics import METRICS_NAME

METRICS_SET = [
    METRICS_NAME.BLUR,
    METRICS_NAME.INTERSECTION_OVER_UNION,
    METRICS_NAME.FALSE_DISCOVERY_RATE,
    METRICS_NAME.FALSE_NEGATIVE_RATE
]

IMAGES_SET = [
    IMAGES.INPUT,
    IMAGES.OUTPUT_3D
]

if __name__ == '__main__':
    testCase(
        start_img_id = 1, end_img_id = 5, start_param = 0, end_param = 100, param_step = 10, metrics_name = METRICS_SET,
        repeat = 3, filename = "blur_solution", generate_mode = 3, generate_param = GENERATE_PARAM.KERNEL_SIZE, images = IMAGES_SET,
        output_generate = 3, sort_method = SORT_METHOD.NOT_REVERSE
    )
