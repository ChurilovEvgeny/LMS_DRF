import re

from rest_framework import serializers


class OnlyYouTubeLinkValidator:
    """Валидатор проверяет поле на наличии URL. Если URL есть, то ТОЛЬКО на YouTube, иначе ошибка"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value:dict):
        urls = self.__get_urls_from_string(value.get(self.field, ""))

        if self.__is_have_not_youtube_urls(urls):
            raise serializers.ValidationError("Указана ссылка на ресурс кроме YouTube")

    def __get_urls_from_string(self, data: str) -> list[str]:
        regex = r"(?P<url>https?://[^\s]+)"
        return re.findall(regex, data)

    def __is_have_not_youtube_urls(self, urls: list[str]) -> bool:
        youtube_urls = ("youtube.com", "youtu.be")

        def is_entry(checked_url: str) -> bool:
            return any(yu in checked_url for yu in youtube_urls)

        for url in urls:
            if not is_entry(url):
                return True

        return False
