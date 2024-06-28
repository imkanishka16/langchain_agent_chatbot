from flask import Flask
import data_store

app = Flask(__name__)

@app.route('/special_offers', methods=['GET'])
def get_offers():
    offers_list = data_store.offers["offers"]
    formatted_offers = ""
    for offer in offers_list:
        formatted_offers += f"description = {offer['description']}\n"
        formatted_offers += f"url = {offer['url']}\n\n"
    return formatted_offers, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True)