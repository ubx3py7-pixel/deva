from flask import Flask
from threading import Thread
import asyncio
import json
import os
import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

@app.route('/health')
def health():
    return "OK"

TOKENS = [
    "8511210915:AAEQFdWb-wePkU4z8Fz4_g-lRh-UZrP6syU",
"8199166304:AAFB4zwsjib3m0zm9V1bdw0bPucw50nHvq8",
"8272155257:AAElZnydU_i_S1HnS72JZ_sUCPNfEPm_xik",
"8073038152:AAGiA5oscVrvN0KprLz3YhLj9n6avT3OAKs", "7904263755:AAG0u--XkT-Eu-S3pdAwxO5E7hM6TuF6gHw",
"8257005872:AAFlrcpz2u4WJwiBvIKXZQKGpvRqQI2KU90",
    "8061799871:AAHIprGgp0xMf-XM6Tu49TVw0ZofACl__q8",
    "8275126499:AAGQSqngva9plgmXq4i80p_CkvlLlheIbCU",
"8320677399:AAEY9DbiaZlCqq6qEesWs5pGLhLlNwUXQcE",
"8511210915:AAEQFdWb-wePkU4z8Fz4_g-lRh-UZrP6syU",
]

OWNER_ID = 8534939542
SUDO_FILE = "8534939542"

RAID_TEXTS = [
    "𝐂𝐡𝐮𝐝 𝐊𝐞 𝐏𝐚𝐠𝐚𝐥 🐶.",
    "𝐓𝐞𝐫𝐢 𝐌𝐚 𝐊𝐢 𝐂𝐡𝐮𝐭🪐",
    "𝐓𝐞𝐫𝐢 ᵐᵃᵃ ᶜʰⁱⁿⁿᵃˡ😂 ",
    "𝐅𝐔𝐂𝐊 𝐎𝐅𝐅 🚮",
    "𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 ᵏⁱ ᵐᵒᵗⁱ ᵇʰᵒˢᵈⁱ 😱",
    "𝐒ᴛғᴜ ᗷ𝗂𝗍𝖼𝗁🥀🔥",
    "labour son 🎀🤸🏻",
    "langde chlke dikha 😤😤",
    "suck my cock ♨️",
    "poor👞",
    "hijda🙏🏻",
    "lame🥺",
    "chuddakd👋🏿 ",
    "bhag🥀",
    "tmkl🌙",
    "tmr🍃",
    "mc😁🍃",
    "bc⚡",
    "तेरी मां रंडल 🌹🫧",
    "चुदाई😏",
    "bsdk🎀",
    "tbkc🔥",
    "tbkl👋🏿",
    "tdkl🕳️",
    "tdkc😤",
    "tmc🥺",
    "gareeb🥰",
    "helpless kid😍",
    "normie🤪",
    "fuck u🫧 ",
    "चुदाई done ⚔️"
    "chakka",
    "suar",
    
]

