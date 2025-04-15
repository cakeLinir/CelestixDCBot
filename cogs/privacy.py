import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Embed, Colour

class PrivacyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="privacy", description="Informationen zum Datenschutz und zur Datennutzung")
    async def privacy(self, interaction: Interaction):
        embed = Embed(
            title="🔐 Datenschutz & Datennutzung",
            description=(
                "**Welche Daten werden verarbeitet?**\n"
                "- Riot ID (Spielername)\n"
                "- Öffentliche Matchdaten und Ranginfos\n\n"
                "**Was passiert mit den Daten?**\n"
                "- Keine Speicherung\n"
                "- Keine Weitergabe\n"
                "- Nur temporäre Nutzung zur Verifikation\n\n"
                "**Rechte & Kontrolle**\n"
                "- `/delete` wird folgen für Nutzerdaten-Anfragen\n\n"
                "⚖ Dieses Projekt entspricht den Riot Games Developer Terms."
            ),
            color=Colour.blue()
        )
        embed.set_footer(text="CelestixDCBot • Datenschutz zuerst")
        await interaction.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(PrivacyCog(bot))
