import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

PRODUCTS = [
    {
        "name": "Chaos Rising Booster Box",
        "set": "Mega Evolution — Chaos Rising",
        "type": "Booster Box (36 packs)",
        "release": "May 22, 2026",
        "description": "36 packs, 10 cards each. Features Mega Greninja ex, Mega Floette ex.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/MEG/MEG_EN_logo.png",
        "prices": {"target": "$160.99", "walmart": "$160.99", "bestbuy": "$160.99", "gamestop": "$299.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=chaos+rising+booster+box",
            "walmart": "https://www.walmart.com/search?q=chaos+rising+booster+box",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=chaos+rising+booster+box",
            "gamestop": "https://www.gamestop.com/search/?q=chaos+rising+booster+box",
        },
    },
    {
        "name": "Chaos Rising Elite Trainer Box",
        "set": "Mega Evolution — Chaos Rising",
        "type": "Elite Trainer Box (9 packs)",
        "release": "May 22, 2026",
        "description": "9 booster packs, promo card, accessories. Mega Greninja ex art.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/MEG/MEG_EN_logo.png",
        "prices": {"target": "$49.99", "walmart": "$49.99", "bestbuy": "$49.99", "gamestop": "$89.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=chaos+rising+elite+trainer+box",
            "walmart": "https://www.walmart.com/search?q=chaos+rising+elite+trainer+box",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=chaos+rising+elite+trainer+box",
            "gamestop": "https://www.gamestop.com/search/?q=chaos+rising+elite+trainer+box",
        },
    },
    {
        "name": "Chaos Rising Booster Bundle",
        "set": "Mega Evolution — Chaos Rising",
        "type": "Booster Bundle (6 packs)",
        "release": "May 22, 2026",
        "description": "6 booster packs. Great value for the latest set.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/MEG/MEG_EN_logo.png",
        "prices": {"target": "$27.99", "walmart": "$27.99", "bestbuy": "$27.99", "gamestop": "$59.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=chaos+rising+booster+bundle",
            "walmart": "https://www.walmart.com/search?q=chaos+rising+booster+bundle",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=chaos+rising+booster+bundle",
            "gamestop": "https://www.gamestop.com/search/?q=chaos+rising+booster+bundle",
        },
    },
    {
        "name": "Phantasmal Flames Booster Box",
        "set": "Mega Evolution — Phantasmal Flames",
        "type": "Booster Box (36 packs)",
        "release": "Nov 14, 2025",
        "description": "36 packs. Features Mega Charizard X ex, Mega Gengar ex, Mega Heracross ex.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/PFL/PFL_EN_logo.png",
        "prices": {"target": "$143.99", "walmart": "$143.99", "bestbuy": "$143.99", "gamestop": "$249.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=phantasmal+flames+booster+box",
            "walmart": "https://www.walmart.com/search?q=phantasmal+flames+booster+box",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=phantasmal+flames+booster+box",
            "gamestop": "https://www.gamestop.com/search/?q=phantasmal+flames+booster+box",
        },
    },
    {
        "name": "Phantasmal Flames Elite Trainer Box",
        "set": "Mega Evolution — Phantasmal Flames",
        "type": "Elite Trainer Box (9 packs)",
        "release": "Nov 14, 2025",
        "description": "9 packs, promo card. Mega Charizard X ex art. Most popular ETB.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/PFL/PFL_EN_logo.png",
        "prices": {"target": "$49.99", "walmart": "$49.99", "bestbuy": "$49.99", "gamestop": "$89.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=phantasmal+flames+elite+trainer+box",
            "walmart": "https://www.walmart.com/search?q=phantasmal+flames+elite+trainer+box",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=phantasmal+flames+elite+trainer+box",
            "gamestop": "https://www.gamestop.com/search/?q=phantasmal+flames+elite+trainer+box",
        },
    },
    {
        "name": "Phantasmal Flames Booster Bundle",
        "set": "Mega Evolution — Phantasmal Flames",
        "type": "Booster Bundle (6 packs)",
        "release": "Nov 14, 2025",
        "description": "6 packs. Mega Charizard X ex and Mega Gengar ex inside.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/PFL/PFL_EN_logo.png",
        "prices": {"target": "$27.99", "walmart": "$51.98", "bestbuy": "$27.99", "gamestop": "$49.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=phantasmal+flames+booster+bundle",
            "walmart": "https://www.walmart.com/search?q=phantasmal+flames+booster+bundle",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=phantasmal+flames+booster+bundle",
            "gamestop": "https://www.gamestop.com/search/?q=phantasmal+flames+booster+bundle",
        },
    },
    {
        "name": "Destined Rivals Booster Box",
        "set": "Scarlet & Violet — Destined Rivals",
        "type": "Booster Box (36 packs)",
        "release": "May 30, 2025",
        "description": "36 packs. Team Rocket's Mewtwo ex. High demand reprint incoming.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/DRI/DRI_EN_logo.png",
        "prices": {"target": "$143.99", "walmart": "$143.99", "bestbuy": "$143.99", "gamestop": "$249.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=destined+rivals+booster+box",
            "walmart": "https://www.walmart.com/search?q=destined+rivals+booster+box",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=destined+rivals+booster+box",
            "gamestop": "https://www.gamestop.com/search/?q=destined+rivals+booster+box",
        },
    },
    {
        "name": "Destined Rivals Elite Trainer Box",
        "set": "Scarlet & Violet — Destined Rivals",
        "type": "Elite Trainer Box (9 packs)",
        "release": "May 30, 2025",
        "description": "9 packs, promo card. Features Team Rocket's Mewtwo ex.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/DRI/DRI_EN_logo.png",
        "prices": {"target": "$49.99", "walmart": "$49.99", "bestbuy": "$49.99", "gamestop": "$89.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=destined+rivals+elite+trainer+box",
            "walmart": "https://www.walmart.com/search?q=destined+rivals+elite+trainer+box",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=destined+rivals+elite+trainer+box",
            "gamestop": "https://www.gamestop.com/search/?q=destined+rivals+elite+trainer+box",
        },
    },
    {
        "name": "Destined Rivals Booster Bundle",
        "set": "Scarlet & Violet — Destined Rivals",
        "type": "Booster Bundle (6 packs)",
        "release": "May 30, 2025",
        "description": "6 packs. Most sought-after bundle right now.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/DRI/DRI_EN_logo.png",
        "prices": {"target": "$27.99", "walmart": "$53.99", "bestbuy": "$27.99", "gamestop": "$49.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=destined+rivals+booster+bundle",
            "walmart": "https://www.walmart.com/search?q=destined+rivals+booster+bundle",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=destined+rivals+booster+bundle",
            "gamestop": "https://www.gamestop.com/search/?q=destined+rivals+booster+bundle",
        },
    },
    {
        "name": "Prismatic Evolutions Booster Bundle",
        "set": "Scarlet & Violet — Prismatic Evolutions",
        "type": "Booster Bundle (6 packs)",
        "release": "Jan 17, 2025",
        "description": "6 packs. Eevee evolutions. Still the most hunted product.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/PRE/PRE_EN_logo.png",
        "prices": {"target": "$27.99", "walmart": "$72.99", "bestbuy": "$27.99", "gamestop": "$99.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=prismatic+evolutions+booster+bundle",
            "walmart": "https://www.walmart.com/search?q=prismatic+evolutions+booster+bundle",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=prismatic+evolutions+booster+bundle",
            "gamestop": "https://www.gamestop.com/search/?q=prismatic+evolutions+booster+bundle",
        },
    },
    {
        "name": "Mega Evolution Ascended Heroes ETB",
        "set": "Mega Evolution — Ascended Heroes",
        "type": "Elite Trainer Box (9 packs)",
        "release": "Jan 30, 2026",
        "description": "9 packs + N's Zekrom promo card. Special set.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/MEG/MEG_EN_logo.png",
        "prices": {"target": "$49.99", "walmart": "$49.99", "bestbuy": "$49.99", "gamestop": "$89.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=ascended+heroes+elite+trainer+box",
            "walmart": "https://www.walmart.com/search?q=ascended+heroes+elite+trainer+box",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=ascended+heroes+elite+trainer+box",
            "gamestop": "https://www.gamestop.com/search/?q=ascended+heroes+elite+trainer+box",
        },
    },
    {
        "name": "Pokemon Day 2026 Collection",
        "set": "Pokemon Day 2026",
        "type": "Special Collection Box",
        "release": "Jan 30, 2026",
        "description": "Pikachu 30th anniversary promo, coin, 3 packs (2 Phantasmal Flames + 1 Mega Evolution).",
        "image": "https://assets.pokemon.com/assets/cms2/img/misc/pokemon-day/pokemon-day.png",
        "prices": {"target": "$14.99", "walmart": "$31.99", "bestbuy": "$14.99", "gamestop": "$24.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=pokemon+day+2026+collection",
            "walmart": "https://www.walmart.com/search?q=pokemon+day+2026+collection",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+day+2026+collection",
            "gamestop": "https://www.gamestop.com/search/?q=pokemon+day+2026+collection",
        },
    },
    {
        "name": "White Flare Booster Bundle",
        "set": "Scarlet & Violet — White Flare",
        "type": "Booster Bundle (6 packs)",
        "release": "Jul 18, 2025",
        "description": "6 packs. White Kyurem and Unova Pokemon featured.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/WHT/WHT_EN_logo.png",
        "prices": {"target": "$27.99", "walmart": "$79.99", "bestbuy": "$27.99", "gamestop": "$59.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=white+flare+booster+bundle",
            "walmart": "https://www.walmart.com/search?q=white+flare+booster+bundle",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=white+flare+booster+bundle",
            "gamestop": "https://www.gamestop.com/search/?q=white+flare+booster+bundle",
        },
    },
    {
        "name": "Black Bolt Booster Bundle",
        "set": "Scarlet & Violet — Black Bolt",
        "type": "Booster Bundle (6 packs)",
        "release": "Jul 18, 2025",
        "description": "6 packs. Black Kyurem and Dark-type Pokemon featured.",
        "image": "https://assets.pokemon.com/assets/cms2/img/cards/web/BLK/BLK_EN_logo.png",
        "prices": {"target": "$27.99", "walmart": "$68.90", "bestbuy": "$27.99", "gamestop": "$59.99"},
        "urls": {
            "target": "https://www.target.com/s?searchTerm=black+bolt+booster+bundle",
            "walmart": "https://www.walmart.com/search?q=black+bolt+booster+bundle",
            "bestbuy": "https://www.bestbuy.com/site/searchpage.jsp?st=black+bolt+booster+bundle",
            "gamestop": "https://www.gamestop.com/search/?q=black+bolt+booster+bundle",
        },
    },
]

