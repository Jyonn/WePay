from django.shortcuts import render


def get_index_html(request):
    return render(request, 'index.html')
