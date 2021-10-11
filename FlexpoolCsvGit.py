# This is program was created for acquiring crypto mining data from pooling websites and exporting it.

import csv
import requests
import time
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

spamStop = False
address = ""   # Insert your miner address here
coin = "ETH"    # This script was made only with ethereum mining in mind, so it should only works well with ETH.
counterValue = "BRL"
updateTime = 22  # In Hours

# Inserting the program on an loop.

while True:
    # Getting the data from Flexpool Api.

    urlWorkers = "https://api.flexpool.io/v2/miner/workers?coin=" + coin + "&address=" + address
    urlBalance = "https://api.flexpool.io/v2/miner/balance?coin=" + coin + "&address=" + address \
                 + "&countervalue=" + counterValue
    urlPayments = "https://api.flexpool.io/v2/miner/paymentsStats?coin=" + coin + "&address=" + address \
                  + "&countervalue=" + counterValue

    headers = {"accept": "application/json"}

    workers = requests.get(urlWorkers, headers)
    balance = requests.get(urlBalance, headers)
    payments = requests.get(urlPayments, headers)

    # Making the response data usable for our application.
    # Doing the workers data.

    dictionary = workers.json()
    workersList = dictionary.get("result")
    workersList = list(workersList)

    # Doing the balance data.

    dictionary = balance.json()
    balanceList = dictionary.get("result")

    # Printing the data for each of the workers

    for counter in range(len(workersList)):  # Informing if any worker is offline and which one is.
        if workersList[counter].get("isOnline") == False:
            print("Minerador " + workersList[counter].get("name") + " está OFFLINE")

        if time.localtime()[3] == updateTime:
            print("Shares da " + workersList[counter].get("name") + " de hoje: "
                  + str(workersList[counter].get('validShares')))

    if time.localtime()[3] == updateTime:
        # Printing the data for the unpaid balance on the pool.
        print("O saldo não pago atual é de " + str(balanceList.get("balance")/(10**18)) + " Ethereum.")
        # Printing the ethereum price.
        print("O valor atual de 1 Ethereum é de R$ " + str(balanceList.get("price")))

        # Printing the time when the data was taken
        print("Horas: " + str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5]))

    # Preparing the data for extraction on the csv file.

    # Getting the calendar date.
    if time.localtime()[3] == updateTime and spamStop == False:
        year = str(time.localtime()[0])
        year = year[-2] + year[-1]
        dayCalendar = (str(time.localtime()[2]) + "/" + str(time.localtime()[1]) + "/" + year)

        # Getting the shares data for each worker and the total shares of the day.
        counter = 0
        totalShares = int(int(workersList[counter + 1].get('validShares')) +
                          int((workersList[counter].get('validShares'))))
        sharesWorker1 = int(workersList[counter+1].get('validShares'))
        sharesWorker2 = int(workersList[counter].get('validShares'))
        sharesWorker3 = 0

        # Getting the total revenue of the day.

        with open('MiningProfitsDaily.csv', newline='') as csvfile:
            data = csvfile.readlines()
        lastRow = data[-1]
        lastRow = lastRow.split(",")

        for x in range(len(lastRow)):
            lastRow[x] = lastRow[x].replace("'", "")
            lastRow[x] = lastRow[x].replace('"', "")

        balanceYesterday = float(str(lastRow[-2]) + "." + str(lastRow[-1]))

        # Getting the total revenue of each worker in ETH and the counter value.

        todayRevenue = balanceList.get("balance")/(10**18) - float(balanceYesterday)

        # Making the today revenue always positive, even when there's a withdrawal from the pool.

        if todayRevenue < 0:
            dictionary = payments.json()
            paymentsList = dictionary.get("result")
            paymentsList = paymentsList.get("lastPayment")
            todayRevenue = todayRevenue + paymentsList.get('value')/(10**18)

        balanceWorker1 = (todayRevenue/totalShares) * sharesWorker1
        balanceWorker2 = (todayRevenue/totalShares) * sharesWorker2
        balanceWorker3 = "0,00"
        revenueWorker1 = balanceWorker1 * balanceList.get("price")
        revenueWorker2 = balanceWorker2 * balanceList.get("price")
        revenueWorker3 = "R$0,00"
        balanceToday = balanceList.get("balance")/(10**18)

        # Changing all the CSV data to the local standard.

        todayRevenue = locale.format_string("%.18f", todayRevenue)
        balanceWorker1 = locale.format_string("%.18f", balanceWorker1)
        balanceWorker2 = locale.format_string("%.18f", balanceWorker2)
        revenueWorker1 = locale.currency(revenueWorker1, grouping=True)
        revenueWorker2 = locale.currency(revenueWorker2, grouping=True)
        balanceToday = locale.format_string("%.18f", balanceToday)

        # Writing all the data on the CVS file.

        with open('MiningProfitsDaily.csv', 'a', newline='') as csvfile:
            csvWriter = csv.writer(csvfile)
            csvWriter.writerow([dayCalendar, sharesWorker1, sharesWorker2, sharesWorker3, totalShares, todayRevenue,
                                balanceWorker1, balanceWorker2, balanceWorker3, revenueWorker1, revenueWorker2,
                                revenueWorker3, balanceToday])

        csvfile.close()

        # Making the program only do one interaction with the csv file per day.

        spamStop = True

    if time.localtime()[3] == (updateTime + 1):
        spamStop = False

    # Making the loop take 10 minutes between each server request.

    time.sleep(600)
