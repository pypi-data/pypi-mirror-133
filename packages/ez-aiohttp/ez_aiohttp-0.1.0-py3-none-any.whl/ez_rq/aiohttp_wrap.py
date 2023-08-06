import aiohttp

async def get(*args,**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(*args,**kwargs) as response:
            return response

async def post(*args,**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(*args,**kwargs) as response:
            return response

async def put(*args,**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.put(*args,**kwargs) as response:
            return response

async def patch(*args,**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.patch(*args,**kwargs) as response:
            return response

async def delete(*args,**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.delete(*args,**kwargs) as response:
            return response