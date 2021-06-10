import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np
import pandas as pd

path_faces_rd = "data/faces_from_camera/"
path_csv = "data/csvs_from_camera/"

detector = dlib.get_frontal_face_detector()

# 同上
predictor = dlib.shape_predictor("/datasource/shape_predictor_68_face_landmarks.dat")

# 人臉識別模型
# 把臉部特徵轉換為128維度的資料
facerec = dlib.face_recognition_model_v1("/datasource/dlib_face_recognition_resnet_model_v1.dat")


# 取得單張圖的128維度特徵
def return_128d_features(path_img):
    img = io.imread(path_img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 1)

    print("檢查圖片：", path_img, "\n")

    # 可能會遇到截圖後偵測不到人臉 所以要再次確認這次的截圖有偵測到
    if len(faces) != 0:
        shape = predictor(img_gray, faces[0])
        face_descriptor = facerec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0
        print("no face")

    return face_descriptor


# 把特徵取出後寫入csv檔
def write_into_csv(path_faces_personX, path_csv):
    dir_pics = os.listdir(path_faces_personX)
    with open(path_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(dir_pics)):

            # 1. 用上面的函式找到臉部特徵
            print("目前讀取的臉：", path_faces_personX + "/" + dir_pics[i])
            features_128d = return_128d_features(path_faces_personX + "/" + dir_pics[i])

            # 2. 沒臉的話跳過 有的話就寫入
            if features_128d == 0:
                i += 1
            else:
                writer.writerow(features_128d)


# 每個人輪過一次
faces = os.listdir(path_faces_rd)
for person in faces:
    print(path_csv + person + ".csv")
    write_into_csv(path_faces_rd + person, path_csv + person + ".csv")


# 給整體資料使用: 計算每個人的平均之後再寫到新的資料中
def compute_the_mean(path_csv_rd):
    column_names = []

    # 取出特徵
    for feature_num in range(128):
        column_names.append("features_" + str(feature_num + 1))

    # 讀取csv
    rd = pd.read_csv(path_csv_rd, names=column_names)

    feature_mean = []

    # 存放特徵值
    for feature_num in range(128):
        tmp_arr = rd["features_" + str(feature_num + 1)]
        tmp_arr = np.array(tmp_arr)

        # 計算此刻這個的平均
        tmp_mean = np.mean(tmp_arr)
        feature_mean.append(tmp_mean)
    return feature_mean


# 存所有特徵平均的檔案
path_csv_feature_all = "data/features_all.csv"

# 存人臉特徵的csv路徑
path_csv_rd = "data/csvs_from_camera/"

with open(path_csv_feature_all, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    csv_rd = os.listdir(path_csv_rd)

    for i in range(len(csv_rd)):
        feature_mean = compute_the_mean(path_csv_rd + csv_rd[i])
        writer.writerow(feature_mean)