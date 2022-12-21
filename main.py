import uvicorn
from fastapi import FastAPI

import aiohttp
import asyncio

app = FastAPI()

async def peticion(url, client):
    async with client.get(url) as r:
        res = await r.json()
        return res

async def peticiones(urls):
    async with aiohttp.ClientSession() as client:
        responses = await asyncio.gather(*[peticion(url, client) for url in urls])
        return responses

@app.get("/jokes")
def root():
    async_data = asyncio.run(peticiones(['https://api.chucknorris.io/jokes/random']*25))
    jokes = [joke['value'] for joke in async_data]
    ids = [joke['id'] for joke in async_data]
    
    while len(jokes) != 25:
        res = requests.get('https://api.chucknorris.io/jokes/random')
        data = res.json()
        if not data['id'] in ids:
            jokes.append(data['value'])
    return {"jokes": jokes}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=2345)
