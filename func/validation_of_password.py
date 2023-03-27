import re

def validate_password(arg):
    if len(arg) < 8:
        print("Убедитесь, что ваш пароль состоит как минимум из 8 символов")
    elif re.search('[0-9]',arg) is None:
        print("Убедитесь, что в вашем пароле есть цифра")
    elif re.search('[A-Z]',arg) is None:
        print("Убедитесь, что в вашем пароле есть заглавная буква")
    else:
        print("Ваш пароль, кажется, в порядке")
        return arg