NCEMO_EMOJIS = [
    "❤","🧡","💛","💚","🩵","💙","💜","🤎","🖤","🌼","🍁","🍂","🍄","🌾","🌱","🌿","🍃","☘","🩶","🤍","🩷","💘","💝","💖","💗","💓","💞","💕","🥀","🌺","🌷","🪷","🌸","💮","🏵","🪻","🌻","💌","💟","♥","❣","❤‍🩹","💔","❤‍🔥","💋","💐","🌹","🍀","🪴","🌵","🌴","🌳","🌲","🪵","⛰","🏔","❄","🫧","🌈","🔥","🌧","⛈","🕊️","🌘","😞","😆","😂","😍","😘","😚","😜","😝","😙","😌","😉","🙂","😊","😇","😐","😑","😶","😏","😒","🙄","😬","😒","🤣","😤","😠","😡","😳","😵","😲","😱","😰","😣","😖","😮","😓","😯","😪","😴","😷","🤒","🤕","🤢","🤮","🤧","🥵","🥶","😵‍💫","🤯","🤠","🤡","🤥","🤫","🤭","🤓","😈","👿","💀","👹","👺","💩","👻","👽","👾","🤖","🎃","😺","😸","😹","😻","😼","😽","🙀","🙈","🙉","🙊","🐵","🐒","🦍","🦧","🐶","🐕","🐩","🐺","🦊","🦝","🐱","🐈","🐯","🐅","🐆","🐴","🐎","🐖","🐷","🐽","🐏","🐑","🐐","🐪","🐫","🦒","🦏","🦓","🦌","🦙","🦘","🦡","🐁","🐀","🐹","🐰","🐇","🐿","🦔","🦇","🐻","🐨","🐼","🦥","🦦","🦨","🦘","🦡","🐾","🦃","🕊","🐦","🐧","🕋","🦉","🦅","🦚","🦜","🐸","🐊","🐢","🦎","🐍","🐲","🐉","🦕","🦖","🐙","🐚","🐌","🦋","🐛","🐜","🐝","🐞","🦗","🕷","🕸","🦂","🦟","🦠","💐","🌸","🌺","🌻","🌼","🌷","🌹","🌾","🌿","🍀","🍁","🍂","🍃","🍄","🍅","🍆","🥒","🥬","🌽","🥕","🧅","🧄","🧅","🌰","🍎","🍏","🍊","🍋","🍌","🍉","🍇","🍓","🍈","🍒","🍑","🍍","🥥","🥝","🍅","🍆","🥒","🥬","🌽","🥕","🧅","🧄","🧅","🌰","🍎","🍏","🍊","🍋","🍌","🍉","🍇","🍓","🍈","🍒","🍑","🍍","🥥","🥝","🍗","🍖","🥩","🥓","🌭","🥪","🌮","🌯","🥙","🧇","🥞","🥖","🫐","🥨","🥟","🥠","🥮","🦀","🦐","🦑","🐚","🐌","🦋","🐛","🐜","🐝","🐞","🦗","🕷","🕸","🦂","🦟","🦠","💐","🌸","🌺","🌻","🌼","🌷","🌹","🙇🏻","🙇🏻‍♂️","🙇🏻‍♀️","💃🏻","🕺🏻","💌","💘","💝","💖","💗","💓","💞","💕","💛","💚","🌘","🌗","🌖","🌕","🌑","🌒","🌓","🌔","🌚","🌝","🌞","🪐","🌟","🌠","🌌","🌍","🌎","🌏","🌋","🌊","🪂","🚀","🛸","🚁","🛩","🚂","🚊","🚆","🚄","🚅","🚇","🚈","🚉","🚝","🚋","🚌","🚍","🚎","🚐","🚑","🚒","🚓","🚔","🚕","🚖","🚗","🚘","🚙","🛻","🚚","🚛","🚜","🏎","🏍","🛵","🦽","🦼","🛺","🏍","🛵","🎉","🎊","🎈","🎌","🎍","🎎","🎏","🎐","🎑","🧨","🎀","🎁","🎗","🎟","🎫","🎖","🏆","🏅","🥇","🥈","👃🏻","💪🏻","👂🏻","👀","👁","👅","👄","💋","💦","💧","💨","💫","💥","💣","💢","💬","💭","💤","👂🏻","👀","👁","👅","👄","💋","💦","💧","💨","💫","💥","💣","🤚🏻","🖖🏻",
    "🌩","🌨","🌦","🌧","🌪","💦","☔","🪐",
]

if os.path.exists(SUDO_FILE):
    try:
        with open(SUDO_FILE, "r") as f:
            _loaded = json.load(f)
            SUDO_USERS = set(int(x) for x in _loaded)
    except:
        SUDO_USERS = {OWNER_ID}
else:
    SUDO_USERS = {OWNER_ID}
with open(SUDO_FILE, "w") as f:
    json.dump(list(SUDO_USERS), f)

def save_sudo():
    with open(SUDO_FILE, "w") as f:
        json.dump(list(SUDO_USERS), f)

group_tasks = {}
slide_targets = set()
slidespam_targets = set()
swipe_mode = {}
repeat_tasks = {}
pin_tasks = {}
apps, bots = [], []
delay = 0.1

logging.basicConfig(level=logging.INFO)

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid not in SUDO_USERS:
            return await update.message.reply_text("ʏᴏᴜʀ ᴡᴏʀᴅs ᴀʀᴇ ᴍᴇᴀɴɪɴɢʟᴇss. ɪ sᴇʀᴠᴇ ᴏɴʟʏ ᴍᴀᴅᴅʏ...")
        return await func(update, context)
    return wrapper

