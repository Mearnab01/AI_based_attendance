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
    # st.write(f"Image shape: {image_np.shape}, dtype: {image_np.dtype}")
    # print(f"[debug] faces found: {len(faces)}, image: {image_np.shape}")
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
    
    clf = None
    if (len(set(y)) >= 2):
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
    encodings = extract_face_embedding(class_image_np)

    # Bug 1 fix: guard None and empty before doing anything else
    if not encodings:
        return {}, [], 0

    detected_students = {}
    model_data = get_trained_model()

    if not model_data:
        return {}, [], len(encodings)

    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(set(y_train))

    for encoding in encodings:
        if clf is not None:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            distances = [np.linalg.norm(np.array(x) - encoding) for x in X_train]
            predicted_id = y_train[int(np.argmin(distances))]

        # Bug 2 fix: compare against ALL embeddings for that student, take the best
        student_embeddings = [
            X_train[i] for i, sid in enumerate(y_train) if sid == predicted_id
        ]
        best_match_score = min(np.linalg.norm(e - encoding) for e in student_embeddings)

        # print(f"[predict_attendance] id={predicted_id}, distance={best_match_score:.4f}")
        
        if best_match_score < 0.6:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)