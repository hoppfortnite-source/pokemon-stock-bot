import discord
from discord.ext import commands
import aiohttp
import os
import re

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

STORES = {
    "target": [
        {"id": "t1", "name": "Target — Dynasty Dr", "address": "9350 Dynasty Dr, Fort Myers, FL 33905", "phone": "(239) 265-9022", "hours": "Mon-Sat 8AM-10/11PM, Sun 8AM-10PM", "search_url": "https://www.target.com/s?searchTerm=pokemon+cards&storeId=1267"},
        {"id": "t2", "name": "Target — S Tamiami Trl", "address": "13711 S Tamiami Trl, Fort Myers, FL 33912", "phone": "(239) 481-8860", "hours": "Mon-Sat 7AM-11PM, Sun 7AM-10PM", "search_url": "https://www.target.com/s?searchTerm=pokemon+cards&storeId=2696"},
        {"id": "t3", "name": "Target — Gulf Center Dr ⭐", "address": "10000 Gulf Center Dr, Fort Myers, FL 33913", "phone": "(239) 432-2641", "hours": "Mon-Sat 7AM-11PM, Sun 7AM-10PM", "search_url": "https://www.target.com/s?searchTerm=pokemon+cards&storeId=1268"},
        {"id": "t4", "name": "Target — San Carlos Blvd", "address": "15880 San Carlos Blvd, Fort Myers, FL 33908", "phone": "(239) 265-9002", "hours": "Daily 7AM-10PM", "search_url": "https://www.target.com/s?searchTerm=pokemon+cards&storeId=2354"},
    ],
    "walmart": [
        {"id": "w1", "name": "Walmart — Colonial Blvd", "address": "4770 Colonial Blvd, Fort Myers, FL 33966", "phone": "(239) 274-2920", "hours": "Daily 6AM-11PM", "search_url": "https://www.walmart.com/search?q=pokemon+cards&stores=2924"},
        {"id": "w2", "name": "Walmart — Six Mile Cypress ⭐", "address": "14821 Six Mile Cypress Pkwy, Fort Myers, FL 33912", "phone": "(239) 437-1880", "hours": "Daily 6AM-11PM", "search_url": "https://www.walmart.com/search?q=pokemon+cards&stores=3483"},
        {"id": "w3", "name": "Walmart — Pine Island Rd", "address": "545 Pine Island Rd, N Fort Myers, FL 33903", "phone": "(239) 997-9991", "hours": "Daily 6AM-11PM", "search_url": "https://www.walmart.com/search?q=pokemon+cards&stores=5162"},
        {"id": "w4", "name": "Walmart — San Carlos Blvd", "address": "17105 San Carlos Blvd, Fort Myers Beach, FL 33931", "phone": "(239) 340-7074", "hours": "Daily 6AM-11PM", "search_url": "https://www.walmart.com/search?q=pokemon+cards&stores=3256"},
    ],
    "bestbuy": [
        {"id": "bb1", "name": "Best Buy — S Cleveland Ave", "address": "5019 S Cleveland Ave, Fort Myers, FL 33907", "phone": "(239) 278-1298", "hours": "Mon-Sat 10AM-9PM, Sun 11AM-7PM", "search_url": "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+trading+cards&storeId=268"},
    ],
    "gamestop": [
        {"id": "g1", "name": "GameStop — Edison Mall", "address": "4125 Cleveland Ave Ste 1495, Fort Myers, FL 33901", "phone": "(239) 337-9784", "hours": "Mon-Thu 11AM-7PM, Fri-Sat 10AM-8PM, Sun 12-6PM", "search_url": "https://www.gamestop.com/search/?q=pokemon+cards"},
        {"id": "g2", "name": "GameStop — S Tamiami Trl ⭐", "address": "13711 S Tamiami Trl #4, Fort Myers, FL 33912", "phone": "(239) 432-9639", "hours": "Mon-Thu 11AM-8PM, Fri-Sat 11AM-9PM, Sun 11AM-8PM", "search_url": "https://www.gamestop.com/search/?q=pokemon+cards"},
        {"id": "g3", "name": "GameStop — Pine Island Rd", "address": "535 Pine Island Rd E, N Fort Myers, FL 33903", "phone": "(239) 656-2014", "hours": "Mon-Thu 12-7PM, Fri-Sat 11AM-9PM, Sun 12-8PM", "search_url": "https://www.gamestop.com/search/?q=pokemon+cards"},
    ],
}

COLORS = {"target": 0xCC0000, "walmart": 0x0071CE, "bestbuy": 0x003B64, "gamestop": 0xD4222A}
EMOJIS = {"target": "🎯", "walmart": "🛒", "bestbuy": "💙", "gamestop": "🎮"}

POKEMON_PRODUCTS = [
    ("Booster Box", "pokemon booster box"),
    ("Elite Trainer Box", "pokemon elite trainer box"),
    ("Booster Bundle", "pokemon booster bundle"),
    ("Tin / Collection", "pokemon tin collection"),
    ("Blister Pack", "pokemon blister pack"),
]

async def fetch_walmart_products(store_id):
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1", "Accept-Language": "en-US,en;q=0.9"}
    async with aiohttp.ClientSession() as session:
        for product_name, query in POKEMON_PRODUCTS:
            url = f"https://www.walmart.com/search?q={query.replace(' ', '+')}&stores={store_id}"
            try:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    status = "✅" if r.status == 200 else "❌"
                    results.append(f"{status} [{product_name}]({url})")
            except:
                results.append(f"⚠️ {product_name} — timeout")
    return results

