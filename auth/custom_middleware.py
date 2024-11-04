from functools import wraps

def is_access_jwt_blacklisted(func: callable):
    @wraps(func)
    async def  wrapper(*args, **kwargs):
        
        func()
    pass

