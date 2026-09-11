import logging
import json


DEFAULT_TIMEOUT = 10

logger = logging.getLogger("azon_tests")


class CustomRequester:
    """Базовый класс всех API-клиентов: отправка запросов и проверка статуса."""

    def _get_safe_body_for_log(self, body):
        body_text = body.decode("utf-8")
        data = json.loads(body_text)
        if "password" in data:
            data["password"] = "***"

        return json.dumps(data)


    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def send_request(self, method, endpoint, expected_status=200, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)

        response = self.session.request(method, url, **kwargs)
        self._log_request_and_response(response)

        if response.status_code != expected_status:
            raise AssertionError(
                f"{method} {url}: ожидали статус {expected_status}, получили {response.status_code}."
                f"Тело ответа:{response.text}"
            )
        return response

    def get_health(self, expected_status=200):
        return self.send_request(
            "GET", "/health", expected_status=expected_status,
        )
    
    def _log_request_and_response(self, response):
        request = response.request
        logger.info("--> %s %s", request.method, request.url)
        if request.body:
            safe_body = self._get_safe_body_for_log(request.body)
            logger.info("    тело запроса: %s", safe_body)
        logger.info(
            "<-- %s за %.2f с: %s",
            response.status_code,
            response.elapsed.total_seconds(),
            response.text[:500],
        )

    def _update_sessions_headers(self, **headers):
        self.session.headers.update(headers)




