from fastapi import Header, HTTPException, status

from config import get_settings


def require_admin(x_admin_key: str | None = Header(default=None, alias="x-admin-key")) -> None:
    settings = get_settings()
    if not x_admin_key or x_admin_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin API key.",
        )
