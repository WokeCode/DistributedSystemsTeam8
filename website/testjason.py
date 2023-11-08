import json

fortune_cookies = json.load(open('website/fortunes.json'))
fortune_cookies = fortune_cookies['fortunes']
