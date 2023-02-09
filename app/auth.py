
from config import Settings, get_settings

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = APIKeyHeader(name="access_token", auto_error=False)


async def get_api_key(settings: Settings = Depends(get_settings), api_key_header: str = Security(api_key_header)):
    print(settings)
    if api_key_header == settings.API_KEY:
        print(api_key_header + " is valid")
        return api_key_header
    else:
        print("Could not validate API KEY")
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )