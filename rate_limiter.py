import time
import uuid
import redis.asyncio as redis
from fastapi import Request, HTTPException
from auth.auth_handler import decode_jwt

r = redis.Redis(host='redis', port=6379, decode_responses=True)
RATE_LIMITS = {
    "anonymous": (2, 60),
    "authenticated": (10, 60),
}


async def rate_limit(request: Request):
    user_id = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = decode_jwt(token)
        if payload and "user_id" in payload:
            user_id = payload["user_id"]

    identity = user_id or request.client.host
    limit_type = "authenticated" if user_id else "anonymous"
    limit, period = RATE_LIMITS[limit_type]
    key = f"rate_limit_{identity}"
    now = time.time()
    window_start = now - period

    await r.zremrangebyscore(key, min=0, max=window_start)
    request_count = await r.zcard(key)

    if request_count >= limit:
        raise HTTPException(status_code=429, detail="Too many requests")

    member = f"{now}_{uuid.uuid4()}"
    await r.zadd(key, {member: now})
    await r.expire(key, period)