from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.verify("admin", "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaijsWGUxOaT3pS9pWtGXmhIO"))
print(pwd_context.verify("123456", "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMaijsWGUxOaT3pS9pWtGXmhIO"))
