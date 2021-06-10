import dlib         
import numpy as np 
import cv2         
import pandas as pd 
import PySimpleGUI as sg
import Pack

# 同上
facerec = dlib.face_recognition_model_v1("datasource/dlib_face_recognition_resnet_model_v1.dat")


# 計算兩個比較的臉平均距離
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    print("e_distance: ", dist)

    # 以0.4作為基準
    if dist > 0.4:
        return "diff"
    else:
        return "same"


# 所有人的特徵平均檔案
path_features_known_csv = "data/features_all.csv"
csv_rd = pd.read_csv(path_features_known_csv, header=None)

# 所有人的資料
features_known_arr = []

# 讀取已經有的臉
for i in range(csv_rd.shape[0]):
    features_someone_arr = []
    for j in range(0, len(csv_rd.loc[i, :])):
        features_someone_arr.append(csv_rd.loc[i, :][j])

    features_known_arr.append(features_someone_arr)
print("Faces in Database：", len(features_known_arr))

# 同上
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('/datasource/shape_predictor_68_face_landmarks.dat')

cap = cv2.VideoCapture(1)
cap.set(3, 480)
# 確定有長期出現臉的記數器
change = 0

# 取得臉部特徵(跟之前的一樣)
def get_128d_features(img_gray):
    faces = detector(img_gray, 1)
    if len(faces) != 0:
        face_des = []
        for i in range(len(faces)):
            shape = predictor(img_gray, faces[i])
            face_des.append(facerec.compute_face_descriptor(img_gray, shape))
    else:
        face_des = []
    return face_des

while cap.isOpened():

    flag, img_rd = cap.read()
    kk = cv2.waitKey(1)

    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    faces = detector(img_gray, 0)

    font = cv2.FONT_HERSHEY_COMPLEX

    cv2.putText(img_rd, "Press 'q': Quit", (20, 450),
                font, 0.8, (84, 255, 159), 1, cv2.LINE_AA)

    # 所有人的名字
    pos_namelist = []
    name_namelist = []

    # 按下 q 退出
    if kk == ord('q'):
        break
    else:
        # 有臉
        if len(faces) != 0:
            # 目前找到的臉數據會被放到這個陣列裡面
            features_cap_arr = []
            for i in range(len(faces)):
                shape = predictor(img_rd, faces[i])
                features_cap_arr.append(
                    facerec.compute_face_descriptor(img_rd, shape))

            # 把他跟每個原本就有的資料做比對
            for k in range(len(faces)):

                # 一開始不知道先當作是未知
                name_namelist.append("unknown")

                # 每個人人名的座標
                pos_namelist.append(tuple([faces[k].left(), int(
                    faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                # 去找到底像不像 (用上面的公式去找相異度)
                for i in range(len(features_known_arr)):
                    print("with person_", str(i+1), "the ", end='')
                    
                    compare = return_euclidean_distance(
                        features_cap_arr[k], features_known_arr[i])
                    if compare == "same":  # 有像
                        name_namelist[k] = "person_" + str(i+1)

                # 畫框
                for kk, d in enumerate(faces):
                    cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple(
                        [d.right(), d.bottom()]), (0, 255, 255), 2)

            # 把得到的結果寫下來
            for i in range(len(faces)):
                cv2.putText(
                    img_rd, name_namelist[i], pos_namelist[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)

            # 保險起見，連續三次不一樣才會進到訪客詢問清單內
            if name_namelist[0] == 'unknown':
                change = change - 1
            else:
                change = change + 1
    print("Name list now:", name_namelist, "\n")

    cv2.putText(img_rd, "Face Recognition", (20, 40),
                font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100),
                font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # 訪客
    if change < -3:
        change = 0
        Pack.main()
        print("access")

    # 住戶
    elif change > 3:
        change = 0
        sg.popup_auto_close('Your identity is verified.',
                            auto_close_duration=5)

    cv2.imshow("camera", img_rd)

cap.release()
cv2.destroyAllWindows()
