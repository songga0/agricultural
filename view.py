import tensorflow as tf
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json

# 모델 불러오기
model = tf.keras.models.load_model("model.h5")

# 이미지를 로드하고 전처리
desired_width = 64
desired_height = 64
image_file_path = "C:/Users/Songis/Desktop/Cap2/QC/01.data/2.Validation/imgdata_230921_add/KakaoTalk_20231106_211314708.png"

images_to_predict = []

try:
    image = cv2.imread(image_file_path)
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
