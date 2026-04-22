from database.db import (
    create_teacher, 
    check_teacher_exists, 
    teacher_login
    )
from utils.logger import get_logger
logger = get_logger(__name__)


def _register_teacher(
    teacher_name: str,
    teacher_username: str,
    teacher_pass: str,
    teacher_conf_pass: str
):
    if not teacher_name or not teacher_username or not teacher_pass or not teacher_conf_pass:
        return False, "All fields are required."
    
    if teacher_pass != teacher_conf_pass:
        return False, "Passwords do not match."
    
    if check_teacher_exists(teacher_username):
        logger.warning(f"Registration failed: Username '{teacher_username}' already exists")
        return False, "Username already exists."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)  
        logger.info(f"Teacher registered successfully: {teacher_username}")
        return True, "Teacher registered successfully."
    
    except Exception as e:
        logger.error(f"Error registering teacher '{teacher_username}': {str(e)}", exc_info=True)
        return False, "An error occurred while registering the teacher!"

def _login_teacher(teacher_username:str, teacher_password:str):
    if not teacher_username or not teacher_password:
        return False, "Username and password are required."
    
    try:
        teacher = teacher_login(teacher_username, teacher_password)

        if not teacher:
            logger.warning(f"Login failed for username: {teacher_username}")
            return False, "Invalid username or password."
        
        logger.info(f"Login success: {teacher_username}")
        return True, teacher

    except Exception as e:
        logger.error(f"Login error for {teacher_username}: {str(e)}", exc_info=True)
        return False, "Something went wrong during login."
    

# public function
def register_teacher_service(
    teacher_name: str,
    teacher_username: str,
    teacher_pass: str,
    teacher_conf_pass: str
):
    return _register_teacher(
        teacher_name,
        teacher_username,
        teacher_pass,
        teacher_conf_pass
    )
    
def login_teacher_service(
    teacher_username: str,
    teacher_password: str
    ):
    return _login_teacher(
    teacher_username,
    teacher_password
    )