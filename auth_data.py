
phone = "9876543210" #Enter a 10-digit phone number here, without the country code.  

API_key = "rucaptcha.com API Key" # Register at rucaptcha.com, top up your balance for 160 rubles ~$2.5 (enough for recognition of 1000 captchas, which is a lot) and get API key in your personal account. 

email = {
        "Москва" : "yourMailName1",
        "Казань" : "yourMailName2",
        "Екатеринбург" : "yourMailName3",
        "Ростов-на-Дону" : "yourMailName4",
        "Новосибирск" : "yourMailName5",
        "Нижний Новгород" : "yourMailName6",
        "Самара" : "yourMailName7",
    } # Enter any unique name for your email here and the bot will create temporary emails based on that name. For your convenience and security, I suggest you go to https://tempmail.plus/ru/#! enter your email name and in the settings set mailbox lifetime for 7 days and put the pincode that you specify in the list below. Attention do not touch the default email domain (@mailto.plus)

numberOfCitiesMonitoring = 2 #Since blsspain-russia.com recently strengthened protection against bots, this bot can no longer as before monitor places at the same time in all 7 cities, at the moment the limit is two cities. I will look for an opportunity to bypass this restriction. 

emailPin = "" # Enter the pin if you set it up.


telegram_bot_token = "your telegram bot token" # Telegram bot is used to notify you of available spots! Go to telegram, search for @botfather and follow the instructions to create your telegram bot, enter the received token into this variable

# Attention, according to Telegram rules, the bot cannot be the first to start a conversation with you. After creating it, you need to find it by name in the Telegram search and start a conversation with it!

user_id = "Your telegram user id" # Find @userinfobot on Telegram and start a conversation with him, he will give you your user id on Telegram. Enter it in this variable, and the bot will use this id to send you notifications.  