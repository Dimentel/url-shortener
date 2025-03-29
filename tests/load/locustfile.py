# from locust import HttpUser, task, between
# import random
#
#
# class ShortenerUser(HttpUser):
#     wait_time = between(0.5, 2.5)
#     host = "http://localhost:8000"  # Тестируем внешний интерфейс
#
#     @task(weight=3)
#     def create_unique_link(self):
#         # Генерируем уникальные URL для теста
#         url = f"https://example.com/{random.randint(1, 100000)}"
#         self.client.post("/links/shorten", json={"original_url": url})
#
#     @task
#     def access_random_link(self):
#         # Пробуем получить случайную ссылку (может не существовать)
#         self.client.get(f"/links/{''.join(random.choices('abcdef123456', k=6))}")
