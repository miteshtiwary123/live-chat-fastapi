from celery import Celery

celery = Celery(
    "worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task
def send_notification(user_id: int, message: str):
    # This is a dummy notification - replace with email/SMS/push code
    print(f"📩 Notification to User {user_id}: {message}")
    