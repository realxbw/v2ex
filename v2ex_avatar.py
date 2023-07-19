import sys
import json
from urllib import request
from urllib import error
from hashlib import md5

# Please configure it yourself
PROXIES = {
    'https': ''
}


# get v2ex registered user count
def get_user_count():
    try:
        opener = request.build_opener(request.ProxyHandler(PROXIES))
        resp = opener.open('https://www.v2ex.com/api/site/stats.json')
    except error.URLError as e:
        print(e.reason)
        return -1

    data = resp.read()
    jrel = json.loads(data)
    return jrel['member_max']


# get avatar
def get_user_avatar(user_id):
    md5_val = md5(str(user_id).encode(encoding='UTF-8')).hexdigest()
    jpgurl = 'https://cdn.v2ex.com/avatar/' \
             + md5_val[0:4] + '/' \
             + md5_val[4:8] + '/' \
             + str(user_id) + '_large.png'

    localjpg = str(user_id) + '.png'

    try:
        opener = request.build_opener(request.ProxyHandler(PROXIES))
        resp = opener.open(jpgurl)
    except error.URLError as e:
        print(jpgurl, '[', e.reason, '] => ', localjpg)
        return jpgurl

    data = resp.read()
    with open(localjpg, 'wb') as code:
        code.write(data)

    print(jpgurl, ' => ', localjpg)
    return jpgurl


if __name__ == '__main__':
    v2ex_user_count = get_user_count()
    if -1 == v2ex_user_count:
        print('get v2ex user count error.')
        sys.exit(-1)

    print('total registered user number of v2ex is :', v2ex_user_count)

    for i in range(1, v2ex_user_count + 1):
        get_user_avatar(i)
