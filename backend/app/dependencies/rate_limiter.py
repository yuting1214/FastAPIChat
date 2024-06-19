from fastapi import Depends, HTTPException, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import aioredis

async def init_rate_limiter():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)

def get_rate_limiter():
    return RateLimiter(times=5, seconds=60)  # 5 requests per minute

async def check_ip_rate_limit(request: Request, limiter: RateLimiter = Depends(get_rate_limiter)):
    ip = request.client.host
    try:
        await limiter(request)
    except Exception as e:
        raise HTTPException(status_code=429, detail=f"Rate limit exceeded for IP: {ip}")