async def fetch_target_products(store_id):
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1", "Accept-Language": "en-US,en;q=0.9"}
    async with aiohttp.ClientSession() as session:
        for product_name, query in POKEMON_PRODUCTS:
            url = f"https://www.target.com/s?searchTerm={query.replace(' ', '+')}&storeId={store_id}"
            try:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    status = "✅" if r.status == 200 else "❌"
                    results.append(f"{status} [{product_name}]({url})")
            except:
                results.append(f"⚠️ {product_name} — timeout")
    return results

async def fetch_bestbuy_products(store_id):
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"}
    async with aiohttp.ClientSession() as session:
        for product_name, query in POKEMON_PRODUCTS:
            url = f"https://www.bestbuy.com/site/searchpage.jsp?st={query.replace(' ', '+')}&storeId={store_id}"
            try:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    status = "✅" if r.status == 200 else "❌"
                    results.append(f"{status} [{product_name}]({url})")
            except:
                results.append(f"⚠️ {product_name} — timeout")
    return results

async def fetch_gamestop_products():
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"}
    async with aiohttp.ClientSession() as session:
        for product_name, query in POKEMON_PRODUCTS:
            url = f"https://www.gamestop.com/search/?q={query.replace(' ', '+')}"
            try:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    status = "✅" if r.status == 200 else "❌"
                    results.append(f"{status} [{product_name}]({url})")
            except:
                results.append(f"⚠️ {product_name} — timeout")
    return results

class ChainSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="🎯 Target (4 locations)", value="target", emoji="🎯"),
            discord.SelectOption(label="🛒 Walmart (4 locations)", value="walmart", emoji="🛒"),
            discord.SelectOption(label="💙 Best Buy (1 location)", value="bestbuy", emoji="💙"),
            discord.SelectOption(label="🎮 GameStop (3 locations)", value="gamestop", emoji="🎮"),
        ]
        super().__init__(placeholder="1️⃣ First pick a store chain...", options=options)

    async def callback(self, interaction: discord.Interaction):
        chain = self.values[0]
        view = LocationView(chain)
        embed = discord.Embed(
            title=f"{EMOJIS[chain]} Select a {chain.title()} Location",
            description="Pick which Fort Myers location to check:",
            color=COLORS[chain]
        )
        for s in STORES[chain]:
            embed.add_field(name=s["name"], value=f"📍 {s['address']}\n📞 {s['phone']}\n🕐 {s['hours']}", inline=False)
        await interaction.response.edit_message(embed=embed, view=view)

class LocationSelect(discord.ui.Select):
    def __init__(self, chain):
        self.chain = chain
        options = []
        for s in STORES[chain]:
            options.append(discord.SelectOption(label=s["name"], value=s["id"], description=s["address"][:50]))
        super().__init__(placeholder="2️⃣ Now pick a specific location...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        store_id_selected = self.values[0]
        chain = self.chain
        store = next(s for s in STORES[chain] if s["id"] == store_id_selected)

        embed = discord.Embed(
            title=f"{EMOJIS[chain]} {store['name']}",
            color=COLORS[chain]
        )
        embed.add_field(name="📍 Address", value=store["address"], inline=False)
        embed.add_field(name="📞 Phone", value=store["phone"], inline=True)
        embed.add_field(name="🕐 Hours", value=store["hours"], inline=True)

        if chain == "walmart":
            wid = store_id_selected.replace("w", "")
            store_nums = {"1": "2924", "2": "3483", "3": "5162", "4": "3256"}
            products = await fetch_walmart_products(store_nums.get(wid, "2924"))
        elif chain == "target":
            tid = store_id_selected.replace("t", "")
            store_nums = {"1": "1267", "2": "2696", "3": "1268", "4": "2354"}
            products = await fetch_target_products(store_nums.get(tid, "1267"))
        elif chain == "bestbuy":
            products = await fetch_bestbuy_products("268")
        else:
            products = await fetch_gamestop_products()

        embed.add_field(
            name="🎴 Pokemon Products",
            value="\n".join(products) if products else "Could not load products",
            inline=False
        )
        embed.set_footer(text="✅ = Link works | Tap product name to search that store | Fort Myers FL")
        await interaction.followup.send(embed=embed)

class LocationView(discord.ui.View):
    def __init__(self, chain):
        super().__init__()
        self.add_item(LocationSelect(chain))

class ChainView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ChainSelect())

@bot.tree.command(name="pokemon", description="Check Pokemon stock at Fort Myers stores")
async def pokemon(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎴 Pokemon Stock Checker — Fort Myers FL",
        description="**Step 1:** Pick a store chain\n**Step 2:** Pick your location\n**Step 3:** See Pokemon products!",
        color=0xFFCC00
    )
    embed.add_field(name="📦 Tracks", value="Booster Boxes • ETBs • Booster Bundles • Tins • Blister Packs", inline=False)
    embed.add_field(name="🏪 Stores", value="4 Targets • 4 Walmarts • 1 Best Buy • 3 GameStops", inline=False)
    await interaction.response.send_message(embed=embed, view=ChainView())

@bot.tree.command(name="stores", description="List all Fort Myers Pokemon store locations")
async def stores(interaction: discord.Interaction):
    embed = discord.Embed(title="📍 All Fort Myers Pokemon Store Locations", color=0xFFCC00)
    for chain, locations in STORES.items():
        text = "\n".join([f"• {s['name']} — {s['address']}" for s in locations])
        embed.add_field(name=f"{EMOJIS[chain]} {chain.upper()}", value=text, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")
    await bot.tree.sync()
    print("Synced!")

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
