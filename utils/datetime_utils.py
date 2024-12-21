# utils/datetime_utils.py
from datetime import datetime

import pytz
from django.utils import timezone


def convert_to_utc(dt: str | datetime) -> datetime:
    """Преобразует время в UTC.

    :param `dt`:Время в виде строки (форматы: 'YYYY-MM-DD HH:MM' или 'YYYY-MM-DD HH:MM±HHMM') \
                  или объекта datetime, которое нужно преобразовать.
    :type dt: str | datetime

    :return: Время, преобразованное в UTC.
    :rtype: datetime

    :raises ValueError: Если строка времени не соответствует ожидаемому формату.
    :raises TypeError: Если передан некорректный тип данных.
    :raises Exception: Для всех остальных исключений, возникающих при преобразовании.

    :example:
        dt = convert_to_utc("2024-08-01 12:00")
        dt = convert_to_utc("2024-08-01 12:00+0300")
        dt = convert_to_utc(datetime(2024, 8, 1, 12, 0))
    """
    try:
        if isinstance(dt, str):
            try:
                # Попытка парсинга строки с временной зоной
                dt = datetime.strptime(dt, "%Y-%m-%d %H:%M%z")
            except ValueError:
                try:
                    # Попытка парсинга строки без временной зоны
                    dt = datetime.strptime(dt, "%Y-%m-%d %H:%M")
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())
                except ValueError:
                    raise ValueError(
                        "Формат времени должен быть 'YYYY-MM-DD HH:MM' или 'YYYY-MM-DD HH:MM±HHMM'.",
                    )

        if not isinstance(dt, datetime):
            raise TypeError("Ожидался объект datetime или строка.")

        if dt.tzinfo is None:
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return dt.astimezone(pytz.UTC)
    except Exception as e:
        raise ValueError(f"Не удалось преобразовать время в UTC: {e}")
