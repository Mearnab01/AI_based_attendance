import streamlit as st
import librosa
import io
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

# Model loader
@st.cache_resource
def load_voice_model()->VoiceEncoder:
    return VoiceEncoder()

# ── Single embedding ──────────────────────────────────────────────────────────
def get_voice_embedding(audio_bytes:bytes)->list |None:
    try:
        encoder = load_voice_model()
        audio, _ = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        wav = preprocess_wav(audio)
        return encoder.embed_utterance(wav).tolist()
    except Exception as e:
        print(f"[get_voice_embedding] error: {e}")
        st.error("Voice recognition failed.")
        return None
    

# ── Speaker identification ────────────────────────────────────────────────────
def identify_speaker(
    new_embedding:list,
    candidates_dict:dict,
    threshold:float = 0.75
)-> tuple[str | None, float]:
    if not new_embedding or not candidates_dict:
        return None, 0.0
    
    best_sid = None
    best_score = -1.0
    
    
    for sid, stored_embedding in candidates_dict.items():
        if not stored_embedding:
            continue
        similarity = np.dot(new_embedding, stored_embedding)
        
        if similarity > best_score:
            best_score = similarity
            best_sid = sid

    if best_score < threshold:
        return None, 0.0

    return best_sid, best_score

# ── Bulk audio processing ─────────────────────────────────────────────────────
 
def process_bulk_audio(
    audio_bytes: bytes,
    candidates_dict: dict,
    threshold: float = 0.65
) -> dict:
 
    try:
        encoder = load_voice_model()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segments  = librosa.effects.split(audio, top_db=30)
 
        identified_results = {}
 
        for start, end in segments:
            # Skip segments shorter than 0.5 seconds
            if (end - start) < sr * 0.5:
                continue
 
            segment_audio = audio[start:end]
            wav           = preprocess_wav(segment_audio)
            embedding     = encoder.embed_utterance(wav)
 
            sid, score = identify_speaker(embedding, candidates_dict, threshold)
 
            if sid and (sid not in identified_results or score > identified_results[sid]):
                identified_results[sid] = score
 
        return identified_results
 
    except Exception as e:
        print(f"[process_bulk_audio] error: {e}")
        st.error("Bulk audio processing failed.")
        return {}
 