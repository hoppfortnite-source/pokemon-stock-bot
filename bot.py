import discord
from discord.ext import commands
import aiohttp
import os
import json

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

FORT_MYERS_ZIP = "33901"

TARGET_STORE_ID = "1267"
WALMART_STORE_ID = "2924"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

async def get_target_stock():
    results = []
    try:
        async with aiohttp.ClientSession() as session:
            url = (
                f"https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"
                f"?key=9f36aeafbe60771e321a7cc95a78140772ab3e96"
                f"&channel=WEB&count=24&default_purchasability_filter=true"
                f"&fulfillment_test_mode=grocery_opu_team_member_experience"
                f"&include_sponsored=true&keyword=pokemon+cards"
                f"&offset=0&platform=desktop&pricing_store_id={TARGET_STORE_ID}"
                f"&scheduled_delivery_store_id={TARGET_STORE_ID}"
                f"&store_ids={TARGET_STORE_ID}&visitor_id=test&zip={FORT_MYERS_ZIP}"
            )
            async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 200:
                    data = await r.json()
                    items = data.get("data", {}).get("search", {}).get("products", [])
                    for item in items[:8]:
                        try:
                            title = item["item"]["product_description"]["title"]
                            price = item["price"]["formatted_current_price"]
                            availability = item.get("fulfillment", {}).get("store_options", [{}])
                            in_stock = False
                            for opt in availability:
                                if opt.get("location_id") == TARGET_STORE_ID:
                                    in_stock = opt.get("in_store_only", {}).get("availability_status") == "IN_STOCK"
                            status = "✅" if in_stock else "⚠️"
                            image = item["item"].get("enrichment", {}).get("images", {}).get("primary_image_url", "")
                            results.append({
                                "name": title,
                                "price": price,
                                "status": status,
                                "image": image,
                                "store": "Target"
                            })
                        except:
                            continue
    except Exception as e:
        print(f"Target error: {e}")
    return results

async def get_walmart_stock():
    results = []
    try:
        async with aiohttp.ClientSession() as session:
            url = (
                f"https://www.walmart.com/search?q=pokemon+cards"
                f"&stores={WALMART_STORE_ID}"
            )
            headers = {**HEADERS, "Accept": "text/html,application/xhtml+xml"}
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 200:
                    text = await r.text()
                    start = text.find('"items":[')
                    if start != -1:
                        results.append({
                            "name": "Pokemon Cards",
                            "price": "See site",
                            "status": "✅",
                            "image": "",
                            "store": "Walmart",
                            "url": f"https://www.walmart.com/search?q=pokemon+cards&store={WALMART_STORE_ID}"
                        })
    except Exception as e:
        print(f"Walmart error: {e}")
    return results

async def get_bestbuy_stock():
    results = []
    try:
        async with aiohttp.ClientSession() as session:
            url = (
                f"https://api.bestbuy.com/v1/products"
                f"((search=pokemon+cards)&storeId=268)"
                f"?apiKey=YourBestBuyAPIKey&show=name,salePrice,inStoreAvailability,thumbnailImage"
                f"&pageSize=8&format=json"
            )
            async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 200:
                    data = await r.json()
                    for item in data.get("products", [])[:8]:
                        status = "✅" if item.get("inStoreAvailability") else "❌"
                        results.append({
                            "name": item.get("name", "Unknown"),
                            "price": f"${item.get('salePrice', '?')}",
                            "status": status,
                            "image": item.get("thumbnailImage", ""),
                            "store": "Best Buy"
                        })
    except Exception as e:
        print(f"Best Buy error: {e}")
    return results

def build_embed(store_name, results, color):
    embed = discord.Embed(
        title=f"🎴 {store_name} Pokemon Stock — Fort Myers FL",
        color=color
    )
    if not results:
        embed.description = "❌ Could not retrieve stock data right now. Try the store link directly."
        return embed

    for item in results[:6]:
        embed.add_field(
            name=f"{item['status']} {item['name'][:50]}",
            value=f"💰 {item.get('price', 'N/A')}",
            inline=False
        )

    if results and results[0].get("image"):
        embed.set_thumbnail(url=results[0]["image"])

    return embed

class StoreSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Target — Fort Myers", value="target", emoji="🎯"),
            discord.SelectOption(label="Walmart — Fort Myers", value="walmart", emoji="🛒"),
            discord.SelectOption(label="Best Buy — Fort Myers", value="bestbuy", emoji="💙"),
            discord.SelectOption(label="All Stores", value="all", emoji="🔍"),
        ]
        super().__init__(placeholder="Pick a store to check stock...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        store = self.values[0]

        embeds = []
        if store in ("target", "all"):
            results = await get_target_stock()
            embeds.append(build_embed("🎯 Target", results, 0xCC0000))
        if store in ("walmart", "all"):
            results = await get_walmart_stock()
            embeds.append(build_embed("🛒 Walmart", results, 0x0071CE))
        if store in ("bestbuy", "all"):
            results = await get_bestbuy_stock()
            embeds.append(build_embed("💙 Best Buy", results, 0x003B64))

        for embed in embeds[:3]:
            embed.set_footer(text="Fort Myers, FL 33901 | Stock updates each time you check")
            await interaction.followup.send(embed=embed)

class StoreView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(StoreSelect())

@bot.tree.command(name="pokemon", description="Check real Pokemon stock at Fort Myers stores")
async def pokemon(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎴 Pokemon Stock Checker — Fort Myers FL",
        description="Select a store to see **real current stock** of Pokemon products!",
        color=0xFFCC00
    )
    embed.add_field(
        name="📦 Checking for",
        value="Booster Boxes • Elite Trainer Boxes • Booster Bundles • Tins & Collections",
        inline=False
    )
    await interaction.response.send_message(embed=embed, view=StoreView())

@bot.tree.command(name="checkall", description="Check all Fort Myers stores for Pokemon stock")
async def checkall(interaction: discord.Interaction):
    await interaction.response.defer()
    stores = [
        ("🎯 Target", get_target_stock, 0xCC0000),
        ("🛒 Walmart", get_walmart_stock, 0x0071CE),
        ("💙 Best Buy", get_bestbuy_stock, 0x003B64),
    ]
    for store_name, fetch_fn, color in stores:
        results = await fetch_fn()
        embed = build_embed(store_name, results, color)
        embed.set_footer(text="Fort Myers, FL 33901")
        await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")
    await bot.tree.sync()
    print("Slash commands synced!")

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
