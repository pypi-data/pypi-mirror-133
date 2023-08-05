__all__ = (
    'CNotificationFrequency',
    'VNotificationFrequency',
)
try:
    from typing import Any

    from otsuvalidator.bases import Converter, Validator

    from . import NotificationFrequency

except ImportError as e:
    msg = 'このモジュールは"otsuvalidator"をインストールしている場合のみ使用できます。'
    raise ImportError(msg)


class VNotificationFrequency(Validator):

    def validate(self, value: Any) -> NotificationFrequency:
        if type(value) is not NotificationFrequency:
            msg = self.ERRMSG('NotificationFrequency型である必要があります', value)
            raise TypeError(msg)
        return value


class CNotificationFrequency(VNotificationFrequency, Converter):

    def validate(self, value: Any) -> NotificationFrequency:
        if type(value) is not NotificationFrequency:
            try:
                value = NotificationFrequency(value)
            except:
                msg = self.ERRMSG('NotificationFrequency型として扱える必要があります', value)
                raise TypeError(msg)
        return super().validate(value)

    def super_validate(self, value: Any) -> NotificationFrequency:
        return super().validate(value)
