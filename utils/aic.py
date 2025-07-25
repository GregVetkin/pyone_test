# код от разработчика
import pyone
import requests
import base64
from urllib.parse import urlparse



class PyoneWrap:
    """
    Обертка для взаимодействия с OpenNebula API

    Attributes:
        auth_url (str): ip-адрес API OpenNebula. "172.16.1.30"
        auth_user (str): Имя доменного пользователя "username"
        auth_pass (str): Пароль доменного пользователя "password"

    Raises:
        requests.exceptions.RequestException: Если возникает ошибка при выполнении HTTP-запроса в методе `run_one_vm_action`.
    """
    def __init__(self, endpoint: str, username: str, password: str):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.sessionDir = ""


    def get_client(self) -> pyone.OneServer:
        """
        Пытается аутентифицироваться с использованием предоставленных учетных данных.
        Возникает ошибка аутентификации, пытается получить список токенов из сообщения об ошибке
        и создать клиент с использованием токена.

        Returns:
            pyone.OneServer: Клиент OpenNebula, если аутентификация прошла успешно, иначе None.
        """
        token = f"{self.username}~{self.password}"
        probe_client = pyone.OneServer(self.endpoint, session=token)
        token_list = []
        try:
            # любой вызов
            result = probe_client.vmpool.info()

        except pyone.OneInternalException as e:
            message = str(e)
            message = message.splitlines()
            self.sessionDir = message[1]
            token_list = message[2:]
            
        # oned вернул все токены пользователя. Находим первый валидный.
        # Если нет. 1)!kinit username auth_pass 2) У пользователя нет токена в Брест
        for token in token_list:
            _token = f"{self.username}:{token}"
            client = pyone.OneServer(self.endpoint, session=_token)
            try:
                # любой вызов
                result = client.user.info(0)
                return client
            except Exception as e:
                print(e)


    def run_one_vm_action(self):
        """
        Вызовите после vm.action.
        У one-apache2.cgi таймаут 120 сек. Если в каталоге sessionDir за это время не появится новый скрипт, вернёт 200.
        До этого момент повиснет (вызов блокирующий). Рассмотрите возможность запуска в отдельном потоке.

        Returns:
            requests.Response | None: Объект Response, если запрос был успешно отправлен и получен ответ, иначе None.
        """
        try:
            auth_string = f"{self.username}:{self.password}"
            encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Cookie": f"rack.session={self.sessionDir}"
            }
            host = urlparse(self.endpoint).hostname
            response = requests.get(f"https://{host}/brestcloud/one-apache2.cgi", headers=headers, verify=False, timeout=5)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return None



if __name__ == '__main__':
    endpoint = "10.0.70.20"
    username = "brestadm"
    password = "Qwe!2345"

    pw = PyoneWrap(endpoint, username, password)
    client = pw.get_client()
    


    res  = client.vm.action("resume", 17, pw.sessionDir)
    print(res)

    pw.run_one_vm_action()
