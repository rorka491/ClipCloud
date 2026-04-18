from abc import ABC, abstractmethod


class BaseRepository:
    @abstractmethod
    async def get_all():
        ...

    @abstractmethod
    async def create():
        ...
    
    
