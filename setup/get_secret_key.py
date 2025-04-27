import os
from django.core.management.utils import get_random_secret_key

def save_secret_key_to_file(secret_key, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(secret_key)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    secret_key_path = os.path.join(base_dir, 'secret key', 'key.txt')

    secret_key = get_random_secret_key()
    save_secret_key_to_file(secret_key, secret_key_path)
    print(f"Secret key generated and saved to 'secretkey/key.txt'.")