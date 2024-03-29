from django.core.paginator import Paginator


POSTS_ON_PAGE: int = 10
# Колличество постов на странице


def page_obj_func(queryset, request):
    """Функция получения номера страницы для пагинации."""
    paginator = Paginator(queryset, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