def only_owner(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        if uid != OWNER_ID:
            return await update.message.reply_text("ɪ ᴏɴʟʏ ғᴏʟʟᴏᴡ ᴍᴀsᴛᴇʀ ᴍᴀᴅᴅʏ's ᴄᴏᴍᴍᴀɴᴅs...")
        return await func(update, context)
    return wrapper

async def bot_loop(bot, chat_id, base, mode):
    i = 0
    while True:
        try:
            if mode == "raid":
                text = f"{base} {RAID_TEXTS[i % len(RAID_TEXTS)]}"
            else:
                text = f"{base} {NCEMO_EMOJIS[i % len(NCEMO_EMOJIS)]}"
            asyncio.create_task(bot.set_chat_title(chat_id, text))
            i += 1
            await asyncio.sleep(0)
        except Exception:
            await asyncio.sleep(0)

async def repeat_loop(bot, chat_id, text):
    while True:
        try:
            asyncio.create_task(bot.send_message(chat_id, text))
            await asyncio.sleep(0)
        except Exception:
            await asyncio.sleep(0)

async def pin_loop(bot, chat_id, text):
    while True:
        try:
            sent_msg = await bot.send_message(chat_id, text)
            asyncio.create_task(bot.pin_chat_message(chat_id, sent_msg.message_id, disable_notification=True))
            await asyncio.sleep(0)
        except Exception:
            await asyncio.sleep(0)

async def promote_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    results = []
    for i, bot_app in enumerate(bot_apps):
        try:
            bot_user = await bot_app.bot.get_me()
            await context.bot.promote_chat_member(
                chat_id=chat_id,
                user_id=bot_user.id,
                can_change_info=True,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True
            )
            results.append(f"Bot {i+1} ✅")
        except Exception as e:
            results.append(f"Bot {i+1} ❌ ({str(e)})")
    
    await update.message.reply_text("\n".join(results))

@only_sudo
async def fulladmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    results = []
    for i, bot_obj in enumerate(bots):
        try:
            bot_me = await bot_obj.get_me()
            await context.bot.promote_chat_member(
                chat_id=chat_id,
                user_id=bot_me.id,
                can_change_info=True,
                can_post_messages=True,
                can_edit_messages=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True
            )
            results.append(f"Bot {i+1} ✅")
        except Exception as e:
            results.append(f"Bot {i+1} ❌ ({str(e)})")
    
    await update.message.reply_text("\n".join(results))

@only_sudo
@only_sudo
async def recruit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        # Get the group link if possible, or use a placeholder if not
        chat = await context.bot.get_chat(chat_id)
        invite_link = chat.invite_link
        if not invite_link:
            invite_link = await context.bot.export_chat_invite_link(chat_id)
    except Exception as e:
        return await update.message.reply_text(f"❌ ᴄᴏᴜʟᴅ ɴᴏᴛ ɢᴇᴛ ɪɴᴠɪᴛᴇ ʟɪɴᴋ: {str(e)}")

    results = []
    for i, bot_obj in enumerate(bots):
        if bot_obj.token == context.bot.token:
            continue # Skip the bot that received the command
        try:
            # Most bots can't "join" via link via API directly, 
            # but we can try to force them to interact or the user can use the links provided
            bot_me = await bot_obj.get_me()
            results.append(f"Bot {i+1} (@{bot_me.username}): {invite_link}")
        except Exception as e:
            results.append(f"Bot {i+1} ❌ ({str(e)})")
    
    await update.message.reply_text("🔗 ᴊᴏɪɴ ʟɪɴᴋs ғᴏʀ ᴏᴛʜᴇʀ ʙᴏᴛs:\n" + "\n".join(results))

async def farewell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    results = []
    
    # 1. Cancel all tasks first
    if chat_id in group_tasks:
        for t in group_tasks[chat_id].values():
            t.cancel()
        group_tasks[chat_id] = {}
    if chat_id in repeat_tasks:
        for t in repeat_tasks[chat_id]:
            t.cancel()
        repeat_tasks[chat_id] = []
    if chat_id in pin_tasks:
        for t in pin_tasks[chat_id]:
            t.cancel()
        pin_tasks[chat_id] = []
        
    await update.message.reply_text("👋 ᴘʀᴇᴘᴀʀɪɴɢ ᴛᴏ ʟᴇᴀᴠᴇ...")

    # 2. Process each bot: Demote, Kick, Leave
    for i, bot_obj in enumerate(bots):
        try:
            bot_me = await bot_obj.get_me()
            # Demote from admin (using context bot since it needs admin rights to demote others)
            try:
                await context.bot.promote_chat_member(
                    chat_id=chat_id,
                    user_id=bot_me.id,
                    can_change_info=False,
                    can_post_messages=False,
                    can_edit_messages=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False,
                    can_manage_chat=False,
                    can_manage_video_chats=False
                )
            except:
                pass
            
            # Leave chat (bot leaves itself)
            await bot_obj.leave_chat(chat_id)
            results.append(f"Bot {i+1} ✅")
        except Exception as e:
            results.append(f"Bot {i+1} ❌ ({str(e)})")
            
    await update.message.reply_text("🧹 ᴇxɪᴛ sᴇǫᴜᴇɴᴄᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ:\n" + "\n".join(results))

async def arise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("𝐖ᴇʟᴄᴏᴍᴇ 𝐓ᴏ DEVA 𝐕2 𝐁ᴏᴛ 𝐃ᴏ /help 𝐅ᴏʀ 𝐂ᴏᴍᴍᴀɴᴅs 🌊")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "╔══════════════════════╗\n"
        "        .🪷 DEVA 𝐕4  Mᴇɴᴜ 🪷.\n"
        "╚══════════════════════╝\n\n"
        "🎀 𝗡𝗖 𝗠𝗢𝗗𝗘𝗦\n"
        "━━━━━━━━━━━━━━━\n"
        "➪ /nc <name>  \n"
        "➪ /emo <name> \n\n"
        "⛔ Stop Controls  \n"
        "➪ /freeze\n"
        "➪ /pause \n"
        "➪ /cease \n"
        "➪ /unpin \n\n"
        "😹 𝗦𝗣𝗔𝗠 𝗭𝗢𝗡𝗘\n"
        "━━━━━━━━━━━━━━━\n"
        "➪ /repeat [text]\n"
        "➪ /pin [text]\n\n"
        "🪼 𝗦𝗟𝗜𝗗𝗘 𝗠𝗢𝗗𝗘\n"
        "━━━━━━━━━━━━━━━\n"
        "➪ /aim [reply]\n"
        "➪ /slide [reply]\n"
        "➪ /swipe [name]\n\n"
        "⚡ 𝗦𝗟𝗜𝗗𝗘 𝗦𝗧𝗢𝗣\n"
        "━━━━━━━━━━━━━━━\n"
        "➪ /hold \n"
        "➪ /halt\n"
        "➪ /still\n\n"
        "🦚 𝐓ᴏ 𝐃ᴏ \n"
        "━━━━━━━━━━━━━━━\n"
        "➪ /refresh\n"
        "➪ /fulladmin \n"
        "➪ /farewell\n\n"
        "╔══════════════════════╗\n"
        "      .🔱DEVA 𝐕4 𝐇ᴇʟᴘ 𝐌ᴇɴᴜ🔱.\n"
        "╚══════════════════════╝"
    )
    await update.message.reply_text(help_text)

