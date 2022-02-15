from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Token Schema"""
    # pylint: disable=too-few-public-methods
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """TokenData Schema"""
    # pylint: disable=too-few-public-methods
    login: Optional[str] = None
