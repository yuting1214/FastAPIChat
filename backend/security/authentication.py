import os

def authenticate_user(username: str, password: str) -> bool:
    correct_username = username == os.getenv("USER_NAME")
    correct_password = password == os.getenv("PASSWORD")
    return correct_username and correct_password
