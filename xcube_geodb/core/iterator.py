import math


class GeoDBIterator:
    def __init__(self, geodb, func: str,
                 page_size: int, start_page: int = 0, stop_page: int = math.inf, **kwargs):
        self._kwargs = kwargs
        self._geodb = geodb
        self._func = func
        self._page = start_page or 0
        self._start_page = start_page
        self._stop_page = stop_page
        self._page_size = page_size or 10

    @property
    def start_page(self):
        return self._start_page

    @start_page.setter
    def start_page(self, value):
        self._start_page = value

    @property
    def stop_page(self):
        return self._stop_page

    @stop_page.setter
    def stop_page(self, value):
        self._start_page = value

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value):
        self._page_size = value

    def __iter__(self):
        self._page = self._start_page
        return self

    def __next__(self):
        page = self._page

        if page > self._stop_page:
            raise StopIteration

        self._page += 1

        self._kwargs['kwargs']['offset'] = page * self._page_size
        self._kwargs['kwargs']['limit'] = self._page_size
        self._kwargs['kwargs']['iterate'] = False

        func = getattr(self._geodb, self._func)
        res = func(**self._kwargs['kwargs'])

        if len(res.index) > 0:
            return res
        else:
            raise StopIteration
