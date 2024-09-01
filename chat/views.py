from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Message
from django.conf import settings
from .rag import ask

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)
persistent_directory = str(settings.BASE_DIR / "db" / "chroma_db")
chroma_db = Chroma(collection_name="documents", embedding_function=embeddings, persist_directory=persistent_directory)

def index(request):
    messages = Message.objects.all()

    return render(request, 'chat.html', {'messages': messages})

def create_user_message(request):
    content = request.POST.get('content')
    user_message = Message(role=Message.USER, content=content)
    user_message.save()
    assistant_message = Message(role=Message.ASSISTANT, content=ask(chroma_db, content))
    assistant_message.save()

    user_html = render_to_string('components/user_message.html', {'content': user_message.content}, request)
    assistant_html = render_to_string('components/assistant_message.html', {'content': assistant_message.content}, request)

    return HttpResponse(user_html + assistant_html)