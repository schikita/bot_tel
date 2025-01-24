
from src.db.models import Channel
from src.repositories.admin_repository import AdminRepository
from src.repositories.channel_repository import ChannelRepository
from src.repositories.post_repository import PostRepository
from src.schemas.posts import PostData
from src.services.lemma import lemma_service
from src.services.notification_service import NotificationService
from src.utils.http_requests import get_channel_posts


class ChannelParserService:
    @staticmethod
    async def parse_all_channels() -> None:
        """Запускает парсинг всех активных каналов."""
        channels = await ChannelRepository.fetch_active_channels()
        for channel in channels:
            if await ChannelRepository.is_due_for_parsing(channel):
                await ChannelParserService.process_channel_posts(channel)

    @staticmethod
    async def process_channel_posts(channel: Channel) -> None:
        """Парсит один канал и обрабатывает посты."""
        posts_data: list[PostData] = await get_channel_posts(channel.url)
        if not posts_data:
            return

        for post_data in posts_data:
            await ChannelParserService._process_single_post(channel, post_data)

        await ChannelRepository.set_next_parse_time(channel)

    @staticmethod
    async def _process_single_post(channel: Channel, post_data: PostData) -> None:
        if await PostRepository.post_exists(channel, post_data.post_id):
            return

        await PostRepository.create_post(
            channel=channel,
            post_id=post_data.post_id,
            text=post_data.text,
            published_at=post_data.published_at,
        )

        post_lemmas = lemma_service.lemmatize_text(post_data.text)

        for admin in await AdminRepository.get_subscribed_admins(channel):
            admin_lemmas = {word.lemma or lemma_service.lemmatize_word(word.word) for word in admin.words}
            matched_lemmas = post_lemmas.intersection(admin_lemmas)

            if matched_lemmas:
                await NotificationService.notify_admin(
                    admin=admin,
                    post_id=post_data.post_id,
                    channel=channel,
                    matched_keywords=matched_lemmas,
                )
