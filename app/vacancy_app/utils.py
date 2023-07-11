from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe


class DivErrorList(ErrorList):
    """
    Класс для кастомного css ошибок в формах, цвет текста ошибок красный
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return mark_safe('<div class="text-danger">%s</div>' %
                         "".join(['<div class="error">%s</div>' % e for e in self]))
