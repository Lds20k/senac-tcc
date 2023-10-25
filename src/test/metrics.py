from enum import Enum
import cv2
import numpy as np
from math import sqrt


class METRICS_NAME(Enum):
    BLUR = 1
    INTERSECTION_OVER_UNION = 2
    F1_SCORE = 3
    MATTHEWS_CORRELATION_COEFFICIENT = 4
    FALSE_DISCOVERY_RATE = 5
    FALSE_NEGATIVE_RATE = 6
    ACCURACY = 7

def measureBlur(img):
    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img,  cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    return np.std(grad_mag)

def iou(TP, TN, FP, FN):
    return TP / (TP + FP + FN)


def f1(TP, TN, FP, FN):
    return TP / (TP + FP/2 + FN/2)


def mcc(TP, TN, FP, FN):
    return (TP * TN - FP * FN)/ sqrt((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN))


def fdr(TP, TN, FP, FN):
    return FP / (TP + FP)


def fnr(TP, TN, FP, FN):
    return FN / (TP + FN)


def acc(TP, TN, FP, FN):
    return (TP + TN) / (TP + TN + FP + FN)


METRICS_DICT = {
METRICS_NAME.BLUR: [measureBlur, "Blur"],
METRICS_NAME.INTERSECTION_OVER_UNION: [iou,"IoU"],
METRICS_NAME.F1_SCORE: [f1,"F1"],
METRICS_NAME.MATTHEWS_CORRELATION_COEFFICIENT: [mcc,"MCC"],
METRICS_NAME.FALSE_DISCOVERY_RATE: [fdr,"FDR"],
METRICS_NAME.FALSE_NEGATIVE_RATE: [fnr,"FNR"],
METRICS_NAME.ACCURACY: [acc,"Acc"],
}
