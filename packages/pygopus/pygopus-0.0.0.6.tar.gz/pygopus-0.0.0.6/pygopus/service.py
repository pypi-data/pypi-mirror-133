from functools import cached_property, wraps
from typing import Any, Dict, Literal, Optional, List
from pydantic import BaseModel
import atexit
import httpx


def kill_go():
    import psutil

    for p in psutil.process_iter():
        if "pygobin" in p.name():
            proc = psutil.Process(p.pid)
            proc.terminate()


atexit.register(kill_go)


def auto_abort(func):
    @wraps(func)
    def instead(self, *args, **kwd):
        try:
            res = func(self, *args, **kwd)
            return res
        except httpx.ConnectError:
            raise
        except Exception as e:
            kill_go()
            raise e
        finally:
            ...

    return instead


class Service(BaseModel):
    pid: int

    class Config:
        # arbitrary_types_allowed = True
        keep_untouched = (cached_property,)

    @auto_abort
    def get(self, data: dict = {}):
        d = self.dict()
        if data:
            d.update(data)
        res = httpx.get(self.api, params=d, timeout=None)
        return res.json()

    @auto_abort
    def post(self, data: dict = {}):
        d = {**self.dict(), **data}
        res = httpx.post(self.api, json=d, timeout=None)
        return res.json()

    @cached_property
    def api(self):
        from .core import HOST, service_pool

        info = service_pool[self.pid]
        return f"{HOST}:{info.port}/{self.schema()['title']}"


class Hello(Service):
    ...


class Save(Service):
    ...


class SaveAs(Service):
    path: str


class Close(Service):
    ...


class HighLight(Service):
    sheet_name: str
    tar_type: Literal["row", "col", "cell"]
    targets: List[str]
    color: List[str] = ["#ffff00"]


class AddSheet(Service):
    sheet_name: str


class DeleteSheet(Service):
    sheet_name: str


# never use this ...
# class GetSheet(Service):
#     ...


class GetSheets(Service):
    ...


class GetRows(Service):
    sheet_name: str


class GetCols(Service):
    sheet_name: str


class DeleteCol(Service):
    sheet_name: str
    col_axis: str


class DeleteRow(Service):
    sheet_name: str
    row_axis: int


class WriteRows(Service):
    sheet_name: str
    rows: Dict


class GetCell(Service):
    sheet_name: str
    axis: str


class SetCell(Service):
    sheet_name: str
    axis: str
    val: Any


class TotalCols(Service):
    sheet_name: str


class SearchCell(Service):

    val: str
    regex: Optional[str] = None
