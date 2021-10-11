# FlexpoolCSV
A python script to pull mining data from the Flexpool API and store it to an already existing CSV file for keeping historical data.

This script was created as a tool to automate my work of manually input miner data on my Excel sheet. The Excel sheet was created as a way for me to see how much ETH was mined
daily, for each worker that i have mining on Flexpool and also calculate the estimated daily profit of that worker.

Due to the already existing Excel sheet, and this being more of a project for my personal programming education, this script was created with some limitations, such as:

- A third, now inactive worker has been filed with "0.00" on all its columns.
- A file format with only two active workers
- ETH prices only working on Brazilian real
- Using the previous row to save the total unpaid ETH mined, which renders this script useless without an already existing CSV file.

Other known limitations.

- This script should be left running 24/7 or ran once per day at the scheduled update time.
- If it's turned off at the scheduled update time, it shouldn't be opened again until after the time window ( start of the next hour by default) is closed or it will add an  unnecessary row oin the CSV file.
- It requires constant internet connection to reach de Flexpool API.
