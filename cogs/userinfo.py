import discord
from discord.ext import commands
import utils.default


class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user(self, ctx, *, user: discord.Member = None):
      """ Get user information """
      user = user or ctx.author

      show_roles = ', '.join([
          f"<@&{x.id}>"
          for x in sorted(
              user.roles,
              key=lambda x: x.position,
              reverse=True
            )

          if x.id != ctx.guild.default_role.id
          ]) if len(user.roles) > 1 else 'None'


      embed = discord.Embed(
          colour=user.top_role.colour.value
        )
      embed.set_thumbnail(
          url=user.avatar_url
        )
      embed.add_field(
          name="Full name",
          value=user,
          inline=True
        )
      embed.add_field(
          name="Nickname",
          value=user.nick if hasattr(user, "nick") else "None",
          inline=True
        )
      embed.add_field(
          name="Account created",
          value=utils.default.date(user.created_at),
          inline=True
        )
      embed.add_field(
          name="Joined this server",
          value=utils.default.date(user.joined_at),
          inline=True
        )

      embed.add_field(
          name="Roles", value=show_roles, inline=False
        )

      await ctx.send(
          content=f"About **{user.id}**",
          embed=embed
        )


    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """ Get the avatar of you or someone else """
        user = user or ctx.author
        await ctx.send(f"Avatar to **{user.name}**\n{user.avatar_url_as(size=1024)}")

def setup(bot):
    bot.add_cog(UserInfo(bot))
