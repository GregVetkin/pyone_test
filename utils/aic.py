# код от разработчика
import pyone
import requests
import base64



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
    def __init__(self, ip: str, auth_user: str, auth_pass: str):
        self.ip = ip
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.sessionDir = ""


    def get_client(self) -> pyone.OneServer:
        """
        Пытается аутентифицироваться с использованием предоставленных учетных данных.
        Возникает ошибка аутентификации, пытается получить список токенов из сообщения об ошибке
        и создать клиент с использованием токена.

        Returns:
            pyone.OneServer: Клиент OpenNebula, если аутентификация прошла успешно, иначе None.
        """
        token = f"{self.auth_user}~{self.auth_pass}"
        probe_client = pyone.OneServer(f"http://{self.ip}:2633/RPC2", session=token)
        token_list = []
        try:
            # любой вызов
            result = probe_client.vmpool.info()

        except pyone.OneInternalException as e:
            message = str(e)
            print("Message:", message)
            message = message.splitlines()
            print(message)
            self.sessionDir = message[1]
            
            token_list = message[2:]
        # oned вернул все токены пользователя. Находим первый валидный.
        # Если нет. 1)!kinit auth_user auth_pass 2) У пользователя нет токена в Брест
        for token in token_list:
            _token = f"{self.auth_user}:{token}"
            client = pyone.OneServer(f"http://{self.ip}:2633/RPC2", session=_token)
            try:
                # любой вызов
                print("start")
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
            auth_string = f"{self.auth_user}:{self.auth_pass}"
            encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
            headers = {
                "Authorization": f"Basic {encoded_auth}",
                "Cookie": f"rack.session={self.sessionDir}"
            }
            response = requests.get(f"https://{self.ip}/brestcloud/one-apache2.cgi", headers=headers, verify=False)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
            return None



if __name__ == '__main__':
    ip = "10.0.70.20"
    auth_user = "brestadm"
    auth_pass = "Qwe!2345"

    pw = PyoneWrap(ip, auth_user, auth_pass)
    client = pw.get_client()
    


    res  = client.vm.action("resume", 17, pw.sessionDir)
    print(res)

    pw.run_one_vm_action()
