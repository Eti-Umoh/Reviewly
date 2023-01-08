from fastapi import FastAPI
from .import models
from .database import engine
from .routers import authentication,review,user

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations related to everything auth",
    },
    {
        "name": "Review",
        "description": "Operations related to the the reviews left by users,reviews about music",
    },
    {
        "name": "User",
        "description": "Operations related to the user",
    },
]

app = FastAPI(
    title='Reviewly API',
    description='Review any music album of your choice on our website',
    openapi_tags=tags_metadata,
    contact={
        "Developer name":"ATM",
        "website":"https://mrmorale.pythonanywhere.com/",
        "email":"etiumoh04@gmail.com",
    },
    # docs_url='/documentation',redoc_url=None
)

app.include_router(authentication.router)
app.include_router(review.router)
app.include_router(user.router)

models.Base.metadata.create_all(engine)
