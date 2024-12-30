import json
import requests
import pprint

vTest1 = {"email": "xxx@yandex.ru", "text": "avgra", "phone": "+7 986 735 12 35", "date": "08.07.1999"}
vTest2 = {"text": "abra"}
notFoundTest = {"foo": "bazz", "Phone":"+7 986 735 12 35", "eMail": "xxx@yandex.ru", "DaTe": "1999-09-23"}
invTest = {"bazz": 2, "fone":"7986 735 12 35"}

host = "http://127.0.0.1:8000/get_form"
jHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
testReqs = [vTest1, vTest2, notFoundTest, invTest]

for test in testReqs:
    js = json.dumps(test)
    resp = requests.post(url=host, data=js, headers=jHeaders)
    print(f"test: {js}")
    print(f"Response code {resp.status_code}")
    if (resp.status_code == 200):
        print(json.dumps(resp.json(), indent=4, sort_keys=True))
    else:
        print(resp.text)