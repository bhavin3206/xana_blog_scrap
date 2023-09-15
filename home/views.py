# django lib
from django.http import JsonResponse
import pandas as pd
from home.utils import Bot
from django.views import View

    

class task_list(View):
    def get(self, request):
        task_id = request.GET.get('task_id')
        bot = Bot(task_id)
        bot.filter_blog_posts()
        response = bot.scrape_blog_text()
        print('response send')
        return JsonResponse(response, safe=False)