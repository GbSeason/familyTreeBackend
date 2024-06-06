from ml_ann import TestAnn

if __name__ == '__main__':

    tn = TestAnn()
    # 训练模型
    # gdata = tn.generate_data("C:/familyTree/backend/util/img/", None)
    # print(len(gdata[0][0]))
    # tn.mlpTrain(gdata[0], gdata[1])
    #测试识别
    tn.annPredict("C:/familyTree/backend/util/ANN_MLPTrainCase.xml",
                  "C:/familyTree/backend/util/img/4.png")

