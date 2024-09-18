import uvicorn
from fastapi import FastAPI
from database.connection import Base,engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from route import user_route,product_route,order_route
from model import *


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# config routes
app.include_router(user_route.user_Router)
app.include_router(product_route.product_Router)
app.include_router(order_route.order_Router)

@app.get("/")
async def index():
   return {"message": "Hello World"}



if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)