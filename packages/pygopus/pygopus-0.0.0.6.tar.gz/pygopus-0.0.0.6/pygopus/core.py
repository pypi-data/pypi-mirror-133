from dataclasses import dataclass
from collections import UserList
from typing import Any, List
from random import randint
from .service import *
from path import Path
import pkg_resources
import subprocess
import platform
import httpx
import os


HOST = "http://127.0.0.1"
FOLDER = platform.system()
if not FOLDER:
    raise Exception("Unknown OS")

BIN = pkg_resources.resource_filename(
    "pygopus",
    Path(f"/bin/{FOLDER}/pygobin"),
)


if platform.system() == "Windows":
    BIN = pkg_resources.resource_filename(
        "pygopus",
        Path(f"/bin/{FOLDER}/pygobin.exe"),
    )

service_pool = {}


def check_path(path: str):
    p = Path(path)
    if not p.exists():
        raise Exception(f"{ path } is not exists.Please check carefully")


def create_workbook(path: str):
    import shutil

    tpl = pkg_resources.resource_filename(
        "pygopus",
        Path("/bin/tpl.xlsx"),
    )
    shutil.copyfile(tpl, Path(path))


@dataclass
class XlInfo:
    pid: int
    port: int
    file_name: str


class Cell:
    ...


class Row(UserList):
    _pid: int
    row_axis: int
    sheet_name: str

    def _at(self, row_axis):
        self.row_axis = row_axis
        return self

    def _id(self, pid: int):
        self._pid = pid
        return self

    def _info(self, pid: int, row_axis: int, sheet_name: str):
        self._at(row_axis)
        self._id(pid)
        self.sheet_name = sheet_name
        return self

    def highlight(self, at: int = None, color="#FEF9B0"):
        color = [color]
        from string import ascii_uppercase

        targets = [f"{l}{self.row_axis}" for l, _ in zip(ascii_uppercase, self.data)]
        # the line top here will be changed in future for a header caused data offset
        if at != None:
            targets = [f"{ascii_uppercase[at]}{self.row_axis}"]
            print(targets)

            res = HighLight(
                pid=self._pid,
                sheet_name=self.sheet_name,
                tar_type="cell",
                targets=targets,
                color=color,
            ).post()
            return res

        res = HighLight(
            pid=self._pid,
            sheet_name=self.sheet_name,
            tar_type="row",
            targets=targets,
            color=color,
        ).post()

        return res


