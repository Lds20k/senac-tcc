from utils import testCase, IMAGES, GENERATE_PARAM
from metrics import METRICS_NAME

METRICS_SET = {
    METRICS_NAME.INTERSECTION_OVER_UNION,
    METRICS_NAME.BLUR
}

IMAGES_SET = {
    IMAGES.INPUT,
    IMAGES.OUTPUT_3D
}

if __name__ == '__main__':
    testCase(
        start_img_id = 1, end_img_id = 1, start_param = 0, end_param = 100, param_step = 100, metrics_name = METRICS_SET,
        repeat = 3, filename = "blur_error", generate_mode = 2, generate_param = GENERATE_PARAM.KERNEL_SIZE, images = IMAGES_SET
    )
