import bcrypt


def hash_password(password):
    """
    Hash a password using bcrypt.
    Returns the hashed password as a string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(hashed_password, plain_password):
    """
    Verify if a plain-text password matches the hashed password.
    Returns True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