STORES = {
    "target": [
        {"id": "t1", "name": "Target — Dynasty Dr", "address": "9350 Dynasty Dr, Fort Myers, FL 33905", "phone": "(239) 265-9022", "hours": "Mon-Sat 8AM-10/11PM, Sun 8AM-10PM"},
        {"id": "t2", "name": "Target — S Tamiami Trl", "address": "13711 S Tamiami Trl, Fort Myers, FL 33912", "phone": "(239) 481-8860", "hours": "Mon-Sat 7AM-11PM, Sun 7AM-10PM"},
        {"id": "t3", "name": "Target — Gulf Center Dr ⭐", "address": "10000 Gulf Center Dr, Fort Myers, FL 33913", "phone": "(239) 432-2641", "hours": "Mon-Sat 7AM-11PM, Sun 7AM-10PM"},
        {"id": "t4", "name": "Target — San Carlos Blvd", "address": "15880 San Carlos Blvd, Fort Myers, FL 33908", "phone": "(239) 265-9002", "hours": "Daily 7AM-10PM"},
    ],
    "walmart": [
        {"id": "w1", "name": "Walmart — Colonial Blvd", "address": "4770 Colonial Blvd, Fort Myers, FL 33966", "phone": "(239) 274-2920", "hours": "Daily 6AM-11PM"},
        {"id": "w2", "name": "Walmart — Six Mile Cypress ⭐", "address": "14821 Six Mile Cypress Pkwy, Fort Myers, FL 33912", "phone": "(239) 437-1880", "hours": "Daily 6AM-11PM"},
        {"id": "w3", "name": "Walmart — Pine Island Rd", "address": "545 Pine Island Rd, N Fort Myers, FL 33903", "phone": "(239) 997-9991", "hours": "Daily 6AM-11PM"},
        {"id": "w4", "name": "Walmart — San Carlos Blvd", "address": "17105 San Carlos Blvd, Fort Myers Beach, FL 33931", "phone": "(239) 340-7074", "hours": "Daily 6AM-11PM"},
    ],
    "bestbuy": [
        {"id": "bb1", "name": "Best Buy — S Cleveland Ave", "address": "5019 S Cleveland Ave, Fort Myers, FL 33907", "phone": "(239) 278-1298", "hours": "Mon-Sat 10AM-9PM, Sun 11AM-7PM"},
    ],
    "gamestop": [
        {"id": "g1", "name": "GameStop — Edison Mall", "address": "4125 Cleveland Ave Ste 1495, Fort Myers, FL 33901", "phone": "(239) 337-9784", "hours": "Mon-Thu 11AM-7PM, Fri-Sat 10AM-8PM, Sun 12-6PM"},
        {"id": "g2", "name": "GameStop — S Tamiami Trl ⭐", "address": "13711 S Tamiami Trl #4, Fort Myers, FL 33912", "phone": "(239) 432-9639", "hours": "Mon-Thu 11AM-8PM, Fri-Sat 11AM-9PM, Sun 11AM-8PM"},
        {"id": "g3", "name": "GameStop — Pine Island Rd", "address": "535 Pine Island Rd E, N Fort Myers, FL 33903", "phone": "(239) 656-2014", "hours": "Mon-Thu 12-7PM, Fri-Sat 11AM-9PM, Sun 12-8PM"},
    ],
}

