# Orange SMS API 📬

[![Made-In-Senegal](https://github.com/GalsenDev221/made.in.senegal/blob/master/assets/badge.svg)](https://github.com/GalsenDev221/made.in.senegal)

> Orange SMS is a client library that allow you to send SMS with Python using the [Orange SMS API](https://developer.orange.com/apis/sms-sn/overview)

## Disclaimer ⛔

This gem is not an official client of Orange, in order to use the client you need to create a [Orange SMS API](https://developer.orange.com/apis/sms-sn/overview) and to register an app in the developer dashboard that orange provide to you.  
After registering your app you can ask for SMS integration approval (this process can take time :)  
The registration process is detailed [here](https://developer.orange.com/apis/sms-sn/overview)

Instead of reading and trying to understand once again how the Orange SMS API work this gem aims to let you quickly send SMS from Python using the [Orange SMS API](https://developer.orange.com/apis/sms-sn/overview).

## Install 📥

### Via PIP
`python -m pip install orange-sms-client`

## Usage ✅

1. Copy your client id [here](https://developer.orange.com/myapps)
(if you have already create an app)
2. generate token with `getToken` function
3. send sms with `sendSMS` function


Exemple : [usageExample.py](usageExample.py)


### Python 🐍

```python

clientID="your clientID"
token = getToken(clientID)
senderAdress = "+2210000"
address = "+221{{receiver}}"
sendSMS(senderAddress, receiverAddress, "message", token)
```

#### Contributing 🤝

Bug reports and Pull Requests are welcome 👋🏽  
You can tell me **[HERE](https://github.com/honorableCon/OrangeSMS-API/issues)**

#### License 🔖

This project is under **[MIT License](https://opensource.org/licenses/MIT)**.