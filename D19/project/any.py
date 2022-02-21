
def user_type(user):
    res = ''
    if user.is_staff:
        res = 'Администратор'
    else:
        if user.groups.filter(name='senior').exists():
            res = 'Спициалист'
        else:
            res = 'Пользователь'
    return res
