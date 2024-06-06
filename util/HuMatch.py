import cv2
import numpy as np
from matplotlib import pyplot as plt

imgPath = "C:/familyTree/backend/util/img/1.png"


def testHu():
    img = cv2.imread(imgPath)
    mb = cv2.medianBlur(img, 9)
    grayImg = cv2.cvtColor(mb, cv2.COLOR_BGR2GRAY)
    d, a = cv2.threshold(grayImg, 50, 100, 0)
    # cv2.imshow("gray", grayImg)
    # cv2.imshow("a", a)
    c, h = cv2.findContours(a, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(c),h)
    cv2.drawContours(img, c, -1, (0, 20, 0), 1)
    cv2.imshow("a", img)
    cv2.waitKey(0)


def testC():
    # 读取图像
    image = cv2.imread(imgPath)
    mb = cv2.medianBlur(image, 9)
    # cv2.imshow("medianBlur",mb)
    # cv2.waitKey(0)
    # 转换到灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算直方图
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # 归一化直方图以便可以可视化
    hist_normalized = hist / hist.max()

    # 创建直方图图像
    plt.figure()
    plt.title('Brightness Histogram')
    plt.xlabel('Brightness Level')
    plt.ylabel('Number of Pixels')
    plt.plot(hist_normalized)
    plt.xlim([0, 256])
    plt.show()


def testLine():
    points = np.random.rand(30, 2) * 300
    # 转换为np.float32类型
    points = points.astype(np.float32)
    # 拟合到直线
    [vx, vy, x, y] = cv2.fitLine(points, cv2.DIST_L2, 0, 0.01, 0.01)
    print(vx, vy, x, y)
    # 创建一张黑色的图片用于绘制
    image = np.zeros((300, 300, 3), np.uint8)
    # 绘制原始数据点
    for i in range(len(points)):
        cv2.circle(image, (int(points[i][0]), int(points[i][1])), 3, (0, 0, 255), -1)
    # 绘制拟合出来的直线
    cv2.line(image, (int(x), int(y)), (int(x + vx), int(y + vy)), (0, 255, 0), 2)
    # 显示图片
    cv2.imshow('Curve Fitting', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    testLine()
    # testC()
    # testHu()
