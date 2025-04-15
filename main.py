import asyncio
import logging
import nextcord
from nextcord import Interaction, SlashOption, Embed, SelectOption, Colour
from nextcord.ext import commands
from nextcord.ui import View, Select
import os
import json
from dotenv import load_dotenv

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables (for TOKEN and GUILD_ID)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
if not GUILD_ID:
    raise ValueError("GUILD_ID ist nicht in der .env-Datei gesetzt!")
GUILD_ID = int(GUILD_ID)

EMOJI_CACHE = {}

DATA_FILE = "message_data.json"

# Role & Emoji Mapping
RANK_ROLE_MAPPING = {
    "Iron 1": 1353422873745948875,
    "Iron 2": 1353422888589332631,
    "Iron 3": 1353422891965747273,
    "Bronze 1": 1353422895581237370,
    "Bronze 2": 1353422899570282576,
    "Bronze 3": 1353422903361802260,
    "Silver 1": 1353422906876493884,
    "Silver 2": 1353422910215159859,
    "Silver 3": 1353422913587515436,
    "Gold 1": 1356679687681605663,
    "Gold 2": 1356679724838944819,
    "Gold 3": 1356679849808367752,
    "Platinum 1": 1356679862836002996,
    "Platinum 2": 1356679873040486553,
    "Platinum 3": 1356679883761385542,
    "Diamond 1": 1356679892242272306,
    "Diamond 2": 1356679928518672504,
    "Diamond 3": 1356679940082503882,
    "Ascendant 1": 1356679953772712069,
    "Ascendant 2": 1356679965453586726,
    "Ascendant 3": 1356679989889601667,
    "Immortal 1": 1356679998982848593,
    "Immortal 2": 1356680009401499705,
    "Immortal 3": 1356680021577699439,
    "Radiant": 1356680032856182814
}

RANK_EMOJI_MAPPING = {
    "Iron 1": 1357880382963449946,
    "Iron 2": 1357880385362727009,
    "Iron 3": 1357880584747352234,
    "Bronze 1": 1357880358460461168,
    "Bronze 2": 1357880360259686500,
    "Bronze 3": 1357880362264428794,
    "Silver 1": 1357880400566816969,
    "Silver 2": 1357880403456823296,
    "Silver 3": 1357880406908862464,
    "Gold 1": 1357880369348743399,
    "Gold 2": 1357880581295308930,
    "Gold 3": 1357880373136064542,
    "Platinum 1": 1357880390190366932,
    "Platinum 2": 1357880392912343251,
    "Platinum 3": 1357880396091490525,
    "Diamond 1": 1357880363665461348,
    "Diamond 2": 1357880365766938872,
    "Diamond 3": 1357880367805366534,
    "Ascendant 1": 1357880353687208240,
    "Ascendant 2": 1357880354966601784,
    "Ascendant 3": 1357880357172809798,
    "Immortal 1": 1357880375908761794,
    "Immortal 2": 1357880582935150608,
    "Immortal 3": 1357880380371238912,
    "Radiant": 1357880579307343872
}

intents = nextcord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

class RankSelect(Select):
    def __init__(self):
        options = []
        for rank in RANK_ROLE_MAPPING:
            emoji_id = RANK_EMOJI_MAPPING.get(rank)
            emoji = EMOJI_CACHE.get(emoji_id)
            options.append(
                SelectOption(
                    label=rank,
                    description=f"Rolle für {rank} wählen",
                    value=rank,
                    emoji=emoji
                )
            )
        super().__init__(placeholder="Wähle deinen Valorant Rang...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        chosen_rank = self.values[0]
        role_id = RANK_ROLE_MAPPING.get(chosen_rank)
        if not role_id:
            await interaction.response.send_message("Fehler: Rolle nicht gefunden.", ephemeral=True)
            return

        member = interaction.user
        roles_to_remove = [r for r in member.roles if r.id in RANK_ROLE_MAPPING.values()]
        for r in roles_to_remove:
            await member.remove_roles(r)

        new_role = interaction.guild.get_role(role_id)
        if new_role:
            await member.add_roles(new_role)

        emoji_id = RANK_EMOJI_MAPPING.get(chosen_rank)
        emoji = EMOJI_CACHE.get(emoji_id) or bot.get_emoji(emoji_id)
        emoji_preview = f"{emoji}" if emoji else ""
        await interaction.response.send_message(
            f"Du hast jetzt die Rolle **{chosen_rank}** {emoji_preview} erhalten.",
            ephemeral=True
        )

class RankSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RankSelect())

