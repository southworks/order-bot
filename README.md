# Order Bot
If you are here, and reading these words, it means that you are either lost or want to play with our Order Bot. You probably want to know what it is and how to run it. You are lucky, I'm gonna explain that now.

### What's an Order Bot?

Well, it's a bot right? According to Google _a bot is an autonomous program on a network (especially the Internet) which can interact with systems or users_. Well, our bot takes care of the food orders for the #cordoba channel on Slack. In the future, it might rule the order business and take care also of the other channels. Yes, we are that ambitious.


### Architecture

### Deployment
```
az deployment create --name "appName" --template-file "template-with-new-rg.json" --location "westus" --parameters appId="appid" appSecret="appsecret" botId="appName" botSku=S1 newAppServicePlanName="app-service-name" newWebAppName="appName" groupName="RG" groupLocation="westus" newAppServicePlanLocation="westus"
az webapp up -n webapp-name
az bot directline create --name appName --resource-group resourceGroup > "DirectLineConfig.json"
```

### How to start?
Running the bot and testing it is simple:

1. Clone the project `git clone https://github.com/southworks/order-bot.git` 
2. Open the project (using PyCharm, VSCode or... Notepad++? Who am I to judge)
3. Go to a command line, go to the project directory and run `python app.py`. Check for common issues and how to solve them [here]()
*insert cmd image*
4. The cmd should now say "Running on http://localhost:PORT", where PORT will be a number.
*insert running image*
5. Copy that URL into the Emulator and add '/api/message' to the end ->  http://localhost:PORT/api/message 
*insert emulator config image*
6. Done! Now you should have something like this:
*insert image of working bot*

