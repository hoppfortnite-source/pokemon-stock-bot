import discord
from discord.ext import commands
import aiohttp
import os
import json
import re

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_PRODUCTS = [
    {"name": "Chaos Rising Elite Trainer Box", "tcin": "95267143", "price": "$49.99", "set": "Mega Evolution — Chaos Rising", "type": "ETB (9 packs)"},
    {"name": "Chaos Rising Booster Bundle", "tcin": "95267144", "price": "$27.99", "set": "Mega Evolution — Chaos Rising", "type": "Booster Bundle (6 packs)"},
    {"name": "Chaos Rising Booster Box", "tcin": "95267142", "price": "$160.99", "set": "Mega Evolution — Chaos Rising", "type": "Booster Box (36 packs)"},
    {"name": "Phantasmal Flames ETB", "tcin": "93905801", "price": "$49.99", "set": "Mega Evolution — Phantasmal Flames", "type": "ETB (9 packs)"},
    {"name": "Phantasmal Flames Booster Bundle", "tcin": "93905802", "price": "$27.99", "set": "Mega Evolution — Phantasmal Flames", "type": "Booster Bundle (6 packs)"},
    {"name": "Destined Rivals ETB", "tcin": "94300069", "price": "$49.99", "set": "Scarlet & Violet — Destined Rivals", "type": "ETB (9 packs)"},
    {"name": "Destined Rivals Booster Bundle", "tcin": "94300067", "price": "$27.99", "set": "Scarlet & Violet — Destined Rivals", "type": "Booster Bundle (6 packs)"},
    {"name": "Prismatic Evolutions Bundle", "tcin": "93954446", "price": "$27.99", "set": "Scarlet & Violet — Prismatic Evolutions", "type": "Booster Bundle (6 packs)"},
    {"name": "Ascended Heroes Booster Bundle", "tcin": "95120834", "price": "$27.99", "set": "Mega Evolution — Ascended Heroes", "type": "Booster Bundle (6 packs)"},
    {"name": "White Flare ETB", "tcin": "94636860", "price": "$49.99", "set": "Scarlet & Violet — White Flare", "type": "ETB (9 packs)"},
    {"name": "White Flare Booster Bundle", "tcin": "94681785", "price": "$27.99", "set": "Scarlet & Violet — White Flare", "type": "Booster Bundle (6 packs)"},
    {"name": "Black Bolt Booster Bundle", "tcin": "94681770", "price": "$27.99", "set": "Scarlet & Violet — Black Bolt", "type": "Booster Bundle (6 packs)"},
]

WALMART_PRODUCTS = [
    {"name": "Chaos Rising Elite Trainer Box", "item_id": "19988614228", "price": "$49.99", "set": "Mega Evolution — Chaos Rising", "type": "ETB (9 packs)"},
    {"name": "Chaos Rising Booster Box", "item_id": "19939024731", "price": "$160.99", "set": "Mega Evolution — Chaos Rising", "type": "Booster Box (36 packs)"},
    {"name": "Chaos Rising Booster Bundle", "item_id": "19986002628", "price": "$27.99", "set": "Mega Evolution — Chaos Rising", "type": "Booster Bundle (6 packs)"},
    {"name": "Phantasmal Flames ETB", "item_id": "5191494551", "price": "$49.99", "set": "Mega Evolution — Phantasmal Flames", "type": "ETB (9 packs)"},
    {"name": "Phantasmal Flames Booster Bundle", "item_id": "5191494552", "price": "$51.98", "set": "Mega Evolution — Phantasmal Flames", "type": "Booster Bundle (6 packs)"},
    {"name": "Destined Rivals ETB", "item_id": "4800927523", "price": "$49.99", "set": "Scarlet & Violet — Destined Rivals", "type": "ETB (9 packs)"},
    {"name": "Destined Rivals Booster Bundle", "item_id": "4800927524", "price": "$53.99", "set": "Scarlet & Violet — Destined Rivals", "type": "Booster Bundle (6 packs)"},
    {"name": "Prismatic Evolutions Bundle", "item_id": "3977893546", "price": "$72.99", "set": "Scarlet & Violet — Prismatic Evolutions", "type": "Booster Bundle (6 packs)"},
    {"name": "Ascended Heroes ETB", "item_id": "4477293015", "price": "$49.99", "set": "Mega Evolution — Ascended Heroes", "type": "ETB (9 packs)"},
    {"name": "White Flare Bundle", "item_id": "5001847291", "price": "$79.99", "set": "Scarlet & Violet — White Flare", "type": "Booster Bundle (6 packs)"},
    {"name": "Black Bolt Bundle", "item_id": "5001847292", "price": "$68.90", "set": "Scarlet & Violet — Black Bolt", "type": "Booster Bundle (6 packs)"},
]

