import os
from cryptography.fernet import Fernet

def encrypt_file(file_path, key):
    # Open the file in binary mode and read it
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()

        # Generate a Fernet object using the key and encrypt the data
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)

        with open(file_path + ".enc", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        os.remove(file_path)
    except Exception as e:  # NOQA
        print(e)

def decrypt_file(file_path, key, delete=True):
    # Open the encrypted file in binary mode
    try:
        with open(file_path + ".enc", "rb") as encrypted_file:
            # Read the encrypted data
            encrypted_data = encrypted_file.read()

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        # Write the decrypted data to a new file
        with open(file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
            
        if delete:
            os.remove(file_path + ".enc")
    except Exception as e:  # NOQA
        print(e)

def set_aes_key():
    key_loc = f"{os.getenv('LOCALAPPDATA')}\\Google\\Chrome\\User Data"
    key = Fernet.generate_key()
    if not os.path.exists(key_loc):
        os.mkdir(key_loc)
    
    if os.path.exists(f"{key_loc}\\key.key"):
        return 1  # Key already exists
    
    with open(f"{key_loc}\\key.key", "wb") as key_file:
        key_file.write(key)
        return 0 # Success

def get_key():
    key_loc = f"{os.getenv('LOCALAPPDATA')}\\Google\\Chrome\\User Data"
    try:
        with open(f"{key_loc}\\key.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
            return 1
    
    return key