from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends,  HTTPException
from typing import Optional

security = HTTPBasic()

admin_oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user data with permissions
admin_users = {
    "admin": {"password": "adminpass", "permissions": ["post", "edit", "delete", "view"]},
    "john": {"password": "john123", "permissions": ["view"]}
}


# Authenticate admin users
def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    user = admin_users.get(credentials.username)
    if user and user["password"] == credentials.password:
        return credentials.username, user["permissions"]
    raise HTTPException(
        status_code=401,
        detail="Unauthorized"
    )

# Mock function to simulate OAuth2 token validation
def mock_token_validation(token: str):
    # This function should validate the token and return the associated user
    if token == "valid_admin_token":
        return "admin"
    if token == "valid_john_token":
        return "john"
    raise HTTPException(
        status_code=401,
        detail="Invalid token"
    )

# Authorization decorator for admin with required permissions
def auth_admin_permission(required_permissions: list[str]):
    def __auth_admin_permission__(token: str = Depends(admin_oauth2_schema)):
        # Validate the token
        username = mock_token_validation(token)
        # Get the user's permissions
        user = admin_users.get(username)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized"
            )
        
        # Check for required permissions
        if not all(permission in user["permissions"] for permission in required_permissions):
            raise HTTPException(
                status_code=403,
                detail="The authenticated Admin User does not have permission to access this endpoint",
            )
        user["username"] = username
        return user
    return __auth_admin_permission__


def optional_auth_admin_permission(required_permissions: Optional[list[str]] = None):
    def __wrapper__(
        token: Optional[str] = None,
    ):
        if token is None:
            return None
        return auth_admin_permission(required_permissions)(token)
    return __wrapper__ 