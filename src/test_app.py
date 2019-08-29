import pytest
from flask import url_for


def allowed(response):
    return response.status_code == 200 and response.json["response"]["allowed"] == True


def valid(response):
    return {"uid", "allowed"} <= response.json["response"].keys()


class TestHeathcheck(object):
    def test_healthcheck(self, client):
        assert client.get(url_for("health")).status_code == 204


class TestValidate(object):
    @pytest.fixture
    def url(self):
        return url_for("validate")

    def test_invalid_http_method(self, client, url):
        assert client.get(url).status_code == 405

    def test_validate_with_no_data(self, client, url):
        data = {"request": {"uid": 1, "object": {}}}
        response = client.post(url, json=data)
        assert response.content_type == "application/json"
        assert allowed(response)
        assert valid(response)

    def test_validate_with_no_containers(self, client, url):
        data = {"request": {"uid": 1, "object": {"spec": {"containers": []}}}}
        response = client.post(url, json=data)
        assert allowed(response)
        assert valid(response)

    def test_validate_with_containers_with_env(self, client, url):
        data = {
            "request": {
                "uid": 1,
                "object": {
                    "spec": {
                        "containers": [{"env": {"name": "name", "value": "value"}}]
                    }
                },
            }
        }
        response = client.post(url, json=data)
        assert valid(response)
        assert not allowed(response)

    def test_validate_with_containers_without_env(self, client, url):
        data = {
            "request": {
                "uid": 1,
                "object": {"spec": {"containers": [{"image": "nginx"}]}},
            }
        }
        response = client.post(url, json=data)
        assert valid(response)
        assert allowed(response)


class TestMutate(object):
    @pytest.fixture
    def url(self):
        return url_for("mutate")

    def test_invalid_http_method(self, client, url):
        assert client.get(url).status_code == 405

    def test_mutate_with_no_data(self, client, url):
        data = {"request": {"uid": 1, "object": {}}}
        response = client.post(url, json=data)
        assert response.content_type == "application/json"
        assert valid(response)

    def test_mutate_with_data(self, client, url):
        data = {"request": {"uid": 1, "object": {"metadata": {"labels": {}}}}}
        response = client.post(url, json=data)
        assert valid(response)
        assert response.json["response"]["patch"]
