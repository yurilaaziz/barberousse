import pytest
from flask import Response as BaseResponse
from flask import json
from flask.testing import FlaskClient


class Response(BaseResponse):
    def open(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'application/json')
        kwargs.setdefault('data', {})
        kwargs['data'] = json.dumps(kwargs.get('data'))
        return super().open(*args, **kwargs)


class CustomClient(FlaskClient):
    def json(self):
        return json.loads(self.data.decode('utf-8'))


@pytest.fixture
def api_client():
    from bareberousse.api import app
    app.test_client_class = CustomClient
    app.response_class = Response
    app.testing = True
    return app.test_client()


@pytest.fixture
def controller():
    from bareberousse.controller import Controller
    return Controller(async_mode=False, _disable_recover=True,
                      _raise_error=True)


@pytest.fixture
def cwd():
    from os import getcwd
    _cwd = getcwd()
    if "tests" in _cwd:
        return _cwd + "/.."
    else:
        return _cwd
