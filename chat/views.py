from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Message
from rag.services import query

def index(request):
    messages = Message.objects.all()

    return render(request, 'chat.html', {'messages': messages})

def create_user_message(request):
    content = request.POST.get('content')
    user_message = Message(role=Message.USER, content=content)
    user_message.save()

    answer, metadata = query(user_message.content)

    assistant_message = Message(role=Message.ASSISTANT, content=answer)
    assistant_message.save()

    user_html = render_to_string('components/user_message.html', {'content': user_message.content}, request)
    assistant_html = render_to_string('components/assistant_message.html', {'content': assistant_message.content}, request)
    script = render_to_string('components/pdf_render.html', {'pdf_url': metadata['url'], 'pdf_page': metadata['page']}, request)

    return HttpResponse(user_html + assistant_html + script)