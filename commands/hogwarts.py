import discord
from discord.ext import commands

class HarryPotter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.add_role_triggers = [
            "I solemnly swear that I'm up to no good",
            "I solemnly swear that I am up to no good",
            "I solemnly swear that I'm upto no good",
            "I solemnly swear that I am upto no good"
        ]
        self.remove_role_trigger = "mischief managed"
        self.role_id = 1320302009295048734 

    @commands.Cog.listener()
    async def on_message(self, message):        
        if message.author.bot:
            return

        try:
            role = message.guild.get_role(self.role_id)
            if not role:
                await message.channel.send(
                    f"Padfoot forgot to create the role.", delete_after=3
                )
                await message.delete()
                return

            message_content = message.content.strip().lower()

            if message_content in (trigger.lower() for trigger in self.add_role_triggers):
                if role in message.author.roles:
                    await message.delete()
                    return
                await message.author.add_roles(role)
                await message.channel.send(
                    f"{message.author.mention}[.](https://tenor.com/view/harry-potter-hp-hogwarts-ticket-hogwarts-gif-25730828)", delete_after=5
                )
                await message.delete()

            elif message_content == self.remove_role_trigger.lower():
                if role not in message.author.roles:
                    await message.delete()
                    return
                await message.author.remove_roles(role)
                await message.delete()
        
        except discord.Forbidden:
            await message.channel.send(
                "Master, would you allow this house-elf to manage roles?", delete_after=3
            )
            await message.delete()
        except discord.HTTPException as e:
            await message.channel.send(str(e), delete_after=3)
            await message.delete()
        except Exception as e:
            await message.channel.send(str(e), delete_after=3)
            await message.delete()

async def setup(bot):
    await bot.add_cog(HarryPotter(bot))
