from locust import HttpUser, task

class ChatUser(HttpUser):
    @task
    def send_message(self):
        self.client.post('/chat/create-user-message')

class AdminUser(HttpUser):
    @task
    def get_admin(self):
        self.client.get('/admin')