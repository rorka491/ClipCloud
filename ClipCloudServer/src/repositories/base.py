from abc import ABC, abstractmethod


class BaseRepository:
    
    def __init__(self, redis) -> None:
        self._redis = redis 

    @abstractmethod
    async def get_all():
        ...

    @abstractmethod
    async def create():
        ...
    
    