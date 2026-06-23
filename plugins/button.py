from config import FORCE_SUB, BUTTONS_PER_ROW, BUTTONS_JOIN_TEXT
from pyrogram.types import InlineKeyboardButton


def start_button(client):
    buttons = []

    # HELP BUTTON
    row = [
        InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help"),
        InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close"),
    ]
    buttons.append(row)

    # FORCE SUB BUTTONS
    if FORCE_SUB:
        dynamic_buttons = []
        current_row = []

        for key, value in FORCE_SUB.items():

            # ambil invite link dari client (AMAN + fallback)
            invite_link = getattr(client, f'invitelink{key}', None)

            if not invite_link:
                invite_link = value.get("link", "https://t.me")

            current_row.append(
                InlineKeyboardButton(
                    text=f"{BUTTONS_JOIN_TEXT} {key}",
                    url=invite_link
                )
            )

            if len(current_row) == BUTTONS_PER_ROW:
                dynamic_buttons.append(current_row)
                current_row = []

        if current_row:
            dynamic_buttons.append(current_row)

        buttons.extend(dynamic_buttons)

    # CLOSE BUTTON
    buttons.append([
        InlineKeyboardButton("ᴛᴜᴛᴜᴘ", callback_data="close")
    ])

    return buttons


def fsub_button(client, message):
    if not FORCE_SUB:
        return None

    buttons = []
    current_row = []

    for key, value in FORCE_SUB.items():

        invite_link = getattr(client, f'invitelink{key}', None)

        if not invite_link:
            invite_link = value.get("link", "https://t.me")

        current_row.append(
            InlineKeyboardButton(
                text=f"{BUTTONS_JOIN_TEXT} {key}",
                url=invite_link
            )
        )

        if len(current_row) == BUTTONS_PER_ROW:
            buttons.append(current_row)
            current_row = []

    if current_row:
        buttons.append(current_row)

    # retry button aman
    try:
        if hasattr(message, "command") and len(message.command) > 1:
            buttons.append([
                InlineKeyboardButton(
                    text="ᴄᴏʙᴀ ʟᴀɢɪ",
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
    except:
        pass

    return buttons
