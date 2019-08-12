#!/usr/bin/env python3
# encoding: utf-8

"""
@version: 3.7
@author: kavin
@file: cv_code.py
@time: 2019-08-12 23:16
"""
import cv2
import numpy as np


def print_cv_version():
    print('opencv version is ' + cv2.__version__)


def blur_image(img_name):
    img = cv2.imread('./uploads/src/' + img_name)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5), np.float32) / 25
    dst = cv2.filter2D(img_gray, -1, kernel)
    cv2.imwrite('./uploads/dst/' + img_name, dst)
