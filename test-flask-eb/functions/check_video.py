from flask import Flask, request
import cv2
import tensorflow as tf
import numpy as np
from concurrent.futures import ThreadPoolExecutor

inception_model = tf.keras.applications.MobileNetV2(weights='imagenet')
input_shape = (224, 224)

def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, input_shape)
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    preprocessed_frame = tf.keras.applications.mobilenet_v2.preprocess_input(rgb_frame)
    return preprocessed_frame

def classify_frame(frame):
    preprocessed_frame = preprocess_frame(frame)
    preprocessed_frame = np.expand_dims(preprocessed_frame, axis=0)
    predictions = inception_model.predict(preprocessed_frame)
    return predictions

def contains_explicit_content(predictions, threshold=0.5):
    # "adult content" class index in ImageNet is 954
    return predictions[0][954] > threshold

def process_batch(frames):
    predictions = [classify_frame(frame) for frame in frames]
    return [contains_explicit_content(prediction) for prediction in predictions]

def process_video(video_path, batch_size=32, frame_decimation=10):
    video_capture = cv2.VideoCapture(video_path)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    executor = ThreadPoolExecutor(max_workers=4)
    batch = []
    for i in range(frame_count):
        ret, frame = video_capture.read()
        if not ret:
            break
        if i % frame_decimation == 0:
            batch.append(frame)
        if len(batch) == batch_size:
            futures = [executor.submit(classify_frame, frame) for frame in batch]
            predictions = [future.result() for future in futures]
            if any(contains_explicit_content(prediction) for prediction in predictions):
                video_capture.release()
                return "Explicit content found"
            batch = []
    video_capture.release()
    return "No explicit content found"