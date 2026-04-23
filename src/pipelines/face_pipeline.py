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
def get_trained_model()->dict | None:
    X = [] # embeddings of 15 students
    y = [] # corresponding student IDs


    students = get_all_students()

    if not students:
        return None
    
    for student in students:
        embedding = student.get('face_embeddings')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    if not X:
        return None
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)
    except ValueError as e:
        print(f"[get_trained_model] fit error: {e}")
        return None

    return {'clf': clf, 'X': X, 'y': y}

def train_classifier()->bool:
    st.cache_resource.clear()
    return bool(get_trained_model())


# ── Prediction ────────────────────────────────────────────────────────────────
 
def predict_attendance(class_image_np: np.ndarray) -> tuple[dict, list, int]:
    encodings = extract_face_embedding(class_image_np) or [np.zeros(128)]
    detected_studnets = {}
    model_data = get_trained_model()
    
    if not model_data:
        return detected_studnets, [], 0 
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']
    
    all_students = sorted(set(y_train))
    
    for encoding in encodings:
        # Need at least 2 classes for SVC predict — fallback to only student if one enrolled
        predicted_id = (
            int(clf.predict([encoding])[0])
            if len(all_students) >= 2
            else int(all_students[0])
        )
        
        student_embeddings = X_train[y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embeddings - encoding)
        
        if best_match_score < 0.6:  # Threshold for a valid match
            detected_studnets[predicted_id] = True
            
    return detected_studnets, all_students, len(encodings)
         
