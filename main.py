from fastapi import FastAPI
import uvicorn
from bundle.bundle import router as bundle_router

app = FastAPI()

#route to the bundle services
app.include_router(bundle_router, prefix="/bundle")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)