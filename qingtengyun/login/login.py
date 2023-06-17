def login(func):
    def inner(*args,**kwargs):
        #通过selenium模拟登陆获取token
        kwargs['auth'] = {"token": getToken()}
        func(*args,**kwargs)
    return inner

@login
def get_order():
    data = {"orderid":"123"}
    requests.post(url=BASE_URL+"/order",json=data,header= )


def login():
    #通过selenium模拟登陆获取token
    return {"Authorization":token}

def get_order():
    data = {"orderid":"123"}
    requests.post(url=BASE_URL+"/order",json=data,header=login() )
