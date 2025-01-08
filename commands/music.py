from typing import Optional, cast
import discord
from discord.ext import commands
import wavelink
import config

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        """Play a song with the given query."""
        if not ctx.guild:
            return

        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)

        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except discord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return

        player.autoplay = wavelink.AutoPlayMode.enabled

        # Lock the player to the current text channel
        if not hasattr(player, "home"):
            player.home = ctx.channel
        elif player.home != ctx.channel:
            await ctx.send(f"You can only play songs in {player.home.mention}.")
            return

        tracks = await wavelink.Playable.search(query)
        if not tracks:
            await ctx.send(f"Could not find any tracks for `{query}`.")
            return

        if isinstance(tracks, wavelink.Playlist):
            added = await player.queue.put_wait(tracks)
            await ctx.send(f"Added playlist **`{tracks.name}`** ({added} songs) to the queue.")
        else:
            track = tracks[0]
            await player.queue.put_wait(track)
            await ctx.send(f"Added **`{track.title}`** to the queue.")

        if not player.is_playing():
            await player.play(player.queue.get(), volume=30)

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """Skip the current song."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.skip(force=True)
        await ctx.message.add_reaction("\u2705")

    @commands.command()
    async def nightcore(self, ctx: commands.Context):
        """Set the filter to a nightcore style."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        filters = wavelink.Filters()
        filters.timescale.set(pitch=1.2, speed=1.2, rate=1)
        await player.set_filters(filters)
        await ctx.message.add_reaction("\u2705")

    @commands.command(name="toggle", aliases=["pause", "resume"])
    async def pause_resume(self, ctx: commands.Context):
        """Pause or resume the player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.pause(not player.paused)
        await ctx.message.add_reaction("\u2705")

    @commands.command()
    async def volume(self, ctx: commands.Context, value: int):
        """Change the volume of the player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.set_volume(value)
        await ctx.message.add_reaction("\u2705")

    @commands.command(aliases=["dc"])
    async def disconnect(self, ctx: commands.Context):
        """Disconnect the player."""
        player: wavelink.Player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            return

        await player.disconnect()
        await ctx.message.add_reaction("\u2705")


async def setup(bot):
    await bot.add_cog(Music(bot))