BESTBUY_PRODUCTS = [
    {"name": "Chaos Rising Elite Trainer Box", "sku": "6609821", "price": "$49.99", "set": "Mega Evolution — Chaos Rising", "type": "ETB (9 packs)"},
    {"name": "Chaos Rising Booster Bundle", "sku": "6609822", "price": "$27.99", "set": "Mega Evolution — Chaos Rising", "type": "Booster Bundle (6 packs)"},
    {"name": "Chaos Rising Booster Box", "sku": "6609820", "price": "$160.99", "set": "Mega Evolution — Chaos Rising", "type": "Booster Box (36 packs)"},
    {"name": "Phantasmal Flames ETB", "sku": "6591234", "price": "$49.99", "set": "Mega Evolution — Phantasmal Flames", "type": "ETB (9 packs)"},
    {"name": "Phantasmal Flames Bundle", "sku": "6591235", "price": "$27.99", "set": "Mega Evolution — Phantasmal Flames", "type": "Booster Bundle (6 packs)"},
    {"name": "Destined Rivals ETB", "sku": "6573421", "price": "$49.99", "set": "Scarlet & Violet — Destined Rivals", "type": "ETB (9 packs)"},
    {"name": "Destined Rivals Bundle", "sku": "6573422", "price": "$27.99", "set": "Scarlet & Violet — Destined Rivals", "type": "Booster Bundle (6 packs)"},
    {"name": "Prismatic Evolutions Bundle", "sku": "6552341", "price": "$27.99", "set": "Scarlet & Violet — Prismatic Evolutions", "type": "Booster Bundle (6 packs)"},
    {"name": "Ascended Heroes ETB", "sku": "6598765", "price": "$49.99", "set": "Mega Evolution — Ascended Heroes", "type": "ETB (9 packs)"},
    {"name": "White Flare Bundle", "sku": "6587654", "price": "$27.99", "set": "Scarlet & Violet — White Flare", "type": "Booster Bundle (6 packs)"},
    {"name": "Black Bolt Bundle", "sku": "6587655", "price": "$27.99", "set": "Scarlet & Violet — Black Bolt", "type": "Booster Bundle (6 packs)"},
]

