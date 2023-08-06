config = open('config.py', 'w')
config.write(
    'TOKEN = \'<bot_token>\'\n'
    'ID = <bot_id>\n'
    'PREFIX = \'<bot_prefix>\'\n'
    'OWNER = \'<bot_owner>\''
) 
config.close()

bot = open('bot.py', 'w')
bot.write(
    'import discord\n'
    'from discord.ext import commands\n'
    'import config\n'
    'import modules\n\n'

    'bot = commands.Bot(command_prefix=congig.PREFIX\n\n'

    '# other code\n\n'

    'bot.run(config.TOKEN)'
)

modules = open('modules.py', 'w')
modules.write('# additional functions')
modules.close()

filters = open('filters.py', 'w')
filters.write('# custom filters')
filters.close()