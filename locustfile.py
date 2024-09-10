from locust import HttpUser, task, constant

class ChatUser(HttpUser):
    wait_time = constant(1)
    @task
    def send_message(self):
        data = {
            'content': 'Your message content here'
        }

        self.client.post('/chat/create-user-message', data=data)

# class AdminUser(HttpUser):
#     @task
#     def get_admin(self):
#         self.client.get('/admin')