def save_message_id(message_id):
    with open(DATA_FILE, "w") as file:
        json.dump({"message_id": message_id}, file)

def load_message_id():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return data.get("message_id")
    return None

@bot.slash_command(
    name="setup_rank_verification",
    description="Postet das Valorant Rang-Auswahl-Embed",
    guild_ids=[GUILD_ID]
)
async def setup_rank_verification(
    interaction: Interaction,
    channel_id: int = SlashOption(description="Channel-ID für das Embed")
):
    try:
        channel = interaction.guild.get_channel(int(channel_id))
        if not channel:
            await interaction.response.send_message("Channel nicht gefunden.", ephemeral=True)
            return

        embed = Embed(
            title="Valorant Rang-System",
            description=(
                "Wähle deinen aktuellen Rang aus dem Dropdown-Menü unten.\n"
                "Der Bot wird dir automatisch die passende Rolle zuweisen.\n\n"
                "## Wichtige Information:\n"
                "Du kannst deine Rolle jederzeit ändern, indem du erneut auswählst.\n"
                "### Hinweis:\n"
                "Sei bitte ehrlich und wähle nur den Rank aus, den du derzeit hast."
            ),
            color=Colour.dark_red()
        )
        embed.set_thumbnail(url="https://raw.githubusercontent.com/cakeLinir/CelestixDCBot/master/pictures/Celestix_Transparent.png")
        embed.set_image(url="https://raw.githubusercontent.com/cakeLinir/CelestixDCBot/master/pictures/Valorant_Rank_%C3%BCbersicht.png")
        embed.set_footer(text="Celestix Rank System • Valorant Edition • Beta v1.0")

        message = await channel.send(embed=embed, view=RankSelectView())
        save_message_id(message.id)
        await interaction.response.send_message("Setup erfolgreich abgeschlossen!", ephemeral=True)

    except Exception as e:
        await interaction.response.send_message(f"Fehler beim Setup: {e}", ephemeral=True)

# --- on_ready: Emoji Cache + View Restore + Cog Load ---
@bot.event
async def on_ready():
    global EMOJI_CACHE
    logging.info(f"✅ Bot ist eingeloggt als {bot.user}")
    guild = bot.get_guild(GUILD_ID)

    if guild:
        EMOJI_CACHE = {e.id: e for e in guild.emojis}
        logging.info(f"📦 {len(EMOJI_CACHE)} benutzerdefinierte Emojis gecached.")

        # Cogs laden
        loaded = getattr(bot, "_cogs_loaded", False)
        if not loaded:
            try:
                bot.load_extension("cogs.privacy")
                bot._cogs_loaded = True
                logging.info("🔧 Datenschutz-Cog erfolgreich geladen.")
            except Exception as e:
                logging.error(f"❌ Fehler beim Laden der Datenschutz-Cog: {e}")

        # View wiederherstellen
        message_id = load_message_id()
        if message_id:
            for channel in guild.text_channels:
                try:
                    message = await channel.fetch_message(message_id)
                    await message.edit(view=RankSelectView())
                    logging.info(f"🔄 View für Nachricht {message_id} wurde wiederhergestellt!")
                    break
                except nextcord.NotFound:
                    continue
    else:
        logging.warning("⚠ GUILD_ID nicht gefunden oder Bot ist nicht auf dem Server.")

@bot.event
async def on_connect():
    await bot.sync_all_application_commands()
    logging.info("✅ Slash Commands synchronisiert.")


# Bot starten
if __name__ == "__main__":
    async def main():
        await bot.start(TOKEN)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot wird heruntergefahren...")
