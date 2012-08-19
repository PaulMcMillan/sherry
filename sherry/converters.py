import re
from werkzeug import routing


def strip_mac(value):
    return re.sub('[\W_]', '', value).lower()


class MacConverter(routing.BaseConverter):
    """ Strips non-alphanumeric characters from input mac addresses """

    def to_python(self, value):
        return strip_mac(value)

    def to_url(self, value):
        return strip_mac(value)
