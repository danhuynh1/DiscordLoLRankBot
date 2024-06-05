from discord import app_commands

import constants
import settings
import discord
from discord.ext import commands

from responses import get_response

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        logger.info(f"Guild ID: {bot.guilds[0].id}")
        # bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync()

    @bot.tree.command(description="Get lol rank", name="rank")
    @app_commands.choices(server=[
        app_commands.Choice(name="Brazil", value="NA"),
        app_commands.Choice(name="EU Nordic & East", value="EUNE"),
        app_commands.Choice(name="Europe West", value="EUW"),
        app_commands.Choice(name="Latin America North", value="LA1"),
        app_commands.Choice(name="Latin America South", value="LA2"),
        app_commands.Choice(name="North America", value="NA"),
        app_commands.Choice(name="Oceania", value="OCE"),
        app_commands.Choice(name="Russia", value="RU"),
        app_commands.Choice(name="Turkey", value="TR"),
        app_commands.Choice(name="Japan", value="JP"),
        app_commands.Choice(name="Korea", value="KR"),
        app_commands.Choice(name="Philippines", value="PH"),
        app_commands.Choice(name="Singapore, Malaysia, & Indonesia", value="SG"),
        app_commands.Choice(name="Taiwan", value="TW"),
        app_commands.Choice(name="Thailand", value="TH"),
        app_commands.Choice(name="Vietnam", value="VN"),
    ])
    @app_commands.describe(queue_type="Queue Type")
    @app_commands.choices(queue_type=[
        app_commands.Choice(name="Solo", value=('ranked_solo')),
        app_commands.Choice(name="Flex", value=('ranked_flex'))
    ])
    @app_commands.describe(riot_id="Riot ID")
    @app_commands.rename(riot_id="id")
    @app_commands.describe(tag_line="Tagline")
    @app_commands.rename(tag_line="tag")
    async def color(interaction: discord.Interaction, riot_id: str, tag_line: str, queue_type: app_commands.Choice[str],
                    server: app_commands.Choice[str]):
        response = get_response(riot_id, tag_line, queue_type.value, server.value)

        await interaction.response.send_message(f"{interaction.user.mention} {response}", ephemeral=False)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
