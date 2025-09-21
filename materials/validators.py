from django.core.exceptions import ValidationError
import re


def validate_youtube_url(value):
    if value:
        pattern = r"^(https?://)?(www\.)?youtube\.com/"
        if not re.match(pattern, value):
            raise ValidationError("Разрешены только ссылки на youtube.com")
