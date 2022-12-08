import os
import pandas as pd
from bs4 import BeautifulSoup

df = pd.read_csv("archive-data.csv")


def _check_file(filename):
    return os.path.exists(f"data/{filename}")


def _get_content(filename):
    htmlfile = f"data/{filename}"

    soup = BeautifulSoup(open(htmlfile), "html.parser")

    tags = soup.find_all("p", {"class": "TweetTextSize"})

    tweet = " ".join([tag.get_text() for tag in tags])

    return tweet


df["downloaded"] = df["filename"].apply(_check_file)

filtered_df = df[df["downloaded"]]
filtered_df["tweet_content"] = filtered_df["filename"].apply(_get_content)
filtered_df["url-trunc"] = filtered_df["url"].apply(lambda x: x.split("?")[0])

q1_tweets = filtered_df[filtered_df["tweet_content"].str.contains("USD|rupee|dollar|exchange|remittance")]

print("test")
