
import pytest
from apps.app import create_app

def test_hoge():
    assert 1 == 1 

token=''
@pytest.fixture
def app():
    # 本来は実行前にKeycloakからトークンを取得するのが良い
    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQMWFEaHhQa0JaYmZhUmxqTlFlWktndXZmWm9qX3NWZWRDcUc0VTVEY0FJIn0.eyJleHAiOjE2NjY4NTAyMDksImlhdCI6MTY2Njg0MzAwOSwianRpIjoiOThjMGFkZWYtZDgwNi00NDRiLWEwZGEtNWMyZmYyMWVjMGQ3IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnVkZW15LWZsYXNrLXNhbXBsZS50b3A6ODQ0My9yZWFsbXMvaG9nZXBla2UiLCJhdWQiOlsiZmxhc2tzIiwiYWNjb3VudCJdLCJzdWIiOiJjYWZhYjI2My0wMWNiLTRlMDItODlhMS05ZDk2YTFhODk5NmYiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmbGFza3MiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1ob2dlcGVrZSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMTguMjcuMTguMjMiLCJjbGllbnRJZCI6ImZsYXNrcyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWZsYXNrcyIsImNsaWVudEFkZHJlc3MiOiIxMTguMjcuMTguMjMifQ.APokWPeuOlPxgy-BIS65ec1swceo1UizMBb7jn82ocW7xbACkXiDjupPxHxL7Z-BZkYQDQ1-jNYW1YmceDEppUAp8EUT1EF2uTWKF8FS-b3EHCZav9y9ho5E-PAxwbluKTEWwnujOCa6_n4txkmnnXwahvX9l3-dD0WY5xLedOR5N8S7cW0YhkIYJ381MJdfQeoUcCxL_1YZAxB7SGIrQiyNKm6e3MesD9-_PccZH9qgU78QEYGwrCi5tAmo9-PAz1kanaoNJNLqtbLRLDjsiaKruL6aTXdLMEzhfQVToLRDRK6mmerx4MzYNoKq4ph7shqu9gdwwoPp2yamcsqfMQ"
    return create_app()

def test_landing(app):

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