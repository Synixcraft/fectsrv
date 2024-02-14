

import os

from config import (
    AFD_LINK,
    COFFEE_LINK,
    ENABLE_CELERY,
    FREE_DOWNLOAD,
    REQUIRED_MEMBERSHIP,
    TOKEN_PRICE,
)
from database import InfluxDB
from utils import get_func_queue


class BotText:
    start = """
    Welcome to The Video Downloader Bot🤖 Pls Send A Video Link To Download.
    
    Support Me 🙂 [Buy Me A Coffee](https://www.buymeacoffee.com/abel360w)"""

    help = f"""
1. If the bot doesn't work, pls try again Or join https://t.me/Anonxc

2. Supported Sites List: [supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
    """

    about = "A Simple Video Downloader For Downloading Vides From Various Sites .Hosted By @Abel360w."

    inline_mode = "Search @FetchRobot_Inline_bot To Search For More Than 10000 Files From Our DataBase 🤖"

    all_commands =all_commands = """Here Is the List Of All Commands:
/start - Let's Start The Bot 🚀
/about - Know More About The Bot ℹ️
/help - Want Some Help Click Here ! ❓
/ytdl - Download Video In Group 📹
/settings - Set Your Preferences ⚙️
/buy - Buy Download Token 💳
/direct - Download a File Directly 📥
/sub - Subscribe To A YT Channel 📺
/unsub - Unsubscribe From A YT Channel ❌
/sub_count - Check Subscription Status [Owner Special] 🔢
/uncache - Delete Cache For This Link [Owner Special] 🗑️
/purge - Remove All Tasks [Owner Special] 🧹
/inline_mode - Search for files in our database 🔍"""

    buy = f"""Currently /buy Is Disabled And You Cannot Buy Paid Tokens Sorry For The Inconvinience ! """

    private = "This bot is for private use"

    membership_require = f"You need to join this group or channel to use this bot\n\nhttps://t.me/{REQUIRED_MEMBERSHIP}"

    settings = """
Please choose the preferred format and video quality for your video. These settings only **apply to YouTube videos**.

High quality is recommended. Medium quality aims to 720P, while low quality is 480P.

If you choose to send the video as a document, it will not be possible to stream it.

Your current settings:
Video quality: **{0}**
Sending format: **{1}**
"""
    custom_text = os.getenv("CUSTOM_TEXT", "")

    premium_warning = """
    Your file is too big, do you want me to try to send it as premium user? 
    This is an experimental feature so you can only use it once per day.
    Also, the premium user will know who you are and what you are downloading. 
    You may be banned if you abuse this feature.
    """

    @staticmethod
    def get_receive_link_text() -> str:
        reserved = get_func_queue("reserved")
        if ENABLE_CELERY and reserved:
            text = f"Your tasks was added to the reserved queue {reserved}. Processing...\n\n"
        else:
            text = "Your task was added to active queue.\nProcessing...\n\n"

        return text

    @staticmethod
    def ping_worker() -> str:
        from tasks import app as celery_app

        workers = InfluxDB().extract_dashboard_data()
        # [{'celery@BennyのMBP': 'abc'}, {'celery@BennyのMBP': 'abc'}]
        response = celery_app.control.broadcast("ping_revision", reply=True)
        revision = {}
        for item in response:
            revision.update(item)

        text = ""
        for worker in workers:
            fields = worker["fields"]
            hostname = worker["tags"]["hostname"]
            status = {True: "✅"}.get(fields["status"], "❌")
            active = fields["active"]
            load = "{},{},{}".format(fields["load1"], fields["load5"], fields["load15"])
            rev = revision.get(hostname, "")
            text += f"{status}{hostname} **{active}** {load} {rev}\n"

        return text
