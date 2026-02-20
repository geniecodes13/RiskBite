import requests

base = 'http://localhost:8000'
email = 'ci_test@example.com'
password = 'Test123!'

def try_register():
    try:
        r = requests.post(f'{base}/auth/register', json={'email': email, 'password': password}, timeout=5)
        print('REG', r.status_code, r.text)
    except Exception as e:
        print('REG EXC', e)

def try_login():
    try:
        r = requests.post(f'{base}/auth/login', json={'email': email, 'password': password}, timeout=5)
        print('LOGIN', r.status_code, r.text)
        if r.status_code == 200:
            return r.json().get('user_id')
    except Exception as e:
        print('LOGIN EXC', e)
    return None

def try_save_health(uid):
    try:
        r = requests.post(f'{base}/health/{uid}', json={'data': {'conditions': ['peanut_allergy']}}, timeout=5)
        print('SAVE', r.status_code, r.text)
    except Exception as e:
        print('SAVE EXC', e)

def try_get_health(uid):
    try:
        r = requests.get(f'{base}/health/{uid}', timeout=5)
        print('GET', r.status_code, r.text)
    except Exception as e:
        print('GET EXC', e)

if __name__ == '__main__':
    try_register()
    uid = try_login()
    if uid:
        try_save_health(uid)
        try_get_health(uid)
    else:
        print('No user id from login')
