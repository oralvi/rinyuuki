from rin import Service
from .spider import *

svjp = Service('pcr-news-jp', bundle='pcr订阅', help_='日服官网新闻')

async def news_poller(spider:BaseSpider, sv:Service, TAG):
    if not spider.item_cache:
        await spider.get_update()
        sv.logger.info(f'{TAG}新闻缓存为空，已加载至最新')
        return
    news = await spider.get_update()
    if not news:
        sv.logger.info(f'未检索到{TAG}新闻更新')
        return
    sv.logger.info(f'检索到{len(news)}条{TAG}新闻更新！')
    await sv.broadcast(spider.format_items(news), TAG, interval_time=0.5)

@svjp.scheduled_job('cron', minute='*/5', jitter=20)
async def cy_news_poller():
    await news_poller(cygamesSpider, svjp, '日服官网')


async def send_news(bot, ev, spider:BaseSpider, max_num=5):
    if not spider.item_cache:
        await spider.get_update()
    news = spider.item_cache
    news = news[:min(max_num, len(news))]
    await bot.send(ev, spider.format_items(news), at_sender=True)


@svjp.on_fullmatch(('日服新闻', '日服日程'))
async def send_cy_news(bot, ev):
    await send_news(bot, ev, cygamesSpider)
