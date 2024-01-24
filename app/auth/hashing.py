from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify the provided plain password against the given hashed password using the pwd_context.

        Parameters:
            plain_password (str): The plain text password to be verified.
            hashed_password (str): The hashed password to be checked against.

        Returns:
            bool: True if the plain password matches the hashed password, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """
        Returns the hash of the input password using the pwd_context.
        """
        return pwd_context.hash(password)
