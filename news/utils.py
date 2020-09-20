#  Миксины


class UpperMixin(object):
    """
    title страниц выводить заглавными буквами
    """
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()
