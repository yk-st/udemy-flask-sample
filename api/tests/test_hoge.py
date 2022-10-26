
import pytest
from apps.app import create_app

def test_hoge():
    assert 1 == 1 

@pytest.fixture
def app():
    return create_app()

def test_landing(app):

    app.config['TESTING'] = True
    # getの場合
    response = app.test_client().get('/')
    # postの場合
    # app.test_client().post('/dashboard', 
    # data=dict(hoge='1111', peke='2222'),
    # headers={'content-md5': 'some hash'})
    print(response.data)
    app.logger.debug(response.data)
    assert b'landing' == response.data
    # 本番環境は＿認証が入っているのでエラーとなる