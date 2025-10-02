
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, MessageHandler, filters
import database
from config import CHANNEL_URL, CHANNEL_USERNAME, CAPTCHA_QUESTIONS
import random

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    
    database.add_user(user_id, username)
    
    user_data = database.get_user(user_id)
    if user_data and user_data[4]:
        await show_main_menu(update, context)
        return
    
    await show_welcome_message(update)

async def show_welcome_message(update: Update):
    welcome_text = f"""
✨ **مرحباً بك في بوت استلام حسابات التليجرام!** ✨

📢 **قناتنا الرسمية:**
{CHANNEL_USERNAME}

🌟 **مميزات البوت:**
✅ استلام حسابات تليجرام بجودة عالية
💰 أرباح يومية مضمونة  
🎁 عروض حصرية للمشتركين

👉 **للاستفادة من خدماتنا، يرجى الاشتراك في قناتنا أولاً:**
    """

    keyboard = [
        [InlineKeyboardButton("📢 الإنضمام للقناة", url=CHANNEL_URL)],
        [InlineKeyboardButton("🚀 بدء الاستخدام", callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        is_subscribed = member.status in ['member', 'administrator', 'creator']
    except:
        is_subscribed = False
    
    if is_subscribed:
        database.update_user_subscription(user_id, True)
        await send_captcha(query)
    else:
        error_text = f"""
❌ **لم يتم التحقق من اشتراكك!**

⚠️ **تأكد من:**
• الضغط على زر "الإنضمام للقناة"
• الانتظار حتى يتم تحميل القناة  
• الضغط على "تحقق مرة أخرى"

🔗 **رابط القناة:**
{CHANNEL_USERNAME}
        """
        
        keyboard = [
            [InlineKeyboardButton("📢 الإنضمام للقناة", url=CHANNEL_URL)],
            [InlineKeyboardButton("🔄 تحقق مرة أخرى", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(error_text, reply_markup=reply_markup, parse_mode='Markdown')

async def send_captcha(query):
    captcha = random.choice(CAPTCHA_QUESTIONS)
    user_id = query.from_user.id
    user_states[user_id] = captcha["answer"]
    
    captcha_text = f"""
🔐 **تحقق أمني**

{captcha['question']}

📝 **أرسل الإجابة في الشات:**
        """
    
    await query.edit_message_text(captcha_text, parse_mode='Markdown')

async def verify_captcha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answer = update.message.text.strip()
    
    if user_id in user_states:
        correct_answer = user_states[user_id]
        
        if user_answer == correct_answer:
            database.update_user_captcha(user_id, True)
            database.update_user_onboarding(user_id, True)
            del user_states[user_id]
            
            success_text = """
🎉 **تم التحقق بنجاح!** 🎉

✨ **مرحباً بك في عائلة البوت!**

📱 **الآن يمكنك إرسال رقم هاتفك:**

💡 **التنسيق المطلوب:**
`+20123456789`
`+966512345678`  
`+971501234567`

🔒 **ملاحظة:** سيتم مراجعة الحساب وإضافته خلال دقائق
            """
            
            await update.message.reply_text(success_text, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ **الإجابة خاطئة!**\n\nأعد إرسال الإجابة الصحيحة:")
    else:
        await update.message.reply_text("🔁 **اكتب /start لبدء من جديد**")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_states:
        await verify_captcha(update, context)
    else:
        text = update.message.text.strip()
        if text.startswith('+') and any(char.isdigit() for char in text[1:]):
            await handle_phone_number(update, context)
        else:
            await update.message.reply_text(
                "❌ **أرسل رقم الهاتف بالتنسيق الدولي**\n\n"
                "💡 **مثال:** `+20123456789`\n"
                "🔁 أو اكتب /start لبدء من جديد."
            )

async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text.strip()
    user_id = update.effective_user.id
    
    if len(phone_number) < 10:
        await update.message.reply_text(
            "❌ **رقم الهاتف غير صحيح!**\n\n"
            "🔍 **تأكد من كتابة الرقم مع المفتاح الدولي.**\n"
            "💡 **مثال:** `+20123456789`"
        )
        return
    
    await update.message.reply_text(
        f"✅ **تم استلام الرقم:** `{phone_number}`\n\n"
        "⏳ **جاري معالجة طلبك...**\n\n"
        "🔒 سيتم مراجعة الحساب وإضافته خلال دقائق.",
        parse_mode='Markdown'
    )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_text = """
🎊 **مرحباً بعودتك!** 🎊

📊 **اختر من القائمة:**
    """
    
    keyboard = [
        [InlineKeyboardButton("💰 رصيدي", callback_data="balance")],
        [InlineKeyboardButton("📱 إضافة حساب", callback_data="add_account")],
        [InlineKeyboardButton("💳 سحب الأرباح", callback_data="withdraw")],
        [InlineKeyboardButton("🌍 الدول المتاحة", callback_data="countries")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(update, 'message'):
        await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')

def setup_start_handlers(app):
    app.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
