from utils import schema_utils, response_utils
from allure_commons.types import AttachmentType, Severity
from requests import sessions
from curlify import to_curl
import allure
import json
import pytest


def reqres_api(method, url, **kwargs):
    args = kwargs
    base_url = "https://reqres.in"
    new_url = base_url + url
    method = method.upper()

    with allure.step(f'Отправляем запрос {method} {url} {args if len(args) != 0 else ""} '):
        with sessions.Session() as session:
            response = session.request(method=method,
                                       url=new_url, **kwargs)
            message = to_curl(response.request)
            allure.attach(body=message.encode("utf8"),
                          name="Curl",
                          attachment_type=AttachmentType.TEXT,
                          extension='txt')
            allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"),
                          name="Response Json",
                          attachment_type=AttachmentType.JSON,
                          extension='json')

    return response


def get_total_users():
    response = reqres_api('get', '/api/users/?page=2')
    total_users = response.json()['total']
    return total_users


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем, что приходит 200 код при отправке GET /api/users/2")
@pytest.mark.api
def test_ok_status_code():
    response = reqres_api('get', '/api/users/2')
    response_utils.check_status_code(200, response.status_code)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем, что приходит список юзеров с пятой страницы")
@pytest.mark.api
def test_get_users():
    schema = schema_utils.load_schema('get_users.json')

    response = reqres_api('get', '/api/users?page=5')

    response_utils.check_status_code(200, response.status_code)
    response_utils.validate_response_json(schema, response)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем получение информации о юзере №3")
@pytest.mark.api
def test_get_user():
    schema = schema_utils.load_schema('get_single_user.json')

    response = reqres_api('get', '/api/users/3')

    response_utils.check_status_code(200, response.status_code)
    response_utils.validate_response_json(schema, response)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем, что падает ошибка при попытке получить информацию о юзерах на несуществующей странице")
@pytest.mark.api
def test_get_user_not_found():
    total_users = int(get_total_users())
    more_than_expected_users_amount = total_users + 100

    response = reqres_api('get', f'/api/users/{more_than_expected_users_amount}')

    response_utils.check_status_code(404, response.status_code)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем возможность создания нового пользователя")
@pytest.mark.api
def test_create_user():
    schema = schema_utils.load_schema('create_user.json')

    response = reqres_api(
        'post',
        '/api/users',
        json={
            "name": "Theodor",
            "job": "Tester"
        }
    )

    response_utils.check_status_code(201, response.status_code)
    response_utils.validate_response_json(schema, response)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем возможность изменить информацию о юзере №13")
@pytest.mark.api
def test_put_user():
    schema = schema_utils.load_schema('put_user.json')
    name = "Naegleria fowleri"
    job = "brain-eating amoeba"

    response = reqres_api(
        'put',
        '/api/users/13',
        json={
            "name": name,
            "job": job
        }
    )

    response_utils.check_status_code(200, response.status_code)
    response_utils.validate_response_json(schema, response)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем успешность логина")
@pytest.mark.api
def test_post_successful_login():
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    schema = schema_utils.load_schema('post_success_login.json')

    response = reqres_api(
        'post',
        '/api/login',
        json={
            "email": email,
            "password": password
        }
    )

    response_utils.check_status_code(200, response.status_code)
    response_utils.validate_response_json(schema, response)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем, что падает ошибка 'Missing password' при попытке логина без пароля")
@pytest.mark.api
def test_post_unsuccessful_login():
    email = "dieter@bohlen.de"

    response = reqres_api(
        'post',
        '/api/login',
        json={
            "email": email
        }
    )

    response_utils.check_status_code(400, response.status_code)
    with allure.step('Проверяем, что пришла ошибка "Missing password"'):
        assert response.json()['error'] == 'Missing password'


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем успешную регистрацию")
@pytest.mark.api
def test_post_successful_registration():
    email = "eve.holt@reqres.in"
    password = "pistol"
    schema = schema_utils.load_schema('post_register_user.json')

    response = reqres_api(
        'post',
        '/api/register',
        json={
            "email": email,
            "password": password
        }
    )

    response_utils.check_status_code(200, response.status_code)
    response_utils.validate_response_json(schema, response)


@allure.tag("api")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "Zosimov")
@allure.epic("Api тесты")
@allure.feature("Reqres api")
@allure.story("Проверяем, что падает ошибка 'Missing password' при попытке регистрации без пароля")
@pytest.mark.api
def test_post_unsuccessful_registration():
    email = "sydney@fife"

    response = reqres_api(
        'post',
        '/api/register',
        json={
            "email": email
        }
    )

    response_utils.check_status_code(400, response.status_code)
    with allure.step('Проверяем, что пришла ошибка "Missing password"'):
        assert response.json()['error'] == "Missing password"