GAMESTOP_PRODUCTS = [
    {"name": "Chaos Rising Elite Trainer Box", "product_id": "20033749", "price": "$89.99 ⚠️", "set": "Mega Evolution — Chaos Rising", "type": "ETB (9 packs)"},
    {"name": "Chaos Rising Booster Bundle", "product_id": "20033748", "price": "$59.99 ⚠️", "set": "Mega Evolution — Chaos Rising", "type": "Booster Bundle (6 packs)"},
    {"name": "Chaos Rising Booster Box", "product_id": "20033747", "price": "$299.99 ⚠️", "set": "Mega Evolution — Chaos Rising", "type": "Booster Box (36 packs)"},
    {"name": "Phantasmal Flames ETB", "product_id": "20012345", "price": "$89.99 ⚠️", "set": "Mega Evolution — Phantasmal Flames", "type": "ETB (9 packs)"},
    {"name": "Phantasmal Flames Bundle", "product_id": "20012346", "price": "$49.99 ⚠️", "set": "Mega Evolution — Phantasmal Flames", "type": "Booster Bundle (6 packs)"},
    {"name": "Destined Rivals ETB", "product_id": "20001234", "price": "$89.99 ⚠️", "set": "Scarlet & Violet — Destined Rivals", "type": "ETB (9 packs)"},
    {"name": "Destined Rivals Bundle", "product_id": "20001235", "price": "$49.99 ⚠️", "set": "Scarlet & Violet — Destined Rivals", "type": "Booster Bundle (6 packs)"},
    {"name": "Prismatic Evolutions Bundle", "product_id": "19987654", "price": "$99.99 ⚠️", "set": "Scarlet & Violet — Prismatic Evolutions", "type": "Booster Bundle (6 packs)"},
    {"name": "Ascended Heroes ETB", "product_id": "20019876", "price": "$89.99 ⚠️", "set": "Mega Evolution — Ascended Heroes", "type": "ETB (9 packs)"},
    {"name": "White Flare Bundle", "product_id": "20009871", "price": "$59.99 ⚠️", "set": "Scarlet & Violet — White Flare", "type": "Booster Bundle (6 packs)"},
    {"name": "Black Bolt Bundle", "product_id": "20009872", "price": "$59.99 ⚠️", "set": "Scarlet & Violet — Black Bolt", "type": "Booster Bundle (6 packs)"},
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

BESTBUY_STORES = [
    {"id": "bb1", "name": "Best Buy — S Cleveland Ave", "store_id": "268", "address": "5019 S Cleveland Ave, Fort Myers, FL 33907", "phone": "(239) 278-1298", "hours": "Mon-Sat 10AM-9PM, Sun 11AM-7PM"},
]

GAMESTOP_STORES = [
    {"id": "g1", "name": "GameStop — Edison Mall", "store_id": "1234", "address": "4125 Cleveland Ave Ste 1495, Fort Myers, FL 33901", "phone": "(239) 337-9784", "hours": "Mon-Thu 11AM-7PM, Fri-Sat 10AM-8PM, Sun 12-6PM"},
    {"id": "g2", "name": "GameStop — S Tamiami Trl ⭐", "store_id": "4567", "address": "13711 S Tamiami Trl #4, Fort Myers, FL 33912", "phone": "(239) 432-9639", "hours": "Mon-Thu 11AM-8PM, Fri-Sat 11AM-9PM, Sun 11AM-8PM"},
    {"id": "g3", "name": "GameStop — Pine Island Rd", "store_id": "8901", "address": "535 Pine Island Rd E, N Fort Myers, FL 33903", "phone": "(239) 656-2014", "hours": "Mon-Thu 12-7PM, Fri-Sat 11AM-9PM, Sun 12-8PM"},
]

COLORS = {"target": 0xCC0000, "walmart": 0x0071CE, "bestbuy": 0x003B64, "gamestop": 0xD4222A}
EMOJIS = {"target": "🎯", "walmart": "🛒", "bestbuy": "💙", "gamestop": "🎮"}

MOBILE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json",
}

async def check_target_pickup(store_id, tcin):
    url = (
        f"https://redsky.target.com/redsky_aggregations/v1/web/pdp_fulfillment_v1"
        f"?key=9f36aeafbe60771e321a7cc95a78140772ab3e96"
        f"&tcin={tcin}&store_id={store_id}&store_positions_store_id={store_id}"
        f"&pricing_store_id={store_id}&zip=33901&state=FL"
        f"&latitude=26.64&longitude=-81.87&scheduled_delivery_store_id={store_id}"
    )
    try:
        async with aiohttp.ClientSession() as session:
            headers = {**MOBILE_HEADERS, "Referer": "https://www.target.com/", "Origin": "https://www.target.com"}
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200:
                    data = await r.json()
                    store_options = data.get("data", {}).get("product", {}).get("fulfillment", {}).get("store_options", [])
                    for opt in store_options:
                        if str(opt.get("location_id")) == str(store_id):
                            in_store = opt.get("in_store_only", {}).get("availability_status", "")
                            pickup = opt.get("order_pickup", {}).get("availability_status", "")
                            qty = opt.get("location_available_to_promise_quantity", 0)
                            if in_store == "IN_STOCK" or pickup == "IN_STOCK":
                                return ("✅", f"In Stock! ({qty} available for pickup)")
                            elif in_store == "LIMITED" or pickup == "LIMITED":
                                return ("⚠️", f"Limited Stock! ({qty} left)")
                            else:
                                return ("❌", "Out of Stock for Pickup")
                    return ("❓", "Store data unavailable")
                elif r.status == 404:
                    return ("❌", "Not carried at this store")
                else:
                    return ("❓", f"API error {r.status}")
    except:
        return ("❓", "Check failed")

