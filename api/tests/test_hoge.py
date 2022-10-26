
import pytest
from apps.app import create_app

def test_hoge():
    assert 1 == 1 

@pytest.fixture
def app():
    return create_app()

def test_landing(app):

    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQMWFEaHhQa0JaYmZhUmxqTlFlWktndXZmWm9qX3NWZWRDcUc0VTVEY0FJIn0.eyJleHAiOjE2NjY3OTEzMDksImlhdCI6MTY2Njc4NDEwOSwianRpIjoiOWJjMjY4YTAtZTQ2Yy00ZDFkLTllOTUtZjhkZDNkMWFhMTE2IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnVkZW15LWZsYXNrLXNhbXBsZS50b3A6ODQ0My9yZWFsbXMvaG9nZXBla2UiLCJhdWQiOlsiZmxhc2tzIiwiYWNjb3VudCJdLCJzdWIiOiJjYWZhYjI2My0wMWNiLTRlMDItODlhMS05ZDk2YTFhODk5NmYiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmbGFza3MiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1ob2dlcGVrZSIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSIsImNsaWVudEhvc3QiOiIxMTguMjcuMTguMjMiLCJjbGllbnRJZCI6ImZsYXNrcyIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LWZsYXNrcyIsImNsaWVudEFkZHJlc3MiOiIxMTguMjcuMTguMjMifQ.qTGgL2oFRYj1r8YlnodFtOxZhc2FP7I2R9uf3ynx9MzoybSTkmQyjGghgh0q5zL9bS9Y3eW1jYdXTlDInAd6cHWcGi0MZamh16cQu6tN6ycPm6n_wjBGmQxXtAqdRsG2M-Al78Xr-9iINinmYOwZoq7H9URnshNc6Z0_Ns-U12Fl-lDr4kmic3-zMme-9amzDArqsQdsS0eqlNkn0rSq-UzreMdKKZrH8anTwdBCYfYaYt9d9mvYQZ6EPjg-wI7Tba3DoTUa1dKwGdvnfPWRzlPsXSa-wDoU8KQq6tDuLVSCPEhmVETuLDg1FBCH2hxKQfRG6zIpBI0BailD5QFuyQ"
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
    assert body['money']['system_id'] == "9d9d33e0-bb8f-4724-99d9-807cf8b91cdb"
    # Web画面は現状認証が入っているとテストが大変なので、