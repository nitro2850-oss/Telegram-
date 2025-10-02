from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start_handler import start, setup_start_handlers
import database
import config

def main():
    database.init_db()
    
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    setup_start_handlers(app)
    
    print("🚀 البوت اشتغل!")
    app.run_polling()

if __name__ == '__main__':
    main()
