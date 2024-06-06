import random

import cv2
import os
import numpy as np


class TestAnn:
    def __init__(self):
        self.p_image_dir = ""
        self.resize = (50, 50)
        self.imgsize = 50
        self.xmlCaseName = "C:/familyTree/backend/util/ANN_MLPTrainCase.xml"

    def generate_data(self, file_dir, xmlName):
        if xmlName is not None:
            self.xmlCaseName = xmlName  # "ANN_MLPTrainCase.xml"
        train_data = []
        train_labels = np.zeros( 10, np.float32)  # 标签矩阵
        # labels_label = np.zeros((10, 1), np.float32)  # 标签矩阵
        if os.path.exists(file_dir):
            file_list = os.listdir(file_dir)
            index = 0
            for f in file_list:
                print(file_dir, f)
                img_name = os.path.join(file_dir, f)
                img = cv2.imread(img_name).astype(np.float32)
                img = cv2.resize(img, self.resize, interpolation=cv2.INTER_CUBIC)
                # cv2.imwrite(f"{file_dir}{random.random()}{f}", img)
                new_img = img.reshape(1, self.imgsize * self.imgsize*3)
                train_data.append(new_img[0])
                train_labels[index] = 1
                index += 1
        return np.array(train_data), train_labels

    def mlpTrain(self, train_data, train_labels):
        ann = cv2.ml.ANN_MLP.create()
        ann.setLayerSizes(np.array([self.imgsize * self.imgsize*3, 1000, 1]))  # 设置MLP的每一层维度，最前面是输入层，中间是隐藏层，最后的输出层维度
        ann.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM, 0.6, 1.0)  # 激活函数设置
        ann.setTrainMethod(cv2.ml.ANN_MLP_BACKPROP, 0.1, 0.1)  # 训练方式
        ann.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 100, 0.01))
        ann.train(train_data, cv2.ml.ROW_SAMPLE, train_labels)
        ann.save(self.xmlCaseName)

    def annPredict(self, caseXmlName, imgPath):
        ann = cv2.ml.ANN_MLP.load(caseXmlName)
        imgTarget = cv2.imread(imgPath).astype(np.float32)
        img = cv2.resize(imgTarget, self.resize, interpolation=cv2.INTER_CUBIC)
        new_img = img.reshape(1, self.imgsize * self.imgsize * 3)
        res = ann.predict(new_img)
        print(res)

