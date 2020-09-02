# "myprocessplant" App
This code allows you to easily create your own Webhook for interacting with [Dialogflow](https://dialogflow.com/) (API v2) and thus integrating the [Netilion API](https://api.netilion.endress.com/doc/v1/) into a conversational platform, as shown in our promotional video.

![Screenshot from Promotional Video](/images/test.png)


# How to Use this Code
The entire process is explained in detail in this Video on Youtube.

**Disclaimer:**
This code was created on data in Netilion containing at least 1 asset in "failure*" status. The Asset also links to an AssetHealthCondition object that has both a cause and a remedy object associated. If these conditions are not met, this code will not yield the expected results. The code merely acts as a example to teach how data from the Netilion API can be requested, parsed, and integrated into 3rd party applications (Dialogflow, Google Assistant, Telegram). The code can act as a basis to customize & improve the code to suit your respective needs.