bot = open('bot.py', 'w')
bot.write(
    'import logging\n'
    'from aiogram import Bot, Dispatcher, executor, types\n'
    
    '# Configure logging\n'
    'logging.basicConfig(level=logging.INFO)\n\n'

    '# Initialize bot and dispatcher\n'
    'bot = Bot(token=bot.TOKEN)\n'
    'dp = Dispatcher(bot)\n\n'

    '@dp.message_handler()\n'
    'async def echo(message: types.Message):\n'
    '   await message.answer(message.text)\n'
    '   if \'some\' in message.text:\n'
    '       await message.answer(message.text)\n\n'

    'if __name__ == \'__main__\':\n'
    '   executor.start_polling(dp, skip_updates=True)'
) 
bot.close()

filters = open('filters.py', 'w')
filters.write(
    '# Custom filters\n'
)
filters.close()

configs = open('configs.py', 'w')
configs.write(    
    'BOT_TOKEN = 00000000\n'
    'BOT_OWNER = 00000000'
)
configs.close()