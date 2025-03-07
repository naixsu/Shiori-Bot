from discord import Message
from discord.ext import commands
from helpers.responses import send_message

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhooks_cache = {}

    @commands.Cog.listener()
    async def on_message(self, ctx:Message):
        print("on_message", ctx)
        # print("author", ctx.author)
        print("Content", ctx.content)

        if ctx.author.bot:
            return

        if ctx.content.__contains__('$test') and not ctx.content.__contains__('`$test`'):
            content = ctx.content.replace("$test", "This is a test")

            await send_message(ctx, content)

async def setup(bot):
    await bot.add_cog(Test(bot))
