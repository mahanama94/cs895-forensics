import os
import time
import pandas as pd
import urllib.request, urllib.error, urllib.parse

df = pd.read_csv("results.txt", header=None, delimiter=" ",
                 names=["meta", "memento-datetime", "url", "data-type", "status", "1", "2"])

counts = df.groupby(["data-type"]).count()
# print(counts)

df["memento-url"] = df[["memento-datetime", "url"]].astype("str").apply(lambda x: f"https://web.archive.org/web/{x[0]}/{x[1]}", axis=1)
df["filename"] = df[["url", "memento-datetime", "data-type"]].astype("str")\
    .apply(lambda x: f"{x[0].replace('https://twitter.com/an_cabraal/', '').replace('/', '-').replace('?', '_').replace('&', '_').replace('=', '-')}-{x[1]}.{x[2].split('/')[-1]}",
           axis=1)

for index, row in df.iterrows():
    if not os.path.exists(f"data/{row['filename']}"):
        try:
            response = urllib.request.urlopen(row["memento-url"])
            webContent = response.read().decode("UTF-8")

            if response.getcode() == 200:
                f = open(f"data/{row['filename']}", "w")
                f.write(webContent)
                f.close()
            else:
                print(f"{row['memento-url']} : {response.getcode()}")
        except Exception as e:
            print(f"{row['memento-url']} : {e}")
        time.sleep(0.1)

df.to_csv("archive-data.csv")

print("temp")
