import cv2
import numpy as np

imgPath = 'C:/familyTree/backend/util/img/666.png'
# 读取图片并转换为HSV格式
image = cv2.imread(imgPath)
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

bilateImg = cv2.bilateralFilter(image, d=15, sigmaColor=75, sigmaSpace=75)
# cv2.namedWindow("bilateralFilter",cv2.WINDOW_NORMAL)
cv2.imshow("img", image)
cv2.imshow("bilateralFilter", bilateImg)

# 定义要分割的颜色范围（这里选择红色）
lower_red = np.array([0, 0, 0])
upper_red = np.array([10, 255, 255])

# 根据颜色范围创建掩模
mask = cv2.inRange(hsv_image, lower_red, upper_red)
# img = cv2.resize(image, (80,80), interpolation=cv2.INTER_CUBIC)
# cv2.imwrite("C:/familyTree/backend/util/img/41.png", img)

# def checkRow(rowData):
#     start_index = []
#     end_index = []
#     lastValue = 0
#     for index,item in np.ndenumerate(rowData):
#         if item > 0 and start_index == -1:
#             start_index = index[0]
#         if item > 0 and start_index > 0 and end_index == -1 and start_index < index[0]:
#             end_index = index[0]
#     return (start_index,end_index)


# row_index = 0
# while row_index < len(mask):
#     indexse = checkRow(mask[row_index])
#     if indexse[0] >0 and indexse[1]>0:
#         for i in range(indexse[1]-indexse[0]):
#             mask[row_index][indexse[0]+i] = 255
#     # print(indexse)
#     row_index +=1


# for row in mask:
#     print(row)
    # if np.mean(row) < 50:
    #     row = np.zeros(80)

# 对原始图像应用掩模
result = cv2.bitwise_and(image, image, mask=mask)

# cv2.namedWindow("Original Image",cv2.WINDOW_NORMAL)
# cv2.namedWindow("Result",cv2.WINDOW_NORMAL)
# 显示结果
# cv2.imshow("Original Image", image)
# cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

#=======================================处理曝光过度

# Load and read the input image
# img1 = cv2.imread(imgPath)
# image1 = cv2.cvtColor( cv2.imread(imgPath), cv2.COLOR_BGR2GRAY)
#
# # Apply adaptive histogram equalization (AHE) to adjust exposure
# equ = cv2.equalizeHist(image1)
#
# # Calculate edge information using Laplacian operator
# edges = cv2.Laplacian(equ, cv2.CV_64F).astype("uint8") * 50
#
# # Combine original image, AHE-processed image, and edge image for final result
# result1 = cv2.addWeighted(img1, 0.7, equ, 0.3, 0)
#
# # Display the output image
# cv2.imshow('Exposure Overexposed Repair', result1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()