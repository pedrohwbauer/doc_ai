from django.http import JsonResponse
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

    return JsonResponse({
        'answer': answer,
        'metadata': metadata
    })