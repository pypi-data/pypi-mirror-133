from .formatbase import FormatterBase
import extendable_json as json


class JSON_Formatter(FormatterBase):
    def write(self, file, data):
        file.write(json.dumps(data, indent=2))

    def read(self, file):
        return json.loads(file.read())
