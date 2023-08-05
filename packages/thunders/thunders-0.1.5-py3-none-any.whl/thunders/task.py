# -*- coding: utf-8 -*-
# @author: leesoar

"""Thunder Download"""

import base64
import json
import subprocess
from time import sleep
from typing import Iterable

import pyperclip


__all__ = ["Task", "GroupTask"]


class Task:
    def __init__(self, url: str, name: str = None):
        self.url = self.encode(url)
        self.name = name
        self.dir = ""
        self.origin_url = url

    @staticmethod
    def encode(url) -> str:
        encoded_url = base64.b64encode(f"AA{url}ZZ".encode()).decode()
        return f"thunder://{encoded_url}"

    def create(self) -> dict:
        task = {
            "url": self.url,
            "dir": self.dir,
            "originUrl": self.origin_url,
        }
        self.name and task.update({
            "name": self.name,
        })
        return task


class GroupTask(list):
    dirname = "thunders"
    user_agent = "Bot"
    referer = ""
    min_version = "10.0.1.0"

    def __init__(self, name: str, thread_cnt=10):
        super().__init__()
        self.name = name
        self.thread_cnt = thread_cnt
        self.__already_run = False
        self.__check_protocol()

    def __check_protocol(self):
        import sys
        if sys.platform == "win32":
            self.__protocol = "thunderx://"
            self.__command = "start"
            self.__is_windows = True
        else:
            self.__protocol = "thunders://"
            self.__command = "open"
            self.__is_windows = False

    def __create(self):
        task = {
            "downloadDir": self.dirname,
            "installFile": "",
            "taskGroupName": self.name,
            "tasks": self,
            "minVersion": self.min_version,
            "userAgent": self.user_agent,
            "hideYunPan": "'1'",
            "threadCount": self.thread_cnt,
            "referer": self.referer,
        }
        return task

    def json(self) -> str:
        return json.dumps(self.__create(), ensure_ascii=False, separators=",:")

    def run(self, timeout=3):
        pyperclip.copy(self.__repr__())
        try:
            subprocess.check_output([self.__command, Task.encode("DummyLink/Copy-From-Clipboard")],
                                    shell=self.__is_windows, timeout=timeout)
        except subprocess.CalledProcessError:
            print("[ERROR] Thunder version is wrong or not installed!")
        else:
            # 由于windows下，start命令仅启动一次后，无法检测剪切板，所以延迟启动第二次来达到效果
            if self.__is_windows and self.__already_run is False:
                self.__already_run = True
                sleep(timeout) or self.run()
        finally:
            self.__already_run = True

    def append(self, task: Task):
        return super(GroupTask, self).append(task.create())

    def extend(self, tasks: Iterable[Task]):
        return super(GroupTask, self).extend(map(Task.create, tasks))

    def dump(self) -> str:
        return self.__repr__()

    def __str__(self):
        return f"{self.__protocol}{self.json()}"

    __repr__ = __str__
