from time import time
from starlette.middleware.base import BaseHTTPMiddleware
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        s=time();r=await call_next(request);r.headers["X-Process-Time"]=str(time()-s);return r