class WorkBook:
    @classmethod
    def open(cls, paths: List[str]):
        return [cls(p) for p in paths]

    def __init__(
        self,
        path: str,
        write_mode="",
        debug=False,
    ) -> None:
        # check file here
        if write_mode != "w+":
            # means user want open, so you gotta if file exists.
            check_path(path)

        else:
            create_workbook(path)
            print(f"{path} file created.")

        port = randint(45555, 55588)
        pygo_bin = Path(BIN)
        mode = os.stat(pygo_bin).st_mode | 0o100
        pygo_bin.chmod(mode)

        # if os.environ.get("code_platform") != "linux":
        # pygo_bin.chmod(mode)
        # only wroks on 云课堂 docker

        cmd = f"{BIN} -path {path} -port {port}".split()

        # p = subprocess.Popen(args=cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        kwd = {}
        if debug:
            ...
        else:
            kwd = dict(
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        p = subprocess.Popen(args=cmd, **kwd)
        self._pid = p.pid
        self.file_name = str(Path(path).abspath())

        info = XlInfo(
            pid=p.pid,
            port=port,
            file_name=self.file_name,
        )
        service_pool.update({self._pid: info})

        while True:
            try:
                res = Hello(pid=self._pid).get()
                break
            except httpx.ConnectError as e:
                if debug:
                    print("Waiting for starting server.")

    def __repr__(self):
        return f"<pygopus.WorkBook at='{self.file_name}'>"

    def __len__(self):
        return len(self.sheets)

    def __getitem__(self, k):
        sheets = {sh.name: sh for sh in self.sheets}
        return sheets[k]

    def __setitem__(self, k: str, v: "Sheet"):
        ...

    def get_sheet(self, name: str):
        return self[name]

    def add(self, name: str):
        res = AddSheet(
            pid=self._pid,
            sheet_name=name,
        ).get()
        return "ok"

    def delete(self, name: str):
        DeleteSheet(
            pid=self._pid,
            sheet_name=name,
        ).get()
        return "ok"

    @property
    def sheets(self):
        res = GetSheets(pid=self._pid).get()
        return [
            Sheet(
                index,
                name,
                pid=self._pid,
            )
            for index, name in res.items()
        ]

    def save(self):
        Save(pid=self._pid).get()

    def save_as(self, path: str):
        SaveAs(pid=self._pid, path=path).get()

    def close(self):
        import psutil

        # Close(file_name=self.file_name).get()
        ps = psutil.Process(self._pid)
        ps.terminate()
        # ps.kill()


class Sheet:
    def __init__(
        self,
        index: int,
        name: str,
        pid: int,
    ) -> None:
        self.name = name
        self._index = index
        self._pid = pid
        self._col_offset = None
        self._row_offset = None

    def __setitem__(self, k, v):
        self.set(k, v)

    def __getitem__(self, k):
        ...

    def __repr__(self):
        return f"<pygopus.Sheet name='{self.name}'>"

    def config(self, header, **kwd):
        ...

    def header_range(self):
        ...

    @cached_property
    def header(self):
        return self.rows[0]

    @property
    def rows(self):
        res = GetRows(
            sheet_name=self.name,
            pid=self._pid,
        ).get()
        # return res
        return [
            Row(r)._info(
                pid=self._pid,
                row_axis=i + 1,
                sheet_name=self.name,
            )
            for i, r in enumerate(res)
        ]

    @property
    def cols(self):
        res = GetCols(
            pid=self._pid,
            sheet_name=self.name,
        ).get()

        return res

    def get(self, axis: str):

        res = GetCell(
            pid=self._pid,
            sheet_name=self.name,
            axis=axis,
        ).get()
        return res

    def set(self, axis: str, val: Any):

        res = SetCell(
            pid=self._pid,
            sheet_name=self.name,
            axis=axis,
            val=val,
        ).get()
        return res

    def batch_set(self, *args, data: List):

        for index, axis in enumerate(args):
            res = SetCell(
                pid=self._pid,
                sheet_name=self.name,
                axis=axis,
                val=data[index],
            ).get()
        return "ok"

    def write_rows(self, data: List, start_at="A"):
        rows = {f"{start_at}{index+1}": d for index, d in enumerate(data)}
        res = WriteRows(
            pid=self._pid,
            sheet_name=self.name,
            rows=rows,
        ).post()
        return res

    def delete_row(self, row_axis: int):
        res = DeleteRow(
            pid=self._pid,
            sheet_name=self.name,
            row_axis=row_axis,
        ).get()
        return

    def append_col(self, col: List, force=False):
        if force:
            # convert col element to every row's last element
            added_rows = [row + [str(col[index])] for index, row in enumerate(self.rows)]
            res = self.write_rows(added_rows)
            return

        res = TotalCols(
            pid=self._pid,
            sheet_name=self.name,
        ).get()

        assert isinstance(res, dict)
        next_key = res["nextkey"]

        for index, val in enumerate(col):
            axis = f"{next_key}{index+1}"
            self.set(axis=axis, val=val)

        return

    def test_col(self):
        res = TotalCols(
            pid=self._pid,
            sheet_name=self.name,
        ).get()
        return res

    # contains gt lt eq
    def find(
        self,
        val: str = "",
        regex: str = "",
    ):
        ...

    def option(self):
        ...


class Operator:
    ...


class RowHelper:
    ...
