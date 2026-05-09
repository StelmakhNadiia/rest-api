from locust import HttpUser, task, between

class LibraryAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_all_books(self):
        with self.client.get("/books/?limit=10&offset=0", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")