from passlib.context import CryptContext
import getpass

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

if __name__ == "__main__":
    plain_password = getpass.getpass("Enter the password to hash: ")
    hashed_password = get_password_hash(plain_password)
    print("\n--- HASH GENERATED ---")
    print("Copy the entire line below:")
    print(hashed_password)
    print("----------------------\n")