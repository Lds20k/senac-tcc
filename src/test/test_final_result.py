from utils import testCase, IMAGES, GENERATE_PARAM
from metrics import METRICS_NAME

METRICS_SET = [
    METRICS_NAME.INTERSECTION_OVER_UNION,
    METRICS_NAME.ACCURACY,
    METRICS_NAME.F1_SCORE,
    METRICS_NAME.MATTHEWS_CORRELATION_COEFFICIENT,
    METRICS_NAME.FALSE_DISCOVERY_RATE,
    METRICS_NAME.FALSE_NEGATIVE_RATE,
    METRICS_NAME.DURATION,
]

IMAGES_SET = [
    IMAGES.INPUT,
    IMAGES.OUTPUT_2D,
    IMAGES.OUTPUT_3D
]

if __name__ == '__main__':
    # Testar primeiro
    testCase(
        start_img_id = 1, end_img_id = 1, start_param = 250, end_param = 250, param_step = 10, metrics_name = METRICS_SET,
        repeat = 1, filename = "final", generate_mode = 3, generate_param = GENERATE_PARAM.POINTS, images = IMAGES_SET,
        output_generate = 1
    )
