import asyncio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Message
from rag.services import query
from asgiref.sync import sync_to_async

from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor()

def index(request):
    messages = Message.objects.all()

    return render(request, 'chat.html', {'messages': messages})

@csrf_exempt
async def create_user_message(request):
    content = request.POST.get('content')
    loop = asyncio.get_running_loop()

    user_message = Message(role=Message.USER, content=content)
    loop.run_in_executor(pool, lambda: user_message.save())

    chat_history = await sync_to_async(lambda: list(Message.objects.values_list('role', 'content')))()
    answer, metadata = await query(content, chat_history)

    assistant_message = Message(role=Message.ASSISTANT, content=answer)
    loop.run_in_executor(pool, lambda: assistant_message.save())

    return JsonResponse({
        'answer': answer,
        'metadata': metadata
    })