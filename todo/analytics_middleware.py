from django.utils.timezone import now
from todoapp.models import Analytics
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User

class AnalyticsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # print(request.META)
        # pass
        if request.user.is_authenticated:
        
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            ip_address = request.META.get('REMOTE_ADDR', '')
            analytics, created = Analytics.objects.get_or_create(user=request.user)
            analytics.last_login = now()
            analytics.ip_address = ip_address
            analytics.user_agent = user_agent
            analytics.save()
        else:
            user = User.objects.get(id=8)
            analytics, created = Analytics.objects.get_or_create(user=user)