async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    msg = await update.message.reply_text("🏓 Checking...")
    end = time.time()
    await msg.edit_text(f"ᴀʟʟ sᴇᴛ ✅ {int((end-start)*1000)} ms")

async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Your ID: {update.effective_user.id}")

@only_sudo
async def nc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("ᴜsᴇ: /nc <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    
    async def sequential_nc():
        for bot in bots:
            if bot.id not in group_tasks[chat_id]:
                task = asyncio.create_task(bot_loop(bot, chat_id, base, "raid"))
                group_tasks[chat_id][bot.id] = task
                await asyncio.sleep(0.01)

    asyncio.create_task(sequential_nc())
    await update.message.reply_text("🔄 𝐃ᴏɴᴇ ")

@only_sudo
async def emo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ ᴍᴀsᴛᴇʀ ᴜsᴇ: /emo <text>")
    base = " ".join(context.args)
    chat_id = update.message.chat_id
    group_tasks.setdefault(chat_id, {})
    
    async def sequential_emo():
        for bot in bots:
            if bot.id not in group_tasks[chat_id]:
                task = asyncio.create_task(bot_loop(bot, chat_id, base, "emoji"))
                group_tasks[chat_id][bot.id] = task
                await asyncio.sleep(0.01)

    asyncio.create_task(sequential_emo())
    await update.message.reply_text("started")

@only_sudo
async def pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in group_tasks:
        for task in group_tasks[chat_id].values():
            task.cancel()
        group_tasks[chat_id] = {}
        await update.message.reply_text("⏸️ ᴀᴛᴛᴀᴄᴋ ᴘᴀᴜsᴇᴅ… ᴀs ᴄᴏᴍᴍᴀɴᴅᴇᴅ.")

@only_sudo
async def freeze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for chat_id, bot_tasks in list(group_tasks.items()):
        for t in bot_tasks.values():
            t.cancel()
        group_tasks[chat_id] = {}
    for chat_id, tasks in list(repeat_tasks.items()):
        for t in tasks:
            t.cancel()
        repeat_tasks[chat_id] = []
    await update.message.reply_text("❄️ ᴇᴠᴇʀʏᴛʜɪɴɢ's ғʀᴏᴢᴇɴ ғᴏʀ ɴᴏᴡ")

@only_sudo
async def set_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    if not context.args:
        return await update.message.reply_text(f"⏱ Current delay: {delay}s")
    try:
        delay = max(0.1, float(context.args[0]))
        await update.message.reply_text(f"✅ Delay set to {delay}ms")
    except:
        await update.message.reply_text("⚠️ Invalid number.")

@only_sudo
async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 Active Loops:\n"
    for chat_id, tasks in group_tasks.items():
        msg += f"Chat {chat_id}: {len(tasks)} bots running\n"
    await update.message.reply_text(msg)

@only_owner
async def sudoadd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            uid = int(context.args[0])
            SUDO_USERS.add(uid)
            save_sudo()
            await update.message.reply_text(f"✅ {uid} ɪs ᴇɴᴛʀᴜsᴛᴇᴅ.")
        except ValueError:
            await update.message.reply_text("⚠️ Invalid User ID.")
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        SUDO_USERS.add(uid)
        save_sudo()
        await update.message.reply_text(f"✅ {uid} ɪs ᴇɴᴛʀᴜsᴛᴇᴅ.")

@only_owner
async def sudorem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            uid = int(context.args[0])
            if uid in SUDO_USERS:
                SUDO_USERS.remove(uid)
                save_sudo()
                await update.message.reply_text(f"🗑 {uid} ɪs ᴅɪsᴛʀᴜsᴛᴇᴅ")
        except ValueError:
            await update.message.reply_text("⚠️ Invalid User ID.")
    elif update.message.reply_to_message:
        uid = update.message.reply_to_message.from_user.id
        if uid in SUDO_USERS:
            SUDO_USERS.remove(uid)
            save_sudo()
            await update.message.reply_text(f"🗑 {uid} ɪs ᴅɪsᴛʀᴜsᴛᴇᴅ")

@only_sudo
async def monarchs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 ᴍᴏɴᴀʀᴄʜs:\n" + "\n".join(map(str, SUDO_USERS)))

@only_sudo
async def aim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slide_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🎯 ᴛᴀʀɢᴇᴛ ɪᴅᴇɴᴛɪғɪᴇᴅ")

@only_sudo
async def hold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slide_targets.discard(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🛑 ᴛᴀʀɢᴇᴛ ᴍᴀʀᴋᴇᴅ ɴᴏ ʟᴏɴɢᴇʀ")

@only_sudo
async def slide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("ᴛʜᴇ sʟɪᴅᴇ ʜᴀs ʙᴇɢᴀɴ")

@only_sudo
async def halt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        slidespam_targets.discard(update.message.reply_to_message.from_user.id)
        await update.message.reply_text("🛑 sʟɪᴅᴇ ʜᴀs ʙᴇᴇɴ sᴛᴏᴘᴘᴇᴅ")

@only_sudo
async def swipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ ᴍᴀsᴛᴇʀ ᴜsᴇ: /swipe <name>")
    swipe_mode[update.message.chat_id] = " ".join(context.args)
    await update.message.reply_text(f"⚡ Swipe mode ON with name: {swipe_mode[update.message.chat_id]}")

@only_sudo
async def still(update: Update, context: ContextTypes.DEFAULT_TYPE):
    swipe_mode.pop(update.message.chat_id, None)
    await update.message.reply_text("🛑 Swipe mode stopped.")

@only_sudo
async def repeat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ ᴍᴀsᴛᴇʀ ᴜsᴇ: /repeat <text>")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    repeat_tasks.setdefault(chat_id, [])
    for bot in bots:
        task = asyncio.create_task(repeat_loop(bot, chat_id, text))
        repeat_tasks[chat_id].append(task)
    await update.message.reply_text("🔁 ʀᴇᴘᴇᴛɪᴛɪᴏɴ ɪɴɪᴛɪᴀᴛᴇᴅ")

@only_sudo
async def cease(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in repeat_tasks:
        for task in repeat_tasks[chat_id]:
            task.cancel()
        repeat_tasks[chat_id] = []
        await update.message.reply_text("🛑 ʀᴇᴘᴇᴛɪᴛɪᴏɴ  ʜᴀs ʙᴇᴇɴ sᴛᴏᴘᴘᴇᴅ")

@only_sudo
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("⚠️ ᴍᴀsᴛᴇʀ ᴜsᴇ: /pin <message>")
    text = " ".join(context.args)
    chat_id = update.message.chat_id
    pin_tasks.setdefault(chat_id, [])
    for bot in bots:
        task = asyncio.create_task(pin_loop(bot, chat_id, text))
        pin_tasks[chat_id].append(task)
    await update.message.reply_text("📌 ᴘɪɴ ʟᴏᴏᴘ sᴛᴀʀᴛᴇᴅ - ᴀʟʟ ᴍᴇssᴀɢᴇs ᴡɪʟʟ ʙᴇ ᴘɪɴɴᴇᴅ")

@only_sudo
async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in pin_tasks:
        for task in pin_tasks[chat_id]:
            task.cancel()
        pin_tasks[chat_id] = []
        await update.message.reply_text("🛑 ᴘɪɴ ʟᴏᴏᴘ sᴛᴏᴘᴘᴇᴅ")

async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid, chat_id = update.message.from_user.id, update.message.chat_id
    if uid in slide_targets:
        for text in RAID_TEXTS:
            await update.message.reply_text(text)
    if uid in slidespam_targets:
        for text in RAID_TEXTS:
            await update.message.reply_text(text)
    if chat_id in swipe_mode:
        for text in RAID_TEXTS:
            await update.message.reply_text(f"{swipe_mode[chat_id]} {text}")

def build_app(token):
    telegram_app = Application.builder().token(token).build()
    telegram_app.add_handler(CommandHandler("arise", arise))
    telegram_app.add_handler(CommandHandler("fulladmin", fulladmin))
    telegram_app.add_handler(CommandHandler("farewell", farewell))
    telegram_app.add_handler(CommandHandler("recruit", recruit))
    telegram_app.add_handler(CommandHandler("help", help_cmd))
    telegram_app.add_handler(CommandHandler("refresh", refresh))
    telegram_app.add_handler(CommandHandler("me", me))
    telegram_app.add_handler(CommandHandler("nc", nc))
    telegram_app.add_handler(CommandHandler("emo", emo))
    telegram_app.add_handler(CommandHandler("pause", pause))
    telegram_app.add_handler(CommandHandler("freeze", freeze))
    telegram_app.add_handler(CommandHandler("set", set_delay))
    telegram_app.add_handler(CommandHandler("status", status_cmd))
    telegram_app.add_handler(CommandHandler("sudoadd", sudoadd))
    telegram_app.add_handler(CommandHandler("sudorem", sudorem))
    telegram_app.add_handler(CommandHandler("monarchs", monarchs))
    telegram_app.add_handler(CommandHandler("aim", aim))
    telegram_app.add_handler(CommandHandler("hold", hold))
    telegram_app.add_handler(CommandHandler("slide", slide))
    telegram_app.add_handler(CommandHandler("halt", halt))
    telegram_app.add_handler(CommandHandler("swipe", swipe))
    telegram_app.add_handler(CommandHandler("still", still))
    telegram_app.add_handler(CommandHandler("repeat", repeat))
    telegram_app.add_handler(CommandHandler("cease", cease))
    telegram_app.add_handler(CommandHandler("pin", pin))
    telegram_app.add_handler(CommandHandler("unpin", unpin))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies))
    return telegram_app

async def run_all_bots():
    global apps, bots
    for token in TOKENS:
        if token.strip():
            try:
                telegram_app = build_app(token)
                apps.append(telegram_app)
                bots.append(telegram_app.bot)
            except Exception as e:
                print("Failed building app:", e)

    for telegram_app in apps:
        try:
            await telegram_app.initialize()
            await telegram_app.start()
            await telegram_app.updater.start_polling()
        except Exception as e:
            print("Failed starting app:", e)

    print("Bot is running...")
    await asyncio.Event().wait()

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_all_bots())

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
