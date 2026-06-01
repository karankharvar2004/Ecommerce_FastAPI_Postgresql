from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class PasswordHelper:

    @classmethod
    def hash_password(cls, password: str):

        return pwd_context.hash(password)

    @classmethod
    def verify_password(
        cls,
        plain_password: str,
        hashed_password: str
    ):

        return pwd_context.verify(
            plain_password,
            hashed_password
        )