
import pytest
from apps.app import create_app

def test_hoge():
    assert 1 == 1 

@pytest.fixture
def app():
    return create_app()

def test_dbs(app):
    
    # 本来は実行前にKeycloakからトークンを取得するのが良い
    token="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQMWFEaHhQa0JaYmZhUmxqTlFlWktndXZmWm9qX3NWZWRDcUc0VTVEY0FJIn0.eyJleHAiOjE2NjY4NTI4NTMsImlhdCI6MTY2Njg0NTY1MywianRpIjoiNWFhM2M1MjgtYTBiMy00NzQ3LThkYzgtNjhmNDVjMTliZGE4IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnVkZW15LWZsYXNrLXNhbXBsZS50b3A6ODQ0My9yZWFsbXMvaG9nZXBla2UiLCJhdWQiOlsiZmxhc2tzIiwiYWNjb3VudCJdLCJzdWIiOiJjYWZhYjI2My0wMWNiLTRlMDItODlhMS05ZDk2YTFhODk5NmYiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmbGFza3MiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1ob2dlcGVrZSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMTguMjcuMTguMjMiLCJjbGllbnRJZCI6ImZsYXNrcyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWZsYXNrcyIsImNsaWVudEFkZHJlc3MiOiIxMTguMjcuMTguMjMifQ.KYfLLlEG3glepFh6_68gNuAxgBPTDV4Rhjr8wazPG2UNhxyqJYCsFJcphK3M9OpB7W_ria1q8V0OMsW86FzPVcjnRXHRwOT4bfHbxNcqRMnBWnwj0iIBG6SS2GnG-1HH02gOgliVj6fcW2Vj6ivDAqLNt8pwqhj0mhvRbsdCAydqun9wj6vHN1xhzFyMshzqnBkMFVMQY10Zs6YfDWG_nrdgKuJDHZPbRV8ZONflYlCsj_7shJTVMFY6ozSCU81-LY1b2m7cekolQsL-p6bh5fFT35fQtZWZlgAkwK0-WthRKL1udrjUi-0suYq6cTu5joyZEwIDZ73ZGyXECoDe_g"
    
    app.config['TESTING'] = True
    # getの場合
    response = app.test_client().get('/api/v1/dbs', headers={'X-Access-Token': token})
    # postの場合
    # app.test_client().post('/dashboard', 
    # data=dict(hoge='1111', peke='2222'),
    # headers={'content-md5': 'some hash'})
    print(response.data)
    app.logger.debug(response.data)
    body = response.get_json()
    print(body)

    # ひとまずsystem_idのみテストを行う
    assert body['money']['system_id'] == "9d9d33e0-bb8f-4724-99d9-807cf8b91cdb"
    # Web画面は現状認証が入っているとテストが大変なので、認証を外した状態でテストすると良いです。