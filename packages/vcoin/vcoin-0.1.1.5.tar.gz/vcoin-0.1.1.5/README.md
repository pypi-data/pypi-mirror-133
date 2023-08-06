=====
django-vcoin
=====

django-vcoin project is coin application for hehuoya.com

virtual coin for app

Quick start

# 安装到特定目录下
pip3 install hhycommon --target='~/Library/Python/3.8/site-packages/'

-----------

1. Add "vcoin" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'vcoin',
    ],
2. 配置aes密钥，默认为
   AES_KEY : "A0UrOf/XVPjdPIKG"

4. Include the class in your project views.py like this::
from vcoin.Checker import HHYAES
from vcoin.views import VCoinManager
    
and then pass  your user token for vcoin

aes_encrypt_data = HHYAES.aes_encrypt(utoken.decode(encoding='utf-8'))
utoken = base64.b64encode(aes_encrypt_data.encode('utf-8'))
VCoinManager.freezeCoin(utoken, 50, 1)

3. Run `python3 manage.py makemigrations vcoin` to create the vcoin models.
4. Run `python3 manage.py migrate` to create the vcoin models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a models if needed (you'll need the Admin app enabled).


demo:

```python
from vcoin.Checker import HHYAES
from vcoin.views import VCoinManager

def index(request):
    current_milli_time = int(round(time.time() * 1000))
    utoken = ('RVAMY>' + str(current_milli_time)).encode("utf-8")
    aes_encrypt_data = HHYAES.aes_encrypt(utoken.decode(encoding='utf-8'))
    utoken = base64.b64encode(aes_encrypt_data.encode('utf-8'))
    # 对base64的tokenAES加密
    VCoinManager.provideCoin(user_token=utoken, coin_count=10, coin_type=1)
    return HttpResponse(utoken)

```

