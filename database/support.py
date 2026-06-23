import asyncio
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid

from database.sql import query_msg


async def users_info(bot):
    active_users = 0
    blocked_users = 0

    users = await query_msg()

    for user in users:
        user_id = int(user[0])

        try:
            # coba kirim "typing action"
            await bot.send_chat_action(user_id, "typing")
            active_users += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except (UserIsBlocked, PeerIdInvalid):
            blocked_users += 1

        except Exception:
            # error lain dianggap tidak aktif
            blocked_users += 1

    return active_users, blocked_users