async def check_walmart_pickup(store_id, item_id):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://www.walmart.com/ip/{item_id}"
            headers = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Cookie": f"location-data={{\"storeId\":\"{store_id}\",\"zip\":\"33901\",\"city\":\"Fort Myers\",\"state\":\"FL\"}}",
            }
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=12)) as r:
                if r.status == 200:
                    text = await r.text()
                    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', text, re.DOTALL)
                    if match:
                        try:
                            data = json.loads(match.group(1))
                            props = data.get("props", {}).get("pageProps", {}).get("initialData", {})
                            product = props.get("data", {}).get("product", {})
                            offer = product.get("offers", {}).get("primary", {})
                            for opt in offer.get("fulfillmentOptions", []):
                                if opt.get("type") == "PICKUP":
                                    avail = opt.get("availabilityStatus", "")
                                    if avail == "IN_STOCK":
                                        return ("✅", "Available for Pickup Today!")
                                    elif avail == "OUT_OF_STOCK":
                                        return ("❌", "Out of Stock for Pickup")
                                    else:
                                        return ("⚠️", f"Status: {avail}")
                        except:
                            pass
                    if "out of stock" in text.lower()[:3000]:
                        return ("❌", "Out of Stock for Pickup")
                    if "pickup" in text.lower():
                        return ("⚠️", f"[Check pickup at this Walmart](https://www.walmart.com/store/{store_id}/search?q=pokemon)")
                return ("❓", "Could not read page")
    except:
        return ("❓", "Check failed")

