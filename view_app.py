import tensorflow as tf
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json
import os
from shutil import copyfile
import datetime

# 모델 불러오기
model = tf.keras.models.load_model("model.h5")

# 이미지를 로드하고 전처리
desired_width = 64
desired_height = 64

# 사용자가 찍은 이미지를 저장할 디렉토리
save_dir = "user_images"
os.makedirs(save_dir, exist_ok=True)

# 현재 시간을 기반으로 이미지 파일 이름 생성
image_filename = f"user_image_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"

# 이미지를 찍어 user_images 디렉토리에 저장하고 전처리

# 이미지 예측 수행
images_to_predict = []

try:
    image = cv2.imread(os.path.join(save_dir, image_filename))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (desired_width, desired_height))
    image = image / 255.0
    images_to_predict.append(image)
except Exception as e:
    print(f"Error processing image: {e}")

# JSON 파일에서 레이블 정보 로드
with open("dataset.json", 'r') as f:
    data = json.load(f)
    labels = [entry["class_label"] for entry in data]

# LabelEncoder 생성 및 학습 데이터에 적용
label_encoder = LabelEncoder()
label_encoder.fit(labels)

# 이미지 예측 수행
predictions = model.predict(np.array(images_to_predict))

# 예측 결과 출력
predicted_labels = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

# 예측 결과 출력
print("Predicted Label:", predicted_labels[0])

# 이미지를 별도의 디렉토리에 복사하여 보관
user_image_path = os.path.join(save_dir, image_filename)
user_image_save_path = os.path.join("saved_user_images", image_filename)
os.makedirs("saved_user_images", exist_ok=True)
copyfile(user_image_path, user_image_save_path)
