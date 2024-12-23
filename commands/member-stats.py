import discord
from discord.ext import commands, tasks
import yaml
import os

class MemberStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'settings.yaml'
        self.load_config()
        self.update_channel_name.start()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = {"channels": {}}
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f)

    @tasks.loop(minutes=10)
    async def update_channel_name(self):
        channel_id = self.config["channels"].get("memberstats")
        if channel_id:
            channel = self.bot.get_channel(int(channel_id))
            if channel:
                guild = channel.guild
                member_count = sum(1 for member in guild.members if not member.bot)
                await channel.edit(name=f'{member_count} members')

    @update_channel_name.before_loop
    async def before_update_channel_name(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(MemberStats(bot))
