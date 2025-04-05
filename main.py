import nextcord
from nextcord import Interaction, SlashOption, Embed, SelectOption, Colour
from nextcord.ext import commands
from nextcord.ui import View, Select
import os
import json
from dotenv import load_dotenv

# Load environment variables (for TOKEN and GUILD_ID)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
if not GUILD_ID:
    raise ValueError("GUILD_ID ist nicht in der .env-Datei gesetzt!")
GUILD_ID = int(GUILD_ID)

DATA_FILE = "message_data.json"  # Datei für gespeicherte Message-ID

# Rank to Role ID mapping
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

intents = nextcord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

class RankSelect(Select):
    def __init__(self):
        options = [
            SelectOption(label=rank, description=f"Rolle für {rank} wählen", value=rank)
            for rank in RANK_ROLE_MAPPING
        ]
        super().__init__(
            placeholder="Wähle deinen Valorant Rang...",
            min_values=1,
            max_values=1,
            options=options,
        )

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
        await member.add_roles(new_role)
        await interaction.response.send_message(f"Du hast jetzt die Rolle **{chosen_rank}** erhalten.", ephemeral=True)

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
    channel_id: str = SlashOption(description="Channel-ID für das Embed")
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

@bot.event
async def on_ready():
    print(f"✅ Bot ist eingeloggt als {bot.user}")

    message_id = load_message_id()
    if message_id:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print("⚠ GUILD_ID nicht gefunden. Ist der Bot auf dem Server?")
            return
        for channel in guild.text_channels:
            try:
                message = await channel.fetch_message(message_id)
                if message:
                    await message.edit(view=RankSelectView())
                    print(f"🔄 View für Nachricht {message_id} wurde wiederhergestellt!")
                    break
            except nextcord.NotFound:
                continue
    else:
        print("⚠ Keine gespeicherte Message-ID gefunden. Bitte `/setup_rank_verification` erneut ausführen.")

bot.run(TOKEN)