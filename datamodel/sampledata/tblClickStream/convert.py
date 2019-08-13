import csv, json, sys
#if you are not using utf-8 files, remove the next line
#check if you pass the input file and output file
if sys.argv[1] is not None and sys.argv[2] is not None:

    fileInput = sys.argv[1]
    fileOutput = sys.argv[2]

    f = csv.writer(open(fileOutput, "w+"))
    f.writerow(["webid", "datetime", "os", "browser", "response_time_ms","product","url"])

    with open(fileInput) as fp:
        for line in fp:
            x  = json.loads(line)
            f.writerow([x["webid"],
                x["datetime"],
                x["os"],
                x["browser"],
                x["response_time_ms"],
                x["product"],
                x["url"]]
               )

    fp.close()
