from fastapi import FastAPI

from .routers import routes


app = FastAPI()
app.include_router(routes.router)



# COGNITO_USER_CLIENT_ID=
# COGNITO_REGION_NAME=
# USER_POOL_ID=
# COGNITO_JWKS_PATH=
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
