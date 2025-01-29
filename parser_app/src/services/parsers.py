import asyncio
from src.db.models import Channel
from src.repositories.admin_repository import AdminRepository
from src.repositories.channel_repository import ChannelRepository
from src.repositories.post_repository import PostRepository
from src.schemas.posts import PostData
from src.services.lemma import lemma_service
from src.services.notification_service import NotificationService
from src.utils.http_requests import get_channel_posts

class ChannelParserService:
    _semaphore = asyncio.Semaphore(40)

    @staticmethod
    async def parse_all_channels() -> None:
        """Запускает парсинг всех активных каналов."""
        channels = await ChannelRepository.fetch_active_channels()
        tasks = [
            ChannelParserService._process_channel_safe(channel) for channel in channels
        ]

        await asyncio.gather(*tasks)

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
    async def _process_channel_safe(channel: Channel) -> None:
        async with ChannelParserService._semaphore:
            if await ChannelRepository.is_due_for_parsing(channel):
                await ChannelParserService.process_channel_posts(channel)

    @staticmethod
    async def _process_single_post(channel: Channel, post_data: PostData) -> None:
        if await PostRepository.is_post_exists(channel, post_data.post_id):
            return

        await PostRepository.create_post(
            channel=channel,
            post_id=post_data.post_id,
            text=post_data.text,
            published_at=post_data.published_at,
        )

        for admin in await AdminRepository.get_subscribed_admins(channel):
            admin_lemmas = {
                word.lemma or lemma_service.lemmatize_word(word.word)
                for word in admin.words
            }

            post_bigrams = lemma_service.generate_phrases(post_data.text, n=2)
            post_trigrams = lemma_service.generate_phrases(post_data.text, n=3)
            
            matched_lemmas = lemma_service.find_matches_in_text(post_data.text, admin_lemmas)

            matched_bigrams = {bigram for bigram in post_bigrams if bigram in admin_lemmas}
            matched_trigrams = {trigram for trigram in post_trigrams if trigram in admin_lemmas}

            all_matches = matched_lemmas.union(matched_bigrams).union(matched_trigrams)

            if all_matches:
                await NotificationService.notify_admin(
                    admin=admin,
                    post_id=post_data.post_id,
                    channel=channel,
                    matched_keywords=all_matches,
                )
