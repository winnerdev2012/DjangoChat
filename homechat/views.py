from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
# Create your views here.


class HomeChatBaseView(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.LOGIN_URL

class HomeChatView(HomeChatBaseView):
    def get(self, request):
        return render(request, 'pages/home.html')