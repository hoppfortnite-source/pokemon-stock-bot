import discord
from discord.ext import commands, tasks
import aiohttp
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

FORT_MYERS_ZIP = "33901"

STORES = {
    "walmart": "Walmart",
    "target": "Target",
    "bestbuy": "Best Buy",
    "gamestop": "GameStop"
}

WALMART_POKEMON_URLS = [
    ("Booster Boxes", "https://www.walmart.com/search?q=pokemon+booster+box&store={}"),
    ("Elite Trainer Boxes", "https://www.walmart.com/search?q=pokemon+elite+trainer+box&store={}"),
    ("Booster Bundles", "https://www.walmart.com/search?q=pokemon+booster+bundle&store={}"),
    ("Tins & Collections", "https://www.walmart.com/search?q=pokemon+tin+collection&store={}")
]

async def check_walmart():
    results = []
    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.walmart.com/search?q=pokemon+cards&zip={FORT_MYERS_ZIP}"
        try:
            async with session.get(url, headers=headers, timeout=10) as r:
                if r.status == 200:
                    results.append("✅ Walmart online: Check walmart.com/search?q=pokemon+cards")
                else:
                    results.append("❌ Walmart: Could not reach site")
        except:
            results.append("❌ Walmart: Request failed")
    return results

async def check_target():
    results = []
    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.target.com/s?searchTerm=pokemon+cards&zipcode={FORT_MYERS_ZIP}"
        try:
            async with session.get(url, headers=headers, timeout=10) as r:
                if r.status == 200:
                    results.append("✅ Target online: Check target.com/s?searchTerm=pokemon+cards")
                else:
                    results.append("❌ Target: Could not reach site")
        except:
            results.append("❌ Target: Request failed")
    return results

async def check_bestbuy():
    results = []
    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards&zipcode={FORT_MYERS_ZIP}"
        try:
            async with session.get(url, headers=headers, timeout=10) as r:
                if r.status == 200:
                    results.append("✅ Best Buy online: Check bestbuy.com for pokemon cards")
                else:
                    results.append("❌ Best Buy: Could not reach site")
        except:
            results.append("❌ Best Buy: Request failed")
    return results

async def check_gamestop():
    results = []
    async with aiohttp.ClientSession() as session:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://www.gamestop.com/search#q=pokemon+cards&t=product"
        try:
            async with session.get(url, headers=headers, timeout=10) as r:
                if r.status == 200:
                    results.append("✅ GameStop online: Check gamestop.com for pokemon cards")
                else:
                    results.append("❌ GameStop: Could not reach site")
        except:
            results.append("❌ GameStop: Request failed")
    return results

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')
    await bot.tree.sync()
    auto_check.start()

class StoreSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Walmart", value="walmart", emoji="🛒"),
            discord.SelectOption(label="Target", value="target", emoji="🎯"),
            discord.SelectOption(label="Best Buy", value="bestbuy", emoji="💙"),
            discord.SelectOption(label="GameStop", value="gamestop", emoji="🎮"),
            discord.SelectOption(label="All Stores", value="all", emoji="🔍"),
        ]
        super().__init__(placeholder="Choose a store to check...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        store = self.values[0]
        embed = discord.Embed(title="🎴 Pokemon Stock Check", color=0xFFCC00)
        embed.set_footer(text=f"Fort Myers, FL {FORT_MYERS_ZIP}")

        results = []
        if store in ("walmart", "all"):
            results += await check_walmart()
        if store in ("target", "all"):
            results += await check_target()
        if store in ("bestbuy", "all"):
            results += await check_bestbuy()
        if store in ("gamestop", "all"):
            results += await check_gamestop()

        embed.description = "\n".join(results) if results else "No results found."
        embed.add_field(
            name="📦 Products to look for",
            value="• Booster Boxes\n• Elite Trainer Boxes\n• Booster Bundles\n• Tins & Collections",
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
        super().__init__(timeout=60)
        self.add_item(StoreSelect())

@bot.tree.command(name="pokemon", description="Check Pokemon card stock at Fort Myers stores")
async def pokemon(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎴 Pokemon Stock Checker",
        description="Select a store below to check Pokemon card availability in Fort Myers!",
        color=0xFFCC00
    )
    await interaction.response.send_message(embed=embed, view=StoreView())

@bot.tree.command(name="checkall", description="Check all stores at once")
async def checkall(interaction: discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="🎴 Pokemon Stock - All Stores", color=0xFFCC00)
    embed.set_footer(text=f"Fort Myers, FL {FORT_MYERS_ZIP}")
    all_results = []
    all_results += await check_walmart()
    all_results += await check_target()
    all_results += await check_bestbuy()
    all_results += await check_gamestop()
    embed.description = "\n".join(all_results)
    embed.add_field(
        name="🔗 Quick Links",
        value="[Walmart](https://www.walmart.com/search?q=pokemon+cards) | [Target](https://www.target.com/s?searchTerm=pokemon+cards) | [Best Buy](https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards) | [GameStop](https://www.gamestop.com/search#q=pokemon+cards)",
        inline=False
    )
    await interaction.followup.send(embed=embed)

@tasks.loop(minutes=30)
async def auto_check():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name == "pokemon-stock" or channel.name == "general":
                embed = discord.Embed(
                    title="🔔 Auto Pokemon Stock Check",
                    description="Use `/pokemon` to check a specific store or `/checkall` for all stores!",
                    color=0xFFCC00
                )
                embed.add_field(
                    name="🔗 Quick Links",
                    value="[Walmart](https://www.walmart.com/search?q=pokemon+cards) | [Target](https://www.target.com/s?searchTerm=pokemon+cards) | [Best Buy](https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards) | [GameStop](https://www.gamestop.com/search#q=pokemon+cards)",
                    inline=False
                )
                await channel.send(embed=embed)
                break

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
