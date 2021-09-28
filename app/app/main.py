from app.dependency.error_handler import app
import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)