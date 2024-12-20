from django import template

register = template.Library()


@register.inclusion_tag('web/car_card.html')
def car_card(car):
    return {
        'car': car,
    }
