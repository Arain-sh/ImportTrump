import apify
import time
import requests
import json
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config():
    """加载配置文件"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("config.json not found. Please create one from config.example.json")
        raise

def load_last_post_ids():
    """加载上次处理的帖子ID"""
    try:
        with open('last_post_ids.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_last_post_ids(post_ids):
    """保存帖子ID"""
    with open('last_post_ids.json', 'w') as f:
        json.dump(list(post_ids), f)

def send_notification(webhook_url, content):
    """发送通知到IFTTT"""
    try:
        payload = {"value1": content}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            logger.info("Notification sent successfully")
        else:
            logger.error(f"Failed to send notification: {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

def main():
    # 加载配置
    config = load_config()
    apify_token = config.get('apify_token')
    webhook_url = config.get('ifttt_webhook_url')
    poll_interval = config.get('poll_interval', 300)  # 默认5分钟

    # 初始化Apify客户端
    client = apify.Client(apify_token)

    # 加载上次帖子ID
    last_post_ids = load_last_post_ids()

    while True:
        try:
            # 运行Apify爬虫
            input_data = {"identifiers": ["@realDonaldTrump"]}
            run = client.actor("louisdeconinck/truth-social-scraper").call(run_input=input_data)
            dataset = run.dataset
            items = list(dataset.iterate_items())

            # 提取当前帖子ID
            current_post_ids = {item['id'] for item in items if 'id' in item}

            # 检测新帖子
            new_post_ids = current_post_ids - last_post_ids

            # 处理新帖子
            for post_id in new_post_ids:
                post = next((item for item in items if item.get('id') == post_id), None)
                if post and 'content' in post:
                    logger.info(f"New post detected: {post['content']}")
                    send_notification(webhook_url, post['content'])

            # 更新并保存帖子ID
            last_post_ids.update(new_post_ids)
            save_last_post_ids(last_post_ids)

        except Exception as e:
            logger.error(f"Error occurred: {e}")

        # 等待下一次轮询
        logger.info(f"Waiting for {poll_interval} seconds...")
        time.sleep(poll_interval)

if __name__ == "__main__":
    main()
