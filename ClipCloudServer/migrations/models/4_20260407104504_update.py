from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "messages" ALTER COLUMN "file_url" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "messages" ALTER COLUMN "file_url" SET NOT NULL;"""


MODELS_STATE = (
    "eJztl21v2jAQgP8KyqdO6qrC+qZ9Szu6MhWYaLZVfVFkEgNWHTt1nBVU8d/ncxLyBhFU7Q"
    "CJb8nd2bl7zue7vBoedzENDto4CNAQG19rrwZDHjwUVfs1A/l+qgCBRH0a2UZGWoj6gRTI"
    "kUo+QDTASuTiwBHEl4QzJWUhpSDkjjIkbJiKQkaeQ2xLPsRyhIVS3D8qMWEuHqvN41f/yR"
    "4QTN2ct8SFb2u5LSe+lrWYvNSG8LW+7XAaeiw19idyxNnMmjAJ0iFmWCCJYXspQnAfvIsj"
    "TSKKPE1NIhcza1w8QCGVmXCXZOBwBvyUN4EOUGflc6N+dHp09uXk6EyZaE9mktNpFF4ae7"
    "RQE+hYxlTrkUSRhcaYcnMEhmBtJMv8vimNJB6eDzG/sgDTjZceJA9FtAnIKraJIIWbHqh3"
    "oqticLuMTuLEVaC0Wu3mjWW2f0IkXhA8U43ItJqgaWjppCDdO/kEcq7KIaqT2Sa1Py3rqg"
    "avtbtup6kJ8kAOhf5iamfdGeATCiW3GX+xkZs5Y4k0AaMs08QKzj2VLReX83oxQmJ+TnOL"
    "CilV3DY0iR4a2xSzoRxBXRwfV2Txt9m7uDJ7e8qqkJpOrGpEumkOZny/RSzm8myy0NNMW8"
    "o3xBxcYlvcY814jcvWdVNZE4ofWKttflcvxFMOPjCreWupQ4bHurJXTcAy+BfDL6EPAyz0"
    "8wrHOLtmd4pnKCHXdijoKiiza96EMr6r1kby5PDwcAmUYLaQZaTMw0zKY1mQif12nsf3pA"
    "gz3OApM42AoI+cpxckXLuk4Q2+yLas8hpeUYKYutTcOE6IIR5se6rXGXMGXi2vnHahS+5G"
    "3d2ouxt1d6Pufy2Qjx8R8NgnKjFvqJH8yu2skS2piSTsUlFsSGc1sSDOaF5vjTWV3RWlNr"
    "v2ukXt9S8WAbi0wh2cWbKdY/GH3MFQGitAjM23E2B9qd+KesVfRb38a6a+KDGb08F+3HQ7"
    "Cya8dEkB5C+mArx3iSP3a5QE8nEzsVZQhKhzXSuBt9c2b4tcL66758V2BBucr/vHbfoPOq"
    "ze9Q=="
)
