import uvicorn
from fastapi.middleware.cors import CORSMiddleware 

from fastapi import FastAPI
from app.api import all_routers

app = FastAPI(title="Market place by Minzifa Travel")

for router in all_routers:
    app.include_router(router, prefix='/v1')


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis


# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)