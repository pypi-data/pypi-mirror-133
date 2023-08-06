import dta
import aiohttp.client_reqrep

async def json2attr(response):
    if isinstance(response,aiohttp.client_reqrep.ClientResponse):
        return dta.Dict2Attr(
            await response.json()
        )
    elif isinstance(response,dict):
        return dta.Dict2Attr(
            response
        )
    
    raise TypeError("Expect aiohttp.client_reqrep.ClientResponse or dict. Got {}".format(response))

async def attr2json(response):
    if isinstance(response,dta.__ConvertedDict):
        return dta.Attr2Dict(response)
    
    raise TypeError("Expect dta.__ConvertedDict. Got {}".format(response))
