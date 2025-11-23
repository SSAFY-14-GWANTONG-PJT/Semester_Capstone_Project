from fastapi import FastAPI

app = FastAPI(root_path="/ai")

@app.get("/")
def read_root():
    return {"message": "Hello from AI Server!"}