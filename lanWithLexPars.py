import json
from sly import Lexer, Parser
from pathlib import Path


class MyLexer(Lexer):
    tokens = {GROUP_SYMBOL, STUDENT_SYMBOL, START, END, GROUP, NUMBER, LINE}

    ignore = r' \t\r'
    ignore_n = r'\n'
    ignore_comm = r'\~.*'

    GROUP_SYMBOL = r'\*'
    STUDENT_SYMBOL = r'\$'
    START = r'\('
    END = r'\)'
    GROUP = r'[^ \n\t\r\~();\'\*\$]+'
    NUMBER = r'[0-9]+'
    LINE = r"'[^\)\(\:\']*'"


class MyParser(Parser):
    tokens = MyLexer.tokens

    @_('none')
    def texts(self, s):
        return []

    @_('none')
    def names(self, s):
        return []

    @_('none')
    def about(self, s):
        return []

    @_('')
    def none(self, s):
        pass

    @_('name')
    def sub(self, s):
        return s.name

    @_('text texts')
    def texts(self, s):
        return [s.text] + s.texts

    @_('group student subject')
    def text(self, s):
        return dict(groups=s.group,
                    students=s.student,
                    subject=s.subject)

    @_("START sub END")
    def subject(self, s):
        return s.sub

    @_("START STUDENT_SYMBOL info about END")
    def student(self, s):
        temp = s.info.split()
        return [dict(age=int(temp[0]),
                     group=(temp[1]),
                     name=(temp[2] + " " + temp[3]))] + s.about

    @_("START GROUP_SYMBOL name names END")
    def group(self, s):
        return [s.name] + s.names

    @_('info about')
    def about(self, s):
        temp = s.info.split()
        return [dict(age=int(temp[0]),
                     group=(temp[1]),
                     name=(temp[2] + " " + temp[3]))] + s.about

    @_('LINE')
    def info(self, s):
        return s[0][1:-1]

    @_('name names')
    def names(self, s):
        return [s.name] + s.names

    @_('NUMBER')
    def name(self, s):
        return int(s[0])

    @_('GROUP')
    def name(self, s):
        return s[0]

    @_('LINE')
    def name(self, s):
        return s[0][1:-1]


class MyLanguage:
    lexer = MyLexer()
    parser = MyParser()

    def get_json_data(self):
        data = Path(file).read_text(encoding='utf-8')
        result = self.parser.parse(self.lexer.tokenize(data))
        for i in range(len(result)):
            print(json.dumps(result[i], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    file = "D:\\Программирование\\Python\\HW_CONFIG\\mirea.txt"
    MyLanguage().get_json_data()
