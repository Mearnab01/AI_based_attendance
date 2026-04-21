import os

# Define your project structure
structure = {
    "src": {
        "components": [
            "dialog_add_photo.py",
            "dialog_attendance_results.py",
            "dialog_auto_enroll.py",
            "dialog_create_subject.py",
            "dialog_enroll.py",
            "dialog_share_subject.py",
            "dialog_voice_attendance.py",
            "footer.py",
            "header.py",
            "subject_card.py",
        ],
        "database": [
            "config.py",
            "db.py",
        ],
        "pipelines": [
            "face_pipeline.py",
            "voice_pipeline.py",
        ],
        "screens": [
            "home_screen.py",
            "student_screen.py",
            "teacher_screen.py",
        ],
        "ui": [
            "base_layout.py",
        ],"utils": [  
            "logger.py",
        ],
    },
    "root_files": [
        "app.py",
        "requirements.txt",
        "README.md",
    ],
}
def create_file(path, content=""):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)
        print(f"Created file: {path}")


def create_init_file(folder_path):
    init_path = os.path.join(folder_path, "__init__.py")
    create_file(init_path, "# Package init\n")

def create_structure(base_path=".", structure=structure):
    for folder, content in structure.items():
        if folder == "root_files":
            # Create root-level files
            for file in content:
                file_path = os.path.join(base_path, file)
                create_file(file_path)
        else:
            folder_path = os.path.join(base_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            create_init_file(folder_path)
            print(f"Created folder: {folder_path}")

            for subfolder, files in content.items():
                subfolder_path = os.path.join(folder_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)
                create_init_file(subfolder_path)
                print(f"Created folder: {subfolder_path}")

                for file in files:
                    file_path = os.path.join(subfolder_path, file)
                    create_file(file_path)


if __name__ == "__main__":
    create_structure()
    print("Project structure created successfully!")