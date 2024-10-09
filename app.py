from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from urllib.parse import urlparse
from main import *
import re
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Custom exception handler for general exceptions
@app.exception_handler(Exception)
def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )



def verify_url(url: str):
    parsed_url = urlparse(url)
    if not(parsed_url.scheme and parsed_url.netloc):
        raise HTTPException(status_code=400, detail="Invalid URL")
    youtube_regex = (
        r'(https?://)?'
        r'(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?'
        r'([^&=%\?]{11})'
    )
    
    youtube_pattern = re.compile(youtube_regex)
    match = youtube_pattern.match(url)

    if not match: raise HTTPException(status_code=400, detail="Invalid Youtube URL")
    return url


@app.get("/video_info", dependencies=[Depends(verify_url)])
def video_info(url: str):
    return get_video_info(url)

@app.get("/audio", dependencies=[Depends(verify_url)])
def audio(url: str):
    download_audio(url)
    return {"msg": "done"}

@app.get("/video", dependencies=[Depends(verify_url)])
def video(url: str, resolution: int):
    download_video(url, resolution)
    return {"msg": "sone"}

# time format = '00:02:00'
@app.get("/video_section", dependencies=[Depends(verify_url)])
def video_section(url: str, start_time, end_time):
    download_video_with_section(url, start_time, end_time)
    return {"msg": "done"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)