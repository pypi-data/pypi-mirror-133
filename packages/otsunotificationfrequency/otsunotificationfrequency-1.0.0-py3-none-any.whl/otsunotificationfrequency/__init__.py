__all__ = (
    'NotificationFrequency',
    'NF_VALUE_REGEX',
)

import re

from typing import Any, Union

NF_VALUE_REGEX = '^([1-9][0-9]*)(%)?$'


class NotificationFrequency:
    """要素数が確定されたシーケンスの途中で処理を挟むタイミングの判定を補助します。
    """

    @property
    def length(self) -> int:
        """管理しているシーケンスの要素数です。
        """
        return self.__length

    @length.setter
    def length(self, length: int) -> None:
        """管理するシーケンスの要素数を設定します。
        """
        self.set_length(length)

    def __init__(self, nf_value: Union[int, str, 'NotificationFrequency']) -> None:
        """要素数が確定されたシーケンスの途中で処理を挟むタイミングの判定を補助するインスタンスを生成します。

        Args:
            nf_value (Union[int, str, NotificationFrequency]): 頻度です。

        Raises:
            ValueError: 上記以外の使用できない値を指定した場合に投げられます。
        """
        if type(nf_value) is NotificationFrequency:
            nf_value = str(nf_value)
        should_raise = False
        if type(nf_value) is str:
            if (match := re.search(NF_VALUE_REGEX, nf_value)):
                v, p = match.groups()
                v = int(v)
                self.__frequency = v
                if p is None:
                    self.__use_percentage = False
                elif v <= 100:
                    self.__use_percentage = True
                else:
                    should_raise = True
            else:
                should_raise = True
        elif type(nf_value) is int:
            self.__frequency = nf_value
            self.__use_percentage = False
        else:
            should_raise = True
        if should_raise or self.__frequency <= 0:
            msg = f'"{nf_value}"は使用することができない値です。'
            raise ValueError(msg)
        self.__before = 0
        self.__length = -1

    def check_and_get_percentage(self, idx: int) -> tuple[bool, int]:
        """現在の進捗が通知に値するかを判定し、進捗率と共に返します。

        Args:
            idx (int): 現在の進捗です。

        Raises:
            AttributeError: 管理するシーケンスの要素数が設定されていない場合に投げられます。

        Returns:
            tuple[bool, int]: (通知に値するか否か, 進捗率)のタプルです。
        """
        if self.length == -1:
            msg = 'このインスタンスにシーケンスの要素数を与えてください。'
            raise AttributeError(msg)
        percentage = idx * 100 // self.length
        if percentage == 100:
            self.__before = percentage
            return True, percentage
        if self.__use_percentage:
            if percentage - self.__before >= self.__frequency:
                self.__before = percentage
                return True, percentage
            return False, percentage
        else:
            if idx - self.__before >= self.__frequency:
                self.__before = idx
                return True, percentage
            return False, percentage

    def set_length(self, length: int) -> None:
        """管理するシーケンスの要素数を設定し、進捗を初期化します。
        """
        self.__length = length
        self.__before = 0

    def __str__(self) -> str:
        res = [str(self.__frequency)]
        if self.__use_percentage:
            res.append('%')
        return ''.join(res)

    def __eq__(self, other: Any) -> bool:
        if type(other) is NotificationFrequency:
            return str(self) == str(other)
        return False

    def __call__(self, idx: int) -> tuple[bool, int]:
        return self.check_and_get_percentage(idx)
