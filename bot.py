from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from solana.rpc.api import Client
import random
import string
import config

# Solana client
solana = Client(config.SOLANA_RPC)

# Temporary in-memory user storage
users = {}

def generate_wallet():
    # Demo wallet generator (public address only)
    return "SoL" + "".join(random.choices(string.ascii_letters + string.digits, k=36))

def get_balance(address):
    try:
        result = solana.get_balance(address)
        return result.value / 1_000_000_000
    except:
        return 0.0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        users[user_id] = {
            "wallet": generate_wallet()
        }

    wallet = users[user_id]["wallet"]
    balance = get_balance(wallet)

    if balance < config.MIN_DEPOSIT_SOL:
        message = (
            "🚀 *Photon Trading Bot*\n\n"
            "🔒 *Trading Locked*\n\n"
            f"💰 Balance: `{balance:.4f} SOL`\n"
            f"📌 Minimum deposit: `{config.MIN_DEPOSIT_SOL} SOL`\n\n"
            "➡️ Deposit SOL to activate trading:\n"
            f"`{wallet}`\n\n"
            "After deposit, tap /start again."
        )
    else:
        message = (
            "✅ *Bot Activated*\n\n"
            f"💰 Balance: `{balance:.4f} SOL`\n\n"
            "📊 Trading features unlocked."
        )

    await update.message.reply_text(message, parse_mode="Markdown")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        await update.message.reply_text("❌ Please start the bot first: /start")
        return

    wallet = users[user_id]["wallet"]
    balance = get_balance(wallet)

    if balance < config.MIN_DEPOSIT_SOL:
        await update.message.reply_text(
            "🔒 Trading locked.\nPlease deposit SOL to continue."
        )
        return

    await update.message.reply_text("📊 Trading module coming soon…")

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trade", trade))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
