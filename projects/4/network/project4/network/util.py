from django.core.paginator import Paginator

def paginate(request, queryset, posts_per_page):
    paginator = Paginator(queryset, posts_per_page)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return posts