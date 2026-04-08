import json
from django.shortcuts import render
from django.views import View
from .services.green_api import GreenAPIService

class IndexView(View):
    template_name = 'green_api_client/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        action = request.POST.get('action')
        id_instance = request.POST.get('idInstance')
        api_token = request.POST.get('ApiTokenInstance')

        context = {
            'idInstance': id_instance,
            'ApiTokenInstance': api_token,
            'action': action,
            'phone_number_msg': request.POST.get('phone_number_msg', ''),
            'message_text': request.POST.get('message_text', ''),
            'phone_number_file': request.POST.get('phone_number_file', ''),
            'file_url': request.POST.get('file_url', ''),
        }

        if not id_instance or not api_token:
            context['error'] = 'idInstance и ApiTokenInstance обязательны'
            return render(request, self.template_name, context)

        result, error = None, None

        if action == 'getSettings':
            result, error = GreenAPIService.get_settings(id_instance, api_token)
        elif action == 'getStateInstance':
            result, error = GreenAPIService.get_state_instance(id_instance, api_token)
        elif action == 'sendMessage':
            phone = context['phone_number_msg']
            message = context['message_text']
            chat_id = f"{phone}@c.us" if '@' not in phone else phone
            result, error = GreenAPIService.send_message(id_instance, api_token, chat_id, message)
        elif action == 'sendFileByUrl':
            phone = context['phone_number_file']
            url_file = context['file_url']
            chat_id = f"{phone}@c.us" if '@' not in phone else phone
            result, error = GreenAPIService.send_file_by_url(id_instance, api_token, chat_id, url_file)
        else:
            context['error'] = 'Неизвестное действие'

        if error:
            context['response'] = json.dumps(result, indent=4, ensure_ascii=False)
        else:
            context['response'] = json.dumps(result, indent=4, ensure_ascii=False)

        return render(request, self.template_name, context)
