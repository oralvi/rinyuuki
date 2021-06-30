# 订阅关键词

import re

import peony
from peony import PeonyClient

from rin import Service
from rin.config import twitter as cfg

from .util import format_tweet

sv = Service('uma-ura9-sniffer', enable_on_default=False, help_='嗅探新鲜出炉的9URA种马', bundle='umamusume')

async def track_stream():
    client = PeonyClient(
        consumer_key=cfg.consumer_key,
        consumer_secret=cfg.consumer_secret,
        access_token=cfg.access_token_key,
        access_token_secret=cfg.access_token_secret,
        proxy=cfg.proxy,
    )
    async with client:
        stream = client.stream.statuses.filter.post(track=['URA9'])

        async for tweet in stream:
            sv.logger.info("Got twitter event.")
            if peony.events.tweet(tweet):
                screen_name = tweet.user.screen_name
                if screen_name in cfg.uma_ura9_black_list:
                    continue    # black list
                if peony.events.retweet(tweet):
                    continue    # 忽略纯转推
                if tweet.get("quoted_status"):
                    continue    # 忽略引用转推
                if tweet.get("in_reply_to_screen_name"):
                    continue    # 忽略评论

                if not re.search(r'\d{9}', tweet.text):
                    continue    # 忽略无id的推特
                if re.search(r'ura(シナリオ)?([:：])?[0-7]', tweet.text, re.I):
                    continue    # 忽略低ura因子
                if re.search(r'目指|狙|チャレンジ', tweet.text, re.I):
                    continue    # 忽略未达成
                if re.search(r'青(因子)?[0-8]', tweet.text, re.I):
                    continue    # 忽略低星蓝
                if re.search(r'(スピ(ード)?|スタ(ミナ)?|パワー|根性?|賢さ?)\s*[0124578]', tweet.text, re.I):
                    continue    # 忽略低星蓝
                if re.search(r'ura(シナリオ)?([:：])?9(では|じゃ)', tweet.text, re.I):
                    continue    # 忽略否定型
                if re.search(r'青(因子)?9(では|じゃ)', tweet.text, re.I):
                    continue    # 忽略否定型

                msg = format_tweet(tweet)

                sv.logger.info(f"推送推文：\n{msg}")
                await sv.broadcast(msg, f" @{screen_name} 推文", 0.2)

            else:
                sv.logger.debug("Ignore non-tweet event.")
