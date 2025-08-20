from locust import HttpUser, task, between

class StudentUser(HttpUser):
    # Wait between requests (random 1–2s), so it's not 100% burst
    wait_time = between(1, 2)

    @task(3)   # more weight → more requests
    def get_students(self):
        self.client.get("/students")

    @task(1)
    def get_students1(self):
        self.client.get("/students1")

    @task(1)
    def get_students2(self):
        self.client.get("/students2")

    @task(1)
    def get_students3(self):
        self.client.get("/students3")

    @task(2)
    def home(self):
        self.client.get("/")

