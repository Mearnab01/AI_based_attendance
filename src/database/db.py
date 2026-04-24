from database.config import supabase
import bcrypt

# ── Auth Helpers ─────────────────────────────────────────────────────────
def hash_pass(pwd:str)-> str:
    str_to_byte = pwd.encode()
    gen_22_char_random_salt = bcrypt.gensalt()
    
    # hashes password + salt together
    hash_all = bcrypt.hashpw(str_to_byte,gen_22_char_random_salt)
    
    byte_to_str = hash_all.decode()
    return byte_to_str

def check_pass(pwd:str, hashed:str)-> bool:
    return bcrypt.checkpw(pwd.encode(), hashed.encode())

# ── Teachers ─────────────────────────────────────────────────────────────
def check_teacher_exists(username:str)-> bool:
    res = supabase.table("teachers").select("username").eq("username", username).execute()
    
    return len(res.data) > 0

def create_teacher(username:str, password:str, name:str):
    res = supabase.table('teachers').insert({
        "username":username,
        "password":hash_pass(password),
        "name":name
    }).execute()
    return res.data

def teacher_login(username:str, password:str):
    res = supabase.table("teachers").select("*").eq("username", username).execute()
    if not res.data:
        return None
    
    teacher = res.data[0]
    return teacher if check_pass(password, teacher['password']) else None


def get_teacher_subjects(teacher_id:int):
    response = supabase.table('subjects').select(
        "*, subject_students(count), attendance_logs(timestamp)"
    ).eq("teacher_id", teacher_id).execute()
    
    subjects = response.data
    
    for sub in subjects:
        sub['total_students'] = sub.get('subject_students', [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        
        attendance = sub.get('attendance_logs', [])
        unique_session = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_session
        
        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)
        
    return subjects
        

# TODO: 2
def get_subject_class_count(subject_id:int)->int:
    pass

def get_attendance_for_teacher(teacher_id: int):
    response = supabase.table('attendance_logs').select('*, subjects!inner(*)').eq('subjects.teacher_id', teacher_id).execute()
    
    return response.data


# ── Students ─────────────────────────────────────────────────────────────
def get_all_students():
    res = supabase.table("students").select("*").execute()
    return res.data

def create_student(name:str, face_embeddings=None, voice_embeddings=None):
    res = supabase.table("students").insert({
        "name": name,
        "face_embeddings": face_embeddings,
        "voice_embeddings": voice_embeddings
    }).execute()
    
    return res.data


def get_student_subjects(student_id: int):
    response = supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data


def get_student_attendance(student_id: int):
    response = supabase.table("attendance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data

# ── Subjects ─────────────────────────────────────────────────────────────────
 
def create_subject(subject_code: str, name: str, section: str, teacher_id: int):
    res = supabase.table("subjects").insert({
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }).execute()
    return res.data

def enroll_student_to_subject(student_id: int, subject_id: int):
    res = supabase.table("subject_students").insert({
        "student_id": student_id,
        "subject_id": subject_id
    }).execute()
    return res.data
 
 
def unenroll_student_to_subject(student_id: int, subject_id: int):
    supabase.table("attendance_logs") \
        .delete() \
        .eq("student_id", student_id) \
        .eq("subject_id", subject_id) \
        .execute()
    res = (
        supabase.table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )
    return res.data

def get_subject_by_code(subject_code: str):
    res = supabase.table("subjects").select('subject_id, name').eq("subject_code", subject_code).execute()
    return res.data[0] if res.data else None

def is_student_enrolled(student_id: int, subject_id: int) -> bool:
    res = supabase.table('subject_students').select('*').eq('subject_id', subject_id).eq('student_id', student_id).execute()
    return bool(res.data)

# ── Attendance ────────────────────────────────────────────────────────────────
 
def create_attendance(logs: list):
    if not logs:
        return []
    res = supabase.table("attendance_logs").insert(logs).execute()
    return res.data