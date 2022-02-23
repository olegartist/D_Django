from django import template
from app.models import Posts, Clicks

register = template.Library()

@register.filter(name='multiply')  # регистрируем наш фильтр под именем multiply, чтоб django понимал, что это именно фильтр, а не простая функция
def multiply(value, arg):
    # первый аргумент здесь — это то значение, к которому надо применить фильтр,
    # второй аргумент — это аргумент фильтра, т. е. примерно следующее будет в шаблоне value|multiply:arg
    if isinstance(value, str) and isinstance(arg, int):
        # проверяем, что value — это точно строка, а arg — точно число, чтобы не возникло курьёзов
        return str(value) * arg  # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
    else:
        raise ValueError(f'Нельзя умножить {type(value)} на {type(arg)}')
        #  в случае, если кто-то неправильно воспользовался нашим тегом, выводим ошибку

# @register.filter(name='censor')
# def censor(value):
#     res = value
#     if isinstance(value, str):
#         xx = list()
#         for ww in Russian_mat.objects.all():
#             xx.append(ww.word)
#         for ss in value.split():
#              if ss.lower() in xx:
#                  res = value.replace(ss, 'x' * len(ss) )
#         return res
#     else:
#         raise ValueError(f'Нельзя фильтровать {type(value)}')
#
@register.filter(name='all_clicks')
def all_clicks(value, arg):
    post_id = int(arg)
    #cur_user_id = int(value)
    cc = Clicks.objects.filter(post_id=post_id, show=True).count()
    res = ''
    if cc > 0: res = cc
    return res

@register.filter(name='att_clicks')
def att_clicks(value, arg):
    post_id = int(arg)
    cur_user_id = int(value)
    res = ''
    if Posts.objects.get(id=post_id).user.id == cur_user_id:
        cc = Clicks.objects.filter(post_id=post_id, show=False).count()
        if cc > 0: res = cc
    return res