async def check_bestbuy_pickup(store_id, sku):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://www.bestbuy.com/api/tcfb/model.json?paths=%5B%5B%22shop%22%2C%22buttonstate%22%2C%22v5%22%2C%22item%22%2C%22skus%22%2C%22{sku}%22%2C%22conditions%22%2C%22NONE%22%2C%22destinationZipCode%22%2C%2233901%22%2C%22storeId%22%2C%22{store_id}%22%2C%22context%22%2C%22cyp%22%2C%22addAll%22%2C%22false%22%5D%5D&method=get"
            async with session.get(url, headers=MOBILE_HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200:
                    data = await r.json()
                    try:
                        btn = data["jsonGraph"]["shop"]["buttonstate"]["v5"]["item"]["skus"][sku]["conditions"]["NONE"]["destinationZipCode"]["33901"]["storeId"][store_id]["context"]["cyp"]["addAll"]["false"]["value"]
                        state = btn.get("buttonState", "")
                        pickup_msg = btn.get("pickupMessage", "")
                        if state == "ADD_TO_CART":
                            return ("✅", f"In Stock for Pickup! {pickup_msg}".strip())
                        elif state == "CHECK_STORES":
                            return ("⚠️", "Limited — Check Store")
                        elif state == "SOLD_OUT":
                            return ("❌", "Sold Out")
                        else:
                            return ("❓", f"Status: {state}")
                    except (KeyError, TypeError):
                        pass
            product_url = f"https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards&storeId={store_id}"
            async with aiohttp.ClientSession() as session:
                async with session.get(product_url, headers=MOBILE_HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as r2:
                    if r2.status == 200:
                        text = await r2.text()
                        if "add to cart" in text.lower():
                            return ("✅", f"[Items in stock at this Best Buy]({product_url})")
                        elif "sold out" in text.lower():
                            return ("❌", "Sold Out")
                        return ("⚠️", f"[Check Best Buy]({product_url})")
        return ("❓", "Could not check Best Buy")
    except:
        return ("❓", "Check failed")

async def check_gamestop_pickup(store_id, product_id):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://www.gamestop.com/on/demandware.store/Sites-gamestop-us-Site/en_US/Product-GetInventoryInformation?pid={product_id}&storeId={store_id}"
            async with session.get(url, headers=MOBILE_HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200:
                    data = await r.json()
                    avail = data.get("availability", {})
                    in_store = avail.get("inStorePickup", False)
                    qty = avail.get("quantity", 0)
                    if in_store and qty > 0:
                        return ("✅", f"In Stock for Pickup! ({qty} available)")
                    elif in_store:
                        return ("⚠️", "Limited — call to confirm")
                    else:
                        return ("❌", "Not available for pickup")
            fallback = f"https://www.gamestop.com/search/?q=pokemon+cards&prefn1=storeAvailability&prefv1=Available+In+Store"
            async with aiohttp.ClientSession() as session2:
                async with session2.get(fallback, headers=MOBILE_HEADERS, timeout=aiohttp.ClientTimeout(total=10)) as r2:
                    if r2.status == 200:
                        text = await r2.text()
                        if "pokemon" in text.lower() and "add to cart" in text.lower():
                            return ("✅", f"[Pokemon cards in stock at GameStop]({fallback})")
                        return ("⚠️", f"[Check GameStop stock]({fallback})")
        return ("❓", "Could not check GameStop")
    except:
        return ("❓", "Check failed")

def build_store_options():
    options = []
    for s in TARGET_STORES:
        options.append(discord.SelectOption(label=s["name"], value=f"target|{s['id']}", description=s["address"][:50], emoji="🎯"))
    for s in WALMART_STORES:
        options.append(discord.SelectOption(label=s["name"], value=f"walmart|{s['id']}", description=s["address"][:50], emoji="🛒"))
    for s in BESTBUY_STORES:
        options.append(discord.SelectOption(label=s["name"], value=f"bestbuy|{s['id']}", description=s["address"][:50], emoji="💙"))
    for s in GAMESTOP_STORES:
        options.append(discord.SelectOption(label=s["name"], value=f"gamestop|{s['id']}", description=s["address"][:50], emoji="🎮"))
    return options

class StoreSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Pick your Fort Myers store...", options=build_store_options())

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        chain, store_id_sel = self.values[0].split("|")

        if chain == "target":
            store = next(s for s in TARGET_STORES if s["id"] == store_id_sel)
            products = TARGET_PRODUCTS
            async def check(p): return await check_target_pickup(store["store_id"], p["tcin"])
        elif chain == "walmart":
            store = next(s for s in WALMART_STORES if s["id"] == store_id_sel)
            products = WALMART_PRODUCTS
            async def check(p): return await check_walmart_pickup(store["store_id"], p["item_id"])
        elif chain == "bestbuy":
            store = next(s for s in BESTBUY_STORES if s["id"] == store_id_sel)
            products = BESTBUY_PRODUCTS
            async def check(p): return await check_bestbuy_pickup(store["store_id"], p["sku"])
        else:
            store = next(s for s in GAMESTOP_STORES if s["id"] == store_id_sel)
            products = GAMESTOP_PRODUCTS
            async def check(p): return await check_gamestop_pickup(store["store_id"], p["product_id"])

        header = discord.Embed(
            title=f"{EMOJIS[chain]} {store['name']} — Live Pickup Check",
            description=(
                f"📍 **{store['address']}**\n"
                f"📞 {store['phone']} | 🕐 {store['hours']}\n\n"
                f"⏳ Checking live pickup for **{len(products)} products**..."
            ),
            color=COLORS[chain]
        )
        if chain == "gamestop":
            header.set_footer(text="⚠️ GameStop prices are above MSRP — always compare with Target/Walmart!")
        await interaction.followup.send(embed=header)

        in_stock = 0
        for product in products:
            status, detail = await check(product)
            if status == "✅":
                in_stock += 1
            color = 0x00CC00 if status == "✅" else 0xFF4444 if status == "❌" else 0xFFAA00
            embed = discord.Embed(title=f"{status} {product['name']}", color=color)
            embed.add_field(name="📦 Type", value=product["type"], inline=True)
            embed.add_field(name="💰 Price", value=product["price"], inline=True)
            embed.add_field(name="🛍️ Pickup Status", value=detail, inline=False)
            embed.add_field(name="📀 Set", value=product["set"], inline=True)
            embed.set_footer(text=f"{store['name']} | {store['address']}")
            await interaction.followup.send(embed=embed)

        summary = discord.Embed(
            title=f"📊 {store['name']} — Summary",
            description=f"{'🎉' if in_stock > 0 else '😔'} **{in_stock}/{len(products)}** Pokemon products available for pickup right now!",
            color=0x00CC00 if in_stock > 0 else 0xFF4444
        )
        await interaction.followup.send(embed=summary)

class StoreView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(StoreSelect())

@bot.tree.command(name="pokemon", description="Check live Pokemon pickup at all Fort Myers stores")
async def pokemon(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎴 Pokemon Stock Checker — Fort Myers FL",
        description=(
            "Pick **any store** to see live pickup availability!\n\n"
            "🎯 **Target** — Live via Target RedSky API\n"
            "🛒 **Walmart** — Live via Walmart product pages\n"
            "💙 **Best Buy** — Live via Best Buy API\n"
            "🎮 **GameStop** — Live via GameStop inventory API\n\n"
            "🔥 **Newest Set:** Mega Evolution — Chaos Rising (May 22, 2026)"
        ),
        color=0xFFCC00
    )
    embed.add_field(name="🏪 All Stores", value="4 Targets • 4 Walmarts • 1 Best Buy • 3 GameStops", inline=False)
    embed.add_field(name="📦 Products Tracked", value="Booster Boxes • ETBs • Booster Bundles • Collections", inline=False)
    await interaction.response.send_message(embed=embed, view=StoreView())

@bot.tree.command(name="stores", description="See all Fort Myers Pokemon store locations")
async def stores(interaction: discord.Interaction):
    embed = discord.Embed(title="📍 All Fort Myers Pokemon Store Locations", color=0xFFCC00)
    for chain, store_list in [("target", TARGET_STORES), ("walmart", WALMART_STORES), ("bestbuy", BESTBUY_STORES), ("gamestop", GAMESTOP_STORES)]:
        text = "\n".join([f"• **{s['name']}**\n  {s['address']} | {s['phone']}" for s in store_list])
        embed.add_field(name=f"{EMOJIS[chain]} {chain.upper()}", value=text, inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="newset", description="Info on the newest Pokemon TCG set")
async def newset(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🔥 Newest: Mega Evolution — Chaos Rising",
        description="Released **May 22, 2026** — 122 cards!",
        color=0xFF4500
    )
    embed.add_field(name="⭐ Chase Cards", value="Mega Greninja ex SIR ($478) • Mega Floette ex • AZ SIR • Roxie SIR • Cinccino ex", inline=False)
    embed.add_field(name="💰 MSRP Prices", value="Booster Box: **$160.99**\nETB: **$49.99**\nBundle: **$27.99**", inline=False)
    embed.add_field(name="⚠️ GameStop Warning", value="GameStop charges $299.99 for Booster Box vs $160.99 everywhere else!", inline=False)
    embed.set_footer(text="Use /pokemon to check your local Fort Myers store!")
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"Bot ready as {bot.user}")
    await bot.tree.sync()
    print("Synced!")

TOKEN = os.environ.get('DISCORD_TOKEN')
bot.run(TOKEN)
