import re
from custom_request.request import AsyncSession
import functools
import asyncio

def normalize_url(url):
    return re.sub(r"/+$","", url)

def chunk_iterator(l, n): 
      
    # looping till length l 
    iterator = iter(l)
    for i in range(0, len(l), n):  
        yield (next(iterator) for j in range(i, min(len(l), i + n)))



def inject_async_session(func):
    '''
        decorator to manually create AsyncSession if not given
    '''
    @functools.wraps(func)
    async def wrapped(*args, session=None, **kwargs):
        need_close = session is None
        if not session:
            session = AsyncSession()
        try:
            result = await func(*args, session=session, **kwargs)
            if need_close:
                await session.close()
            return result
        except Exception as e:
            if need_close:
               await session.close()
            raise e
    return wrapped


