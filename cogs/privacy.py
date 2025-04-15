import nextcord
from nextcord import Interaction, Embed, Colour
from nextcord.ext import commands


class PrivacyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="privacy", description="Informationen zum Datenschutz und zur Datennutzung.")
    async def privacy(self, interaction: Interaction):
        embed = Embed(
            title="🔐 Datenschutz & Datennutzung",
            description=(
                "Dieser Bot nutzt offizielle Schnittstellen (z. B. Riot Games API), um öffentlich zugängliche Spielerinformationen zu verifizieren.\n\n"
                "**Welche Daten werden verarbeitet?**\n"
                "- Spielername (Riot ID)\n"
                "- Matchdaten (öffentlich über Riot API)\n"
                "- Aktueller Rank (öffentlich)\n\n"
                "**Was passiert mit den Daten?**\n"
                "- Keine Speicherung in Datenbanken\n"
                "- Keine Weitergabe an Dritte\n"
                "- Nur zur sofortigen Verifikation verwendet\n\n"
                "**Rechte & Kontrolle**\n"
                "- Nutzer können jederzeit ihre Daten löschen lassen (bald über `/delete`)\n\n"
                "**Weitere Infos:**\n"
                "Dieses Projekt erfüllt die Anforderungen der Riot Games Developer Terms und respektiert die Privatsphäre aller Nutzer."
            ),
            color=Colour.blue()
        )
        embed.set_footer(text="CelestixDCBot • Datenschutz zuerst")

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(PrivacyCog(bot))
