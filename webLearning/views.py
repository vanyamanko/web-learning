from django.utils import translation
from django.conf import settings
from django.shortcuts import redirect

def set_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            request.session[translation.LANGUAGE_SESSION_KEY] = language
            translation.activate(language)
    return redirect(request.META.get('HTTP_REFERER', '/'))
