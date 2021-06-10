import dlib        
import numpy as np  
import cv2          

import os          
import shutil
# 人臉辨識器(內建)
detector = dlib.get_frontal_face_detector()

# 特徵預估器(載入)
predictor = dlib.shape_predictor('/datasource/shape_predictor_68_face_landmarks.dat')

# 攝影機設定(0為內建)
cap = cv2.VideoCapture(1)
cap.set(3, 480)

# counter
cnt_ss = 0

# 儲存資料夾
current_face_dir = 0

# 路徑
path_make_dir = "data/faces_from_camera/"
path_csv = "data/csvs_from_camera/"

# 目前數量
person_cnt = 0

while cap.isOpened():
    flag, im_rd = cap.read()

    # 設定延遲一毫秒
    kk = cv2.waitKey(1)

    # 灰階處理
    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

    # 偵測到的臉
    faces = detector(img_gray, 0)

    # 字體
    font = cv2.FONT_HERSHEY_COMPLEX

    # 按下 'n' 新建資料夾
    if kk == ord('n'):
        person_cnt += 1
        current_face_dir = path_make_dir + "person_" + str(person_cnt)
        print('\n')
        for dirs in (os.listdir(path_make_dir)):
            if current_face_dir == path_make_dir + dirs:
                shutil.rmtree(current_face_dir)
                print("刪除資料夾:", current_face_dir)
        os.makedirs(current_face_dir)
        print("新建的資料夾: ", current_face_dir)

        # 計數器歸零
        cnt_ss = 0

    # 有臉
    if len(faces) != 0:
        # 臉部框架
        for k, d in enumerate(faces):

            # 長方形形大小
            # (x,y)
            pos_start = tuple([d.left(), d.top()])
            pos_end = tuple([d.right(), d.bottom()])
            height = (d.bottom() - d.top())
            width = (d.right() - d.left())

            hh = int(height/2)
            ww = int(width/2)

            # 產生畫出來的長方形
            cv2.rectangle(im_rd,
                          tuple([d.left()-ww, d.top()-hh]),
                          tuple([d.right()+ww, d.bottom()+hh]),
                          (0, 255, 255), 2)

            # 畫圖
            im_blank = np.zeros((height*2, width*2, 3), np.uint8)
            # 按下 's' 把照片存下來
            if kk == ord('s'):
                cnt_ss += 1
                for ii in range(height*2):
                    for jj in range(width*2):
                        im_blank[ii][jj] = im_rd[d.top()-hh + ii][d.left()-ww + jj]
                cv2.imwrite(current_face_dir + "/img_face_" + str(cnt_ss) + ".jpg", im_blank)
                print("寫入：", str(current_face_dir) + "/img_face_" + str(cnt_ss) + ".jpg")

        # 顯示臉
    cv2.putText(im_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    # 說明檔
    cv2.putText(im_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(im_rd, "N: New face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(im_rd, "S: Save face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(im_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

    # 按下 'q' 退出
    if kk == ord('q'):
        break

    cv2.imshow("camera", im_rd)

cap.release()
cv2.destroyAllWindows()