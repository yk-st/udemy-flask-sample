
import pytest
from apps.app import create_app

def test_hoge():
    assert 1 == 1 

@pytest.fixture
def app():
    return create_app()

def test_landing(app):

    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQMWFEaHhQa0JaYmZhUmxqTlFlWktndXZmWm9qX3NWZWRDcUc0VTVEY0FJIn0.eyJleHAiOjE2NjY3ODEyMzEsImlhdCI6MTY2Njc3NDAzMSwianRpIjoiZjYwODhhOGMtMmU1OS00MzBkLWI2MTctNjZmYWFjNGVjNGUxIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnVkZW15LWZsYXNrLXNhbXBsZS50b3A6ODQ0My9yZWFsbXMvaG9nZXBla2UiLCJhdWQiOlsiZmxhc2tzIiwiYWNjb3VudCJdLCJzdWIiOiJjYWZhYjI2My0wMWNiLTRlMDItODlhMS05ZDk2YTFhODk5NmYiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmbGFza3MiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1ob2dlcGVrZSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMTguMjcuMTguMjMiLCJjbGllbnRJZCI6ImZsYXNrcyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWZsYXNrcyIsImNsaWVudEFkZHJlc3MiOiIxMTguMjcuMTguMjMifQ.PJncuogsUvSNpzCKMUyiyZjBi4XhxgT68l834Ypt3l-d9KGzaMHMs3gEs2ZcghPtWGhfBUbNSGq7SQgz1rfGoZQFxlFxcIMmKqC2N_4EyHUrMglovQV0UvT2OYYtlYEVxo-zVN97L4tgFiEyaLxNkNrqhx8-1YobBv-NoMir0LO6jNjVkSGKrybtx5X8RHqULpKG73O_9ZSOI92QM5HagXhpwMUAfh2GKReFr5nGC6lxHlg48gsXK_Utp9XixOjpDSScWl8yWUcJIBu5EyNLzrd8a_l4vZw-D6UiGId-yr0yIRoPaDLcgljeol58iO4HeZSCdhKBvC9VE5MXgJMVQA"

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
    assert body['system_id'] == "9d9d33e0-bb8f-4724-99d9-807cf8b91cdb"
    # Web画面は現状認証が入っているとテストが大変なので、