from config import Settings, get_settings

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends, status
###from starlette.status import HTTP_403_FORBIDDEN

#from fastapi.security import OAuth2PasswordBearer
#from decouple import config

api_key_header = APIKeyHeader(name="api_token", auto_error=False)

##oauth2_scheme = OAuth2PasswordBearer(
##       tokenUrl="token")  # use token authentication


class ApiAuth:

    async def get_api_key(self, settings: Settings = Depends(get_settings), api_key_header: str = Security(api_key_header)):
        print("settings: " + str(settings))
        if api_key_header == settings.API_KEY:
            print(api_key_header + " is valid")
            return api_key_header
        else:
            print("Could not validate API KEY")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate API KEY"
            )


    ##def api_key_auth(self, api_key: str = Depends(oauth2_scheme)):
    ##    print("Validating API KEY: " + api_key)
    ##    if api_key != config("API_KEY"):
    ##        print("Could not validate API KEY")
    ##        raise HTTPException(
    ##            status_code=status.HTTP_401_UNAUTHORIZED,
    ##            detail="Could not validate API KEY"
    ##        )
    ##    print(api_key + " is valid, authorized")
