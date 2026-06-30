def success(data=None,message="Success"): return {"success":True,"message":message,"data":data}
def error(message,status=400): return {"success":False,"status":status,"message":message}
