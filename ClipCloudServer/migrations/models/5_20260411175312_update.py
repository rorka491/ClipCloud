from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "messages" ADD "room_id" INT NOT NULL;
        ALTER TABLE "messages" DROP COLUMN "room_code";
        ALTER TABLE "messages" ADD CONSTRAINT "fk_messages_rooms_d64487d2" FOREIGN KEY ("room_id") REFERENCES "rooms" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "messages" DROP CONSTRAINT IF EXISTS "fk_messages_rooms_d64487d2";
        ALTER TABLE "messages" ADD "room_code" VARCHAR(255) NOT NULL;
        ALTER TABLE "messages" DROP COLUMN "room_id";"""


MODELS_STATE = (
    "eJztmFtv2jAUgP8KylMndVNhvWlvKYWVtcBEs63qRZFJDFh1bGo7K6jiv892EnKFhaq0IP"
    "GWnIvj8x0ffA4vhkddiPmXNuQcDKHxrfJiEOCph6xqv2KA8ThWKIEAfRzYBkZaCPpcMOAI"
    "KR8AzKEUuZA7DI0FokRKiY+xElJHGiIyjEU+QU8+tAUdQjGCTCruHqQYERdO5OLh6/jRHi"
    "CI3dRukau+reW2mI61rEVEUxuqr/Vth2LfI7HxeCpGlMytERFKOoQEMiCgWl4wX21f7S6M"
    "NIoo2GlsEmwx4ePCAfCxSIRbkoFDieInd8N1gDorn2vVw5PD06/Hh6fSRO9kLjmZBeHFsQ"
    "eOmkDHMmZaDwQILDTGmJvDoArWBiLP71xqBPJgMcS0ZwamG7p+iR6yaCOQy9hGghhufKDe"
    "iK6Mwe0SPA0TtwSl1Wo3ri2z/VNF4nH+hDUi02ooTU1Lpxnp3vEnJaeyHII6mS9S+dOyLi"
    "rqtXLb7TQ0QcrFkOkvxnbWraH2BHxBbUKfbeAmzlgkjcBIy0T5BiUZZCSX2voIsAbxPZ3a"
    "lmQCiANzKc6ukUmyJPmuaTWarauGtEYY3pNW2/wuX5AnN3hPrMaNJbnAiT6MJRLvgYmNIR"
    "mKkXw9WpL332avfmH29o4yqeyEiprSzFLofQ6Zfi7EXlxNSZ8Pxly+elIQa0dlMEqrhSC1"
    "Lo1S5dr2GV4FZdLnVSjD8vowkscHBwclUCqzhSwDZRpmVB5lQUb223ke10WRUerZK7UbCY"
    "//9xwbgvIN2g7Vqw0eC7sORSQPsEkZRENyCae5aynDLexNe+Eym8dvFp2BSBr/rDDwPO9f"
    "k0dDhieDgiIoSvO6bp43DA2xD5zHZ8BcO0VTaWiNZiRz27zKq3lZCSDy9nTDKNSek2ALho"
    "EI+OJJQAW0GwN2Y8BuDNiMMUD/wDiyTle5+FNOb3P7r71A1t+LwskYycS8okbSnttZI1tS"
    "E1HYuaLIdSOLb9bcEM15PuNnoWvzsgcx0DQX9imJ/9A2NrG5VmW2zgbDhAw5o6IWI9QsbT"
    "JAbLPrMraoy/gLGQ8LpexVlHDZzjF0LVeRKo0VIIbm2wmwWmqMry6Z4qv5IV5+UUBScJH/"
    "uO52FjS6sUsG5C8iA7xzkSP2Kxhx8bCZWJdQVFGnLu8I3l7bvMlyrV91z7K3slrgrGjmf8"
    "/5dfYPQFeVuQ=="
)
