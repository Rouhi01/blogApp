from home.models import WebsiteMeta
def WebsiteMeta_context(request):
    website_info = None
    if WebsiteMeta.objects.all().exists():
        webiste_info = WebsiteMeta.objects.all()[0]
    return {'website_info':webiste_info}
