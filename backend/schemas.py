from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    login_input: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class OTPRequest(BaseModel):
    phone: str
    otp_code: str

class ResetPasswordRequest(BaseModel):
    phone: str
    otp_code: str
    new_password: str
