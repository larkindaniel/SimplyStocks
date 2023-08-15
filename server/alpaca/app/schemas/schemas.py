from pydantic import BaseModel

# For use with Cognito
class User(BaseModel):
    email: str
    password: str