COLORS = {"target": 0xCC0000, "walmart": 0x0071CE, "bestbuy": 0x003B64, "gamestop": 0xD4222A}
EMOJIS = {"target": "🎯", "walmart": "🛒", "bestbuy": "💙", "gamestop": "🎮"}

SET_FILTERS = [
    ("🔥 Chaos Rising (May 2026)", "Chaos Rising"),
    ("👻 Phantasmal Flames (Nov 2025)", "Phantasmal Flames"),
    ("🃏 Destined Rivals (May 2025)", "Destined Rivals"),
    ("✨ Prismatic Evolutions (Jan 2025)", "Prismatic Evolutions"),
    ("⚡ Ascended Heroes / Pokemon Day", "Ascended"),
    ("❄️ White Flare / Black Bolt", "Flare"),
    ("📦 All Products", "All"),
]

class ChainSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="🎯 Target (4 locations)", value="target", emoji="🎯"),
            discord.SelectOption(label="🛒 Walmart (4 locations)", value="walmart", emoji="🛒"),
            discord.SelectOption(label="💙 Best Buy (1 location)", value="bestbuy", emoji="💙"),
            discord.SelectOption(label="🎮 GameStop (3 locations)", value="gamestop", emoji="🎮"),
        ]
        super().__init__(placeholder="1️⃣ Pick a store chain...", options=options)

    async def callback(self, interaction: discord.Interaction):
        chain = self.values[0]
        embed = discord.Embed(
            title=f"{EMOJIS[chain]} Select a {chain.title()} Location — Fort Myers FL",
            description="Choose which location to check:",
            color=COLORS[chain]
        )
        for s in STORES[chain]:
            embed.add_field(
                name=s["name"],
                value=f"📍 {s['address']}\n📞 {s['phone']}\n🕐 {s['hours']}",
                inline=False
            )
        await interaction.response.edit_message(embed=embed, view=LocationView(chain))

class LocationSelect(discord.ui.Select):
    def __init__(self, chain):
        self.chain = chain
        options = [
            discord.SelectOption(label=s["name"], value=s["id"], description=s["address"][:50])
            for s in STORES[chain]
        ]
        super().__init__(placeholder="2️⃣ Pick a location...", options=options)

    async def callback(self, interaction: discord.Interaction):
        chain = self.chain
        store = next(s for s in STORES[chain] if s["id"] == self.values[0])
        embed = discord.Embed(
            title=f"{EMOJIS[chain]} {store['name']}",
            description="Now pick which Pokemon set to view:",
            color=COLORS[chain]
        )
        embed.add_field(name="📍 Address", value=store["address"], inline=True)
        embed.add_field(name="📞 Phone", value=store["phone"], inline=True)
        embed.add_field(name="🕐 Hours", value=store["hours"], inline=False)
        await interaction.response.edit_message(embed=embed, view=SetFilterView(chain, store))

class SetFilterSelect(discord.ui.Select):
    def __init__(self, chain, store):
        self.chain = chain
        self.store = store
        options = [
            discord.SelectOption(label=label, value=value)
            for label, value in SET_FILTERS
        ]
        super().__init__(placeholder="3️⃣ Pick a set to view products...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        chain = self.chain
        store = self.store
        filter_val = self.values[0]

        if filter_val == "All":
            filtered = PRODUCTS
        elif filter_val == "Ascended":
            filtered = [p for p in PRODUCTS if "Ascended" in p["set"] or "Day 2026" in p["set"]]
        elif filter_val == "Flare":
            filtered = [p for p in PRODUCTS if "Flare" in p["set"] or "Bolt" in p["set"]]
        else:
            filtered = [p for p in PRODUCTS if filter_val in p["set"]]

        if not filtered:
            await interaction.followup.send("No products found for that filter.", ephemeral=True)
            return

        for product in filtered:
            price = product["prices"].get(chain, "N/A")
            url = product["urls"].get(chain, "https://google.com")
            embed = discord.Embed(
                title=f"🎴 {product['name']}",
                color=COLORS[chain]
            )
            embed.add_field(name="📦 Type", value=product["type"], inline=True)
            embed.add_field(name="💰 Price at " + chain.title(), value=price, inline=True)
            embed.add_field(name="📅 Released", value=product["release"], inline=True)
            embed.add_field(name="📝 Details", value=product["description"], inline=False)
            embed.add_field(name="🏪 Store", value=f"{store['name']}\n{store['address']}", inline=False)
            embed.add_field(name="🔗 Check Stock", value=f"[Search {chain.title()} for this product]({url})", inline=False)
            embed.set_thumbnail(url=product["image"])
            embed.set_footer(text=f"Fort Myers FL | {store['hours']} | {store['phone']}")
            await interaction.followup.send(embed=embed)

class SetFilterView(discord.ui.View):
    def __init__(self, chain, store):
        super().__init__()
        self.add_item(SetFilterSelect(chain, store))

class LocationView(discord.ui.View):
    def __init__(self, chain):
        super().__init__()
        self.add_item(LocationSelect(chain))

class ChainView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ChainSelect())

@bot.tree.command(name="pokemon", description="Check Pokemon TCG products at Fort Myers stores")
async def pokemon(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎴 Pokemon Stock Checker — Fort Myers FL",
        description=(
            "**How it works:**\n"
            "**Step 1** — Pick a store chain\n"
            "**Step 2** — Pick your Fort Myers location\n"
            "**Step 3** — Pick a Pokemon set\n"
            "**Result** — See every product with name, price, details & store link!\n\n"
            "🔥 **Newest:** Mega Evolution — Chaos Rising (May 22, 2026)"
        ),
        color=0xFFCC00
    )
    embed.add_field(name="🏪 Stores", value="4 Targets • 4 Walmarts • 1 Best Buy • 3 GameStops", inline=False)
    embed.add_field(name="📦 Sets Tracked", value="Chaos Rising • Phantasmal Flames • Destined Rivals • Prismatic Evolutions • Ascended Heroes • White Flare • Black Bolt", inline=False)
    embed.set_footer(text="Prices updated May 2026 | GameStop charges more — always check Target/Walmart first!")
    await interaction.response.send_message(embed=embed, view=ChainView())

@bot.tree.command(name="newset", description="Info about the newest Pokemon TCG set")
async def newset(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 Newest Set: Mega Evolution — Chaos Rising",
        description="Released **May 22, 2026**\n122 cards featuring **Mega Greninja ex** TCG debut!",
        color=0xFF4500
    )
    embed.add_field(name="🃏 Featured Cards", value="Mega Greninja ex • Mega Floette ex • AZ SIR • Roxie SIR • Cinccino ex", inline=False)
    embed.add_field(name="💰 MSRP Prices", value="Booster Box: **$160.99**\nElite Trainer Box: **$49.99**\nBooster Bundle: **$27.99**", inline=False)
    embed.add_field(name="⚠️ GameStop Warning", value="GameStop charges $299.99 for Booster Box vs $160.99 MSRP everywhere else!", inline=False)
    embed.add_field(name="🏪 Buy at MSRP from", value="Target • Walmart • Best Buy", inline=False)
    embed.set_footer(text="Use /pokemon to check your local Fort Myers store!")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stores", description="List all Fort Myers Pokemon store locations")
async def stores(interaction: discord.Interaction):
    embed = discord.Embed(title="📍 All Fort Myers Pokemon Store Locations", color=0xFFCC00)
    for chain, locations in STORES.items():
        text = "\n".join([f"• **{s['name']}**\n  {s['address']} | {s['phone']}" for s in locations])
        embed.add_field(name=f"{EMOJIS[chain]} {chain.upper()}", value=text, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")
    await bot.tree.sync()
    print("Synced!")

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
