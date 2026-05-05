from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schemas.role import RoleOut


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role_id: int
    role: RoleOut
    created_at: datetime
