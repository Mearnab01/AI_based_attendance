import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    
    shape_predictor = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    
    face_rec_model = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    
    return detector, shape_predictor, face_rec_model


def extract_face_embedding(image_np):
    detector, shape_predictor, face_rec_model = load_dlib_models()
    
    faces = detector(image_np, 1)
    
    if len(faces) == 0:
        return None
    
    embeddings = []
    for face in faces:
        shape = shape_predictor(image_np, face)
        face_descriptor = face_rec_model.compute_face_descriptor(image_np, shape, 1)
        embeddings.append(np.array(face_descriptor))
    
    return embeddings

@st.cache_resource
def get_trained_model():
    X = []
    y = []


    student_db = get_all_students()

    if not student_db:
        return None
    
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if len(X) ==0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError:
        pass

    return {'clf': clf, 'X':X, "y":y}