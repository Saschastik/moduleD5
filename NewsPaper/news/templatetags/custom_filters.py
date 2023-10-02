from django import template

register = template.Library()


@register.filter(name='censor')
def censor(text):
    forbidden_vocabulary = ['nba']

    for i in forbidden_vocabulary:
        text = text.replace(i, '<abn>')
        text = text.replace(i.upper(), '<abn>')

    return text