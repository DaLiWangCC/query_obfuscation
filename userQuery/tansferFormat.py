import csv

# txt转换为csv

def txt2csv(filePath):
    fTMN = "TMN_queries_2018.12.all.txt"
    fUSER = "User_queries_2018.12.all.txt"

    csvFile = open("tmn.csv", 'w', newline='', encoding='utf-8')
    writer = csv.writer(csvFile)
    csvRow = []

    f = open(fTMN, 'r', encoding='GB2312')
    for line in f:
        csvRow = line.split("\t")
        writer.writerow(csvRow)

    f.close()
    csvFile.close()




fTMN = "TMN_queries_2018.12.all.txt"
fUSER = "User_queries_2018.12.all.txt"
txt2csv(fTMN)