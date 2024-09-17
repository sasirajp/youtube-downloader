from fastapi import FastAPI
import uvicorn
from main import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/audio")
def audio():
    url = 'https://www.youtube.com/watch?v=YmQJlortf14'
    download_audio(url)
    return {"Hello": "World"}

@app.get("/video")
def video():
    url = 'https://www.youtube.com/watch?v=YmQJlortf14'
    download_video(url)
    return {"Hello": "World"}

@app.get("/video_section")
def video_section():
    url = 'https://www.youtube.com/watch?v=YmQJlortf14'
    download_video_with_section(url, '00:02:00', '00:02:30')
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)