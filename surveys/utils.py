import string
import random


def unique_slug_generator(model_instance):
    """Генератор уникальных для модели слагов"""
    model_class = model_instance.__class__
    slug = slug_generator()

    while model_class._default_manager.filter(slug=slug).exists():
        slug = slug_generator()

    return slug


def slug_generator():
    """Генератор слага из 8 строчных символов нижнего регистра"""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))