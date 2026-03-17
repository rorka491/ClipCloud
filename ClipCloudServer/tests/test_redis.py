import pytest
import pytest_asyncio
from redis.asyncio import Redis

@pytest_asyncio.fixture(scope="session")
async def init_conn():
    r = Redis.from_url("redis://localhost:6379", decode_responses=True)
    yield r

    try:
        await r.aclose()
    except RuntimeError:
        pass


@pytest.mark.asyncio
async def test_redis_connect(init_conn: Redis):
    await init_conn.set("key", "value")
    val = await init_conn.get("key")
    print(val)
    assert val == "value"