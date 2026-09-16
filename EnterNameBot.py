import discord
from discord.ext import commands
import os

WELCOME_CHANNEL_ID = 1537428192057626696

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Ready as {bot.user} | members intent: {bot.intents.members}")

class NameModal(discord.ui.Modal, title="Set your name"):
    name = discord.ui.TextInput(label="Your name", max_length=32)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.user.edit(nick=str(self.name))
            await interaction.response.send_message(
                f"Done — you're now **{self.name}**.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I can't rename you — check my permissions.", ephemeral=True
            )


class NameButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Set my name", style=discord.ButtonStyle.primary)
    async def set_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal())


@bot.event
async def on_member_join(member: discord.Member):
    print(f"JOIN FIRED for {member} in guild {member.guild.id}")
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    print(f"Channel lookup: {channel}")
    if channel:
        await channel.send(
            f"Welcome {member.mention}! Click below to set your name.",
            view=NameButton(),
        )

bot.run(os.environ["DISCORD_TOKEN"])
