from passlib.hash import bcrypt

def hash_password(raw_pass: str) -> str:
    return bcrypt.hash(raw_pass)



def verify_hash_password(raw_pass: str, hashed_password: str) -> bool:
    return bcrypt.verify(raw_pass, hashed_password)