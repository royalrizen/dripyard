import discord
from discord.ext import commands
import subprocess
import textwrap
from utils.staff import is_dev

class Terminal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.terminal_sessions = {}

    @commands.command(name="terminal", aliases=["t"], usage="-q (optional)", description="Starts a terminal session")
    @commands.check(is_dev)
    async def terminal(self, ctx, *, args=None):
        user_id = ctx.author.id

        if args == "-q":
            if user_id in self.terminal_sessions:
                del self.terminal_sessions[user_id]
                await ctx.send("Terminal session ended.")
            else:
                await ctx.send("You don't have an active terminal session.")
            return

        if user_id not in self.terminal_sessions:
            self.terminal_sessions[user_id] = True
            await ctx.send("Terminal session started. Type commands, or `!terminal -q` to quit.")
        else:
            await ctx.send("You already have an active terminal session.")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        user_id = message.author.id

        if user_id in self.terminal_sessions:
            if message.content.startswith("!terminal"):
                return
            
            try:
                result = subprocess.run(
                    message.content,
                    shell=True,
                    capture_output=True,
                    text=True
                )

                output = result.stdout or result.stderr or "Command executed, but no output."

                chunks = textwrap.wrap(output, width=2000)

                for i, chunk in enumerate(chunks):
                    embed = discord.Embed(
                        title=f"Terminal Output (Part {i + 1}/{len(chunks)})" if len(chunks) > 1 else "Terminal Output",
                        description=f"```{chunk}```",
                        color=0x27272f
                    )
                    await message.channel.send(embed=embed)

            except Exception as e:
                embed = discord.Embed(
                    title="Error",
                    description=e,
                    color=discord.Color.red()
                )
                await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Terminal(bot))
