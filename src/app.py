from fastapi import FastAPI



app: FastAPI = FastAPI()


# endpoints are defined here

@app.get('/')
def index():
    return {
        "message" : "Hello, World!"
    }


# EOSC