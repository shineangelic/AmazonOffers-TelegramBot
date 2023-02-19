from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

# This function allow us to create an HTML message to send
# You can edit all fields of message using HTML syntax

def create_item_html(items):
    response = []
    print(f'{5 * "*"} Creating post {5 * "*"}')

    # Shuffling items
    random.shuffle(items)

    # Iterate over items
    for item in items:
        # If item has an active offer
        if 'off' in item:
             # Creating chart button https://dyn.keepa.com/pricehistory.png?domain=8&asin=B0BGPN9D6F&width=501?
             
            # Creating buy button
            keyboard = [
                [InlineKeyboardButton("🛒 Acquista ora", callback_data='buy', url=item["url"])],
                [InlineKeyboardButton("📉 Grafico prezzi",callback_data='buy',  url='https://dyn.keepa.com/pricehistory.png?domain=8&asin='+item["id"])],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Creating message body

            html = ""
            html += f"🎁 <b>{item['title']}</b> 🎁\n\n"
            if 'description' in list(item.keys()):
                html += f"{item['description']}\n"

            if 'product_group' in list(item.keys()):
                html += f"{item['product_group']}\n"

            if 'product_color' in list(item.keys()):
                html += f"🖌 Colore: {item['product_color']}\n"

            html += f"<a href='{item['image']}'>&#8205</a>\n"

            if 'savings' in list(item.keys()):
                html += f"❌ Non più: {item['original_price']}€ ❌\n\n"

            html += f"💰 <b>Al prezzo di: {item['price']}</b> 💰\n\n"

            if 'lowest_price' in list(item.keys()) and item['lowest_price'] == item['price']:
                html += f"💣 <b>Prezzo minimo garantito</b> 💣\n\n"
            
            if 'highest_price' in list(item.keys()) :
                html += f"📈 <b>In realta partiva da: {item['highest_price']}</b> 📈\n\n"
            
            if 'is_prime_eligible' in list(item.keys()) and item['is_prime_eligible']==True:
                html += f"⏩ <b>Spedizione prime disponibile</b> ⏩\n\n"

            html += f"🔎<a href='{item['url']}' title='{item['url']}'>{item['url']}</a>\n\n"

            if 'savings' in list(item.keys()):
                html += f"💵 <b>Risparmi: {item['savings']}€</b> 💵\n\n"

            html += f"<b><a href='{item['url']}'></a></b>"

            response.append(html)
            response.append(reply_markup)
    return response
