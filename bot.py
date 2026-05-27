import discord
from discord.ext import tasks
import aiohttp
import os

bot = discord.Bot()
FORT_MYERS_ZIP = "33901"

async def check_store(session, name, url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
            if r.status == 200:
                return f"✅ **{name}** — Site reachable, check link below"
            else:
                return f"⚠️ **{name}** — Status {r.status}"
    except Exception as e:
        return f"❌ **{name}** — Failed to reach"

class StoreSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Walmart", value="walmart", emoji="🛒"),
            discord.SelectOption(label="Target", value="target", emoji="🎯"),
            discord.SelectOption(label="Best Buy", value="bestbuy", emoji="💙"),
            discord.SelectOption(label="GameStop", value="gamestop", emoji="🎮"),
            discord.SelectOption(label="All Stores", value="all", emoji="🔍"),
        ]
        super().__init__(placeholder="Pick a store to check...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        store = self.values[0]

        urls = {
            "walmart": ("Walmart", "https://www.walmart.com/search?q=pokemon+cards"),
            "target": ("Target", "https://www.target.com/s?searchTerm=pokemon+cards"),
            "bestbuy": ("Best Buy", "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards"),
            "gamestop": ("GameStop", "https://www.gamestop.com/search#q=pokemon+cards"),
        }

        to_check = urls.values() if store == "all" else [urls[store]]

        embed = discord.Embed(title="🎴 Pokemon Stock Check — Fort Myers FL", color=0xFFCC00)
        results = []
        async with aiohttp.ClientSession() as session:
            for name, url in to_check:
                result = await check_store(session, name, url)
                results.append(result)

        embed.description = "\n".join(results)
        embed.add_field(
            name="📦 Products",
            value="Booster Boxes • ETBs • Booster Bundles • Tins & Collections",
            inline=False
        )
        embed.add_field(
            name="🔗 Quick Links",
            value="[Walmart](https://www.walmart.com/search?q=pokemon+cards) | [Target](https://www.target.com/s?searchTerm=pokemon+cards) | [Best Buy](https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards) | [GameStop](https://www.gamestop.com/search#q=pokemon+cards)",
            inline=False
        )
        await interaction.followup.send(embed=embed)

class StoreView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(StoreSelect())

@bot.slash_command(name="pokemon", description="Check Pokemon stock at Fort Myers stores")
async def pokemon(ctx):
    embed = discord.Embed(
        title="🎴 Pokemon Stock Checker",
        description="Select a store to check Pokemon card availability in Fort Myers!",
        color=0xFFCC00
    )
    await ctx.respond(embed=embed, view=StoreView())

@bot.slash_command(name="checkall", description="Check all stores at once")
async def checkall(ctx):
    await ctx.defer()
    urls = {
        "Walmart": "https://www.walmart.com/search?q=pokemon+cards",
        "Target": "https://www.target.com/s?searchTerm=pokemon+cards",
        "Best Buy": "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards",
        "GameStop": "https://www.gamestop.com/search#q=pokemon+cards",
    }
    embed = discord.Embed(title="🎴 Pokemon Stock — All Stores", color=0xFFCC00)
    results = []
    async with aiohttp.ClientSession() as session:
        for name, url in urls.items():
            result = await check_store(session, name, url)
            results.append(result)
    embed.description = "\n".join(results)
    embed.add_field(
        name="🔗 Quick Links",
        value="[Walmart](https://www.walmart.com/search?q=pokemon+cards) | [Target](https://www.target.com/s?searchTerm=pokemon+cards) | [Best Buy](https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards) | [GameStop](https://www.gamestop.com/search#q=pokemon+cards)",
        inline=False
    )
    await ctx.followup.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)

