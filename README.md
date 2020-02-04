# Order Bot
If you are here, and reading these words, it means that you are either lost or want to play with our Order Bot. You probably want to know what it is and how to run it. You are lucky, I'm gonna explain that now.

### What's an Order Bot?

Well, it's a bot right? According to Google _a bot is an autonomous program on a network (especially the Internet) which can interact with systems or users_. Well, our bot takes care of the food orders for the #cordoba channel on Slack. In the future, it might rule the order business and take care also of the other channels. Yes, we are that ambitious.


### Architecture

### Deployment
This script would:
1. Create a new WebApp and AppService
2. Use an existing Resource Group (if an existing one is passed) or create a new one (if a non existing name is passed)
3. Create a Direct Line connection and it's config file

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

4. The cmd should now say "Running on http://localhost:PORT", where PORT will be a number.
![*insert cmd image*](https://github.com/southworks/order-bot/blob/master/documentation/readme_screenshots/pycharm64_c0feHXTETT.png)

5. Copy that URL into the Emulator and add '/api/message' to the end ->  http://localhost:PORT/api/message 

![*insert emulator config image*](https://github.com/southworks/order-bot/blob/master/documentation/readme_screenshots/Bot_Framework_Emulator_bMxNfN0N5r.png)

6. Done! Now you should have something like this:

![*insert image of working bot*](https://github.com/southworks/order-bot/blob/master/documentation/readme_screenshots/Bot_Framework_Emulator_wTX09dpSCY.png)

## Methodology

Backlog organization
1. Create new issues and assigned them to a project version and milestone.
2. The version will be closed when the milestone is completed.
3. If a bug is found on a specific version, it will be fixed on the next version as a priority issue. Also, it will be tagged as _bug_.

Branch organization
1. Each version has a base branch, i.g: order-bot-vX.
2. Each feature belongs to a branch, i.g: order-bot-vX-featureY.
3. When a feature is finished, it merged on the base branch
4. A version will be merged to master when is ready to be deployed.

### What is done
- A base order is being read and written from a .json file.
- Some of the operations we can perform are "Add" and "Remove" an item from the order.
- The order is shown on an Adaptive Card dynamically created.
- It can recognize item quantities



### Next steps
- Recognize when the user wants to add or remove using a different unit. (2Kg Bananas -> 500 Gr Bananas")
- Add more unit tests.
- Test whole conversations.
- Be able to make several operations in one line.
- Maintain the real number of orders.
- Write on an email template the final order when it's confirmed.
- Add concurrency when several users are editing the same order.
- Consider an alternative to Adaptive Card, due to it's not supported on Slack.
