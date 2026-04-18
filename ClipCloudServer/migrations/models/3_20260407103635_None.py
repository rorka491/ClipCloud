from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "room_code" VARCHAR(255) NOT NULL,
    "message_type" VARCHAR(5) NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "file_url" VARCHAR(6000) NOT NULL,
    "text" VARCHAR(6000) NOT NULL
);
COMMENT ON COLUMN "messages"."message_type" IS 'FILE: file\nIMAGE: image\nTEXT: text';
CREATE TABLE IF NOT EXISTS "rooms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "room_code" VARCHAR(255) NOT NULL UNIQUE,
    "expires_at" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztl+tv2jAQwP8VlE+d1FWF9aV9SxldmQpMbbZVfSgyiQGrjp06zgqq+N/ncxLyggimdQ"
    "Up35J7JHe/8+Uur4bHXUyDgx4OAjTGxufGq8GQBxdF1X7DQL6fKkAg0ZBGtpGRFqJhIAVy"
    "pJKPEA2wErk4cATxJeFMSVlIKQi5owwJG6eikJHnENuSj7GcYKEU949KTJiLp+rh8a3/ZI"
    "8Ipm4uWuLCu7XcljNfy7pMXmhDeNvQdjgNPZYa+zM54WxhTZgE6RgzLJDE8HgpQggfoosz"
    "TTKKIk1NohAzPi4eoZDKTLprMnA4A34qmkAnqKvysdU8Oj06+3RydKZMdCQLyek8Si/NPX"
    "LUBPqWMdd6JFFkoTGm3ByBIVkbyTK/L0ojiYeXQ8x7FmC6setBclFEm4CsYpsIUrjpgfpH"
    "dFUO7oDRWVy4CpRWt9e5sczed8jEC4JnqhGZVgc0LS2dFaR7Jx9AzlU7RH2yeEjjV9e6bM"
    "Bt427Q72iCPJBjod+Y2ll3BsSEQsltxl9s5GbOWCJNwCjLtLCCc09Vy8XlurYnSCyvac6p"
    "UFLFbUuL6KGpTTEbywn0xfFxRRV/mtftS/N6T1kVStOPVa1IN8/BjL9vEYulPDss9DTTro"
    "oNMQeX2Baf8c54jYvuVUdZE4ofWLdnflU3xFMBPjCrc2upQ4anurM3LcA6+FfDL6EPAyz0"
    "9QbHOOtTn+IFSqi1HQq6Ccqsz26iPDk8PFyDJZithBkp8zST/liXZGJfU4QlbvSUWUdAME"
    "TO0wsSrl3S8BZfZVtWeS2vKEFMfdXcOE/IId5sr9WwM5ZsvFpeue7CmKx33XrXrXfdetf9"
    "rw3y9jsCnvpEFeYveiTvuZs9siM9kaRdaootmawmFsSZLJutsaZyuqLUph6vOzRef2MRQE"
    "gbfIMzLru5Fr/JNxhaYwOIsfluAmyu9VvRrPiraJZ/zdQbJWZLJti3m0F/xYaXuhRA/mAq"
    "wXuXOHK/QUkgH7cTawVFyDo3tRJ4ez3ztsi1fTU4L44jeMD5e/+4zf8AsKffQA=="
)
