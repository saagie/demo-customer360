import csv, json, sys
#if you are not using utf-8 files, remove the next line
#check if you pass the input file and output file
if sys.argv[1] is not None and sys.argv[2] is not None:

    fileInput = sys.argv[1]
    fileOutput = sys.argv[2]

    f = csv.writer(open(fileOutput, "w+"))
    f.writerow(["id", "Name","AccountNumber", "AcctType","BillingStreet","BillingCity","BillingState","BillingPostalCode","Phone","Fax","Email","Status","DateStarted","DateEnded"])

    with open(fileInput) as fp:
        for line in fp:
            x  = json.loads(line)
            f.writerow([x["id"],
                x["Name"]["Name"],
                x["accountnumber"],
                x["AcctType"],
                x["BillingStreet"],
                x["BillingCity"]["city"],
                x["BillingState"],
                x["BillingPostalCode"]["zip"],
                x["Phone"],
                x["Fax"],
                x["Email"],
                x["Status"],
		x["DateStarted"],
		x["DateEnded"]])
    fp.close()
