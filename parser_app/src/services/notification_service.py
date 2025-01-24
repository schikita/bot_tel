from src.db.models import Admin, Channel


class NotificationService:
    @staticmethod
    async def notify_admin(admin: Admin, post_id: int, channel: Channel, matched_keywords: set[str]):
        text = (
            f"Админ: {admin.name} (ID: {admin.telegram_id})\n"
            f"Найден пост на канале: {channel.name} ({channel.url})\n"
            f"ID поста: {post_id}\n"
            f"Совпадения: {', '.join(matched_keywords)}\n"
        )
        #TODO: отправка уведомления в телеграм асинхронно через httpx
