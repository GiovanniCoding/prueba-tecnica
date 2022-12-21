import uvicorn
from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/jokes")
async def root():
    jokes = []
    ids = []
    while len(jokes) != 25:
        res = requests.get('https://api.chucknorris.io/jokes/random')
        data = res.json()
        if not data['id'] in ids:
            jokes.append(data['value'])
    return {"jokes": jokes}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=2345)