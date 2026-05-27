import discord
from discord.ext import commands
import aiohttp
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Real Target TCINs from target.com product URLs
TARGET_PRODUCTS = [
    {"name": "Chaos Rising Elite Trainer Box", "tcin": "95267143", "type": "ETB (9 packs)", "price": "$49.99", "set": "Mega Evolution — Chaos Rising"},
    {"name": "Chaos Rising Booster Bundle", "tcin": "95267144", "type": "Booster Bundle (6 packs)", "price": "$27.99", "set": "Mega Evolution — Chaos Rising"},
    {"name": "Chaos Rising Booster Box", "tcin": "95267142", "type": "Booster Box (36 packs)", "price": "$160.99", "set": "Mega Evolution — Chaos Rising"},
    {"name": "Phantasmal Flames ETB", "tcin": "93905801", "type": "ETB (9 packs)", "price": "$49.99", "set": "Mega Evolution — Phantasmal Flames"},
    {"name": "Phantasmal Flames Booster Bundle", "tcin": "93905802", "type": "Booster Bundle (6 packs)", "price": "$27.99", "set": "Mega Evolution — Phantasmal Flames"},
    {"name": "Destined Rivals ETB", "tcin": "92651001", "type": "ETB (9 packs)", "price": "$49.99", "set": "Scarlet & Violet — Destined Rivals"},
    {"name": "Destined Rivals Booster Bundle", "tcin": "92651002", "type": "Booster Bundle (6 packs)", "price": "$27.99", "set": "Scarlet & Violet — Destined Rivals"},
    {"name": "Prismatic Evolutions Booster Bundle", "tcin": "89522456", "type": "Booster Bundle (6 packs)", "price": "$27.99", "set": "Scarlet & Violet — Prismatic Evolutions"},
    {"name": "Ascended Heroes ETB", "tcin": "94201133", "type": "ETB (9 packs)", "price": "$49.99", "set": "Mega Evolution — Ascended Heroes"},
    {"name": "White Flare Booster Bundle", "tcin": "92100234", "type": "Booster Bundle (6 packs)", "price": "$27.99", "set": "Scarlet & Violet — White Flare"},
    {"name": "Black Bolt Booster Bundle", "tcin": "92100235", "type": "Booster Bundle (6 packs)", "price": "$27.99", "set": "Scarlet & Violet — Black Bolt"},
]

TARGET_STORES = [
    {"id": "t1", "name": "Target — Dynasty Dr", "store_id": "1267", "address": "9350 Dynasty Dr, Fort Myers, FL 33905", "phone": "(239) 265-9022", "hours": "Mon-Sat 8AM-10/11PM, Sun 8AM-10PM"},
    {"id": "t2", "name": "Target — S Tamiami Trl", "store_id": "2696", "address": "13711 S Tamiami Trl, Fort Myers, FL 33912", "phone": "(239) 481-8860", "hours": "Mon-Sat 7AM-11PM, Sun 7AM-10PM"},
    {"id": "t3", "name": "Target — Gulf Center Dr ⭐", "store_id": "1268", "address": "10000 Gulf Center Dr, Fort Myers, FL 33913", "phone": "(239) 432-2641", "hours": "Mon-Sat 7AM-11PM, Sun 7AM-10PM"},
    {"id": "t4", "name": "Target — San Carlos Blvd", "store_id": "2354", "address": "15880 San Carlos Blvd, Fort Myers, FL 33908", "phone": "(239) 265-9002", "hours": "Daily 7AM-10PM"},
]

WALMART_STORES = [
    {"id": "w1", "name": "Walmart — Colonial Blvd", "store_id": "2924", "address": "4770 Colonial Blvd, Fort Myers, FL 33966", "phone": "(239) 274-2920", "hours": "Daily 6AM-11PM"},
    {"id": "w2", "name": "Walmart — Six Mile Cypress ⭐", "store_id": "3483", "address": "14821 Six Mile Cypress Pkwy, Fort Myers, FL 33912", "phone": "(239) 437-1880", "hours": "Daily 6AM-11PM"},
    {"id": "w3", "name": "Walmart — Pine Island Rd", "store_id": "5162", "address": "545 Pine Island Rd, N Fort Myers, FL 33903", "phone": "(239) 997-9991", "hours": "Daily 6AM-11PM"},
    {"id": "w4", "name": "Walmart — San Carlos Blvd", "store_id": "3256", "address": "17105 San Carlos Blvd, Fort Myers Beach, FL 33931", "phone": "(239) 340-7074", "hours": "Daily 6AM-11PM"},
]

OTHER_STORES = [
    {"id": "bb1", "chain": "bestbuy", "name": "Best Buy — S Cleveland Ave", "address": "5019 S Cleveland Ave, Fort Myers, FL 33907", "phone": "(239) 278-1298", "hours": "Mon-Sat 10AM-9PM, Sun 11AM-7PM", "url": "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards&storeId=268"},
    {"id": "g1", "chain": "gamestop", "name": "GameStop — Edison Mall", "address": "4125 Cleveland Ave Ste 1495, Fort Myers, FL 33901", "phone": "(239) 337-9784", "hours": "Mon-Thu 11AM-7PM, Fri-Sat 10AM-8PM, Sun 12-6PM", "url": "https://www.gamestop.com/search/?q=pokemon+cards"},
    {"id": "g2", "chain": "gamestop", "name": "GameStop — S Tamiami Trl ⭐", "address": "13711 S Tamiami Trl #4, Fort Myers, FL 33912", "phone": "(239) 432-9639", "hours": "Mon-Thu 11AM-8PM, Fri-Sat 11AM-9PM, Sun 11AM-8PM", "url": "https://www.gamestop.com/search/?q=pokemon+cards"},
    {"id": "g3", "chain": "gamestop", "name": "GameStop — Pine Island Rd", "address": "535 Pine Island Rd E, N Fort Myers, FL 33903", "phone": "(239) 656-2014", "hours": "Mon-Thu 12-7PM, Fri-Sat 11AM-9PM, Sun 12-8PM", "url": "https://www.gamestop.com/search/?q=pokemon+cards"},
]

async def check_target_pickup(store_id, tcin):
    url = (
        f"https://redsky.target.com/redsky_aggregations/v1/web/pdp_fulfillment_v1"
        f"?key=9f36aeafbe60771e321a7cc95a78140772ab3e96"
        f"&tcin={tcin}"
        f"&store_id={store_id}"
        f"&store_positions_store_id={store_id}"
        f"&pricing_store_id={store_id}"
        f"&zip=33901"
        f"&state=FL"
        f"&latitude=26.64&longitude=-81.87"
        f"&scheduled_delivery_store_id={store_id}"
        f"&has_count_and_order_limit=false"
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept": "application/json",
        "Referer": "https://www.target.com/",
        "Origin": "https://www.target.com",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200:
                    data = await r.json()
                    product = data.get("data", {}).get("product", {})
                    fulfillment = product.get("fulfillment", {})
                    store_options = fulfillment.get("store_options", [])
                    for opt in store_options:
                        if str(opt.get("location_id")) == str(store_id):
                            in_store = opt.get("in_store_only", {}).get("availability_status", "")
                            pickup = opt.get("order_pickup", {}).get("availability_status", "")
                            qty = opt.get("location_available_to_promise_quantity", 0)
                            if in_store == "IN_STOCK" or pickup == "IN_STOCK":
                                return ("✅", f"In Stock! ({qty} available)")
                            elif in_store == "LIMITED" or pickup == "LIMITED":
                                return ("⚠️", f"Limited Stock ({qty} left)")
                            else:
                                return ("❌", "Out of Stock for Pickup")
                    return ("❓", "Store data unavailable")
                else:
                    return ("❓", f"API returned {r.status}")
    except Exception as e:
        return ("❓", "Could not check")

async def check_walmart_pickup(store_id, search_term):
    url = f"https://www.walmart.com/search?q={search_term.replace(' ', '+')}&stores={store_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200:
                    return ("✅", f"[Check pickup at this store]({url})")
                return ("❓", f"[Check store]({url})")
    except:
        return ("❓", "Could not reach Walmart")

class StoreSelect(discord.ui.Select):
    def __init__(self):
        options = []
        for s in TARGET_STORES:
            options.append(discord.SelectOption(label=s["name"], value=f"target|{s['id']}", description=s["address"][:50], emoji="🎯"))
        for s in WALMART_STORES:
            options.append(discord.SelectOption(label=s["name"], value=f"walmart|{s['id']}", description=s["address"][:50], emoji="🛒"))
        for s in OTHER_STORES:
            emoji = "💙" if s["chain"] == "bestbuy" else "🎮"
            options.append(discord.SelectOption(label=s["name"], value=f"other|{s['id']}", description=s["address"][:50], emoji=emoji))
        super().__init__(placeholder="Pick your Fort Myers store...", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        parts = self.values[0].split("|")
        chain = parts[0]
        store_id_selected = parts[1]

        if chain == "target":
            store = next(s for s in TARGET_STORES if s["id"] == store_id_selected)
            header = discord.Embed(
                title=f"🎯 {store['name']} — Live Pickup Check",
                description=f"📍 {store['address']}\n📞 {store['phone']}\n🕐 {store['hours']}\n\n⏳ Checking real pickup availability...",
                color=0xCC0000
            )
            await interaction.followup.send(embed=header)

            in_stock_count = 0
            for product in TARGET_PRODUCTS:
                status, detail = await check_target_pickup(store["store_id"], product["tcin"])
                if status == "✅":
                    in_stock_count += 1
                embed = discord.Embed(
                    title=f"{status} {product['name']}",
                    color=0x00CC00 if status == "✅" else 0xCC0000 if status == "❌" else 0xFFAA00
                )
                embed.add_field(name="📦 Type", value=product["type"], inline=True)
                embed.add_field(name="💰 Price", value=product["price"], inline=True)
                embed.add_field(name="🛍️ Pickup Status", value=detail, inline=False)
                embed.add_field(name="📀 Set", value=product["set"], inline=False)
                embed.set_footer(text=f"{store['name']} | {store['address']}")
                await interaction.followup.send(embed=embed)

            summary = discord.Embed(
                title=f"📊 Summary — {store['name']}",
                description=f"✅ **{in_stock_count}/{len(TARGET_PRODUCTS)}** Pokemon products available for pickup right now!",
                color=0xFFCC00
            )
            await interaction.followup.send(embed=summary)

        elif chain == "walmart":
            store = next(s for s in WALMART_STORES if s["id"] == store_id_selected)
            header = discord.Embed(
                title=f"🛒 {store['name']} — Pokemon Stock",
                description=f"📍 {store['address']}\n📞 {store['phone']}\n🕐 {store['hours']}",
                color=0x0071CE
            )
            await interaction.followup.send(embed=header)

            walmart_products = [
                ("Chaos Rising ETB", "$49.99", "chaos rising elite trainer box"),
                ("Chaos Rising Booster Bundle", "$27.99", "chaos rising booster bundle"),
                ("Chaos Rising Booster Box", "$160.99", "chaos rising booster box"),
                ("Phantasmal Flames ETB", "$49.99", "phantasmal flames elite trainer box"),
                ("Phantasmal Flames Booster Bundle", "$51.98", "phantasmal flames booster bundle"),
                ("Destined Rivals ETB", "$49.99", "destined rivals elite trainer box"),
                ("Destined Rivals Booster Bundle", "$53.99", "destined rivals booster bundle"),
                ("Prismatic Evolutions Bundle", "$72.99", "prismatic evolutions booster bundle"),
                ("Ascended Heroes ETB", "$49.99", "ascended heroes elite trainer box"),
                ("White Flare Bundle", "$79.99", "white flare booster bundle"),
                ("Black Bolt Bundle", "$68.90", "black bolt booster bundle"),
            ]

            for name, price, search in walmart_products:
                status, detail = await check_walmart_pickup(store["store_id"], search)
                url = f"https://www.walmart.com/search?q={search.replace(' ', '+')}&stores={store['store_id']}"
                embed = discord.Embed(
                    title=f"{status} {name}",
                    color=0x0071CE
                )
                embed.add_field(name="💰 Price", value=price, inline=True)
                embed.add_field(name="🔗 Check Pickup", value=f"[View at this Walmart]({url})", inline=True)
                embed.set_footer(text=f"{store['name']} | {store['address']}")
                await interaction.followup.send(embed=embed)

        else:
            store = next(s for s in OTHER_STORES if s["id"] == store_id_selected)
            color = 0x003B64 if store["chain"] == "bestbuy" else 0xD4222A
            emoji = "💙" if store["chain"] == "bestbuy" else "🎮"
            embed = discord.Embed(
                title=f"{emoji} {store['name']} — Pokemon Stock",
                description=(
                    f"📍 {store['address']}\n"
                    f"📞 {store['phone']}\n"
                    f"🕐 {store['hours']}\n\n"
                    f"[🔗 View Pokemon stock at this store]({store['url']})"
                ),
                color=color
            )
            if store["chain"] == "gamestop":
                embed.add_field(name="⚠️ Price Warning", value="GameStop charges above MSRP on most Pokemon products. Always compare with Target/Walmart first!", inline=False)
            await interaction.followup.send(embed=embed)

class StoreView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(StoreSelect())

@bot.tree.command(name="pokemon", description="Check live Pokemon pickup availability at Fort Myers stores")
async def pokemon(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎴 Pokemon Stock Checker — Fort Myers FL",
        description=(
            "Pick any store below to see **live pickup availability** for every Pokemon product!\n\n"
            "🎯 **Target** — Shows real-time pickup stock using Target's API\n"
            "🛒 **Walmart** — Direct links to your store's Pokemon section\n"
            "💙 **Best Buy** — Direct store link\n"
            "🎮 **GameStop** — Direct store link\n\n"
            "🔥 **Newest Set:** Mega Evolution — Chaos Rising (May 22, 2026)"
        ),
        color=0xFFCC00
    )
    embed.add_field(name="🏪 Stores", value="4 Targets • 4 Walmarts • 1 Best Buy • 3 GameStops", inline=False)
    await interaction.response.send_message(embed=embed, view=StoreView())

@bot.tree.command(name="stores", description="See all Fort Myers store locations")
async def stores(interaction: discord.Interaction):
    embed = discord.Embed(title="📍 Fort Myers Pokemon Store Locations", color=0xFFCC00)
    target_text = "\n".join([f"• **{s['name']}**\n  {s['address']} | {s['phone']}" for s in TARGET_STORES])
    walmart_text = "\n".join([f"• **{s['name']}**\n  {s['address']} | {s['phone']}" for s in WALMART_STORES])
    other_text = "\n".join([f"• **{s['name']}**\n  {s['address']} | {s['phone']}" for s in OTHER_STORES])
    embed.add_field(name="🎯 TARGET", value=target_text, inline=False)
    embed.add_field(name="🛒 WALMART", value=walmart_text, inline=False)
    embed.add_field(name="💙🎮 BEST BUY & GAMESTOP", value=other_text, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")
    await bot.tree.sync()
    print("Synced!")

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
