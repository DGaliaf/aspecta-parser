import os


def check_directory(directory: str) -> bool:
    if os.path.exists(directory):
        return True
    else:
        print(f"[+] Директория '{directory}' не существует.")
        return False


def check_files(directory: str, files: list[str]) -> bool:
    missing_files = []
    for file in files:
        file_path = os.path.join(directory, file)
        if not os.path.exists(file_path):
            print(f"[+] Файл '{file}' не существует.")
            missing_files.append(file)

    return len(missing_files) == 0  # True, если все файлы существуют


def create_directory(directory: str) -> None:
    if not os.path.exists(directory):
        print(f"[+] Создаю директорию '{directory}'...")
        os.makedirs(directory)


def create_files(directory: str, files: list[str]) -> None:
    for file in files:
        file_path = os.path.join(directory, file)
        if not os.path.exists(file_path):
            print(f"[+] Создаю файл '{file}'...")
            with open(file_path, 'w') as f:
                f.write("")  # Создаем пустой файл
