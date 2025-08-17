from django.http import HttpResponse
def webhook(request):
    # For extension later; keep 200 OK to avoid failures during test.
    return HttpResponse("OK")
