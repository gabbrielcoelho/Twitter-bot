import tweepy
import logging
import time
import random
from answers import ans

def create_api():
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        print("Online")
    except Exception as e:
        logging.error("Error creating API", exc_info=True)
        raise e
    logging.info("API created")
    return api

def check_mentions(api, keywords, since_id):
    logging.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)

        if any(keyword in tweet.text.lower() for keyword in keywords):
            logging.info(f"Answering to {tweet.user.name}")

            tweet.favorite()
            if not tweet.user.following:
                tweet.user.follow()

            arq = open('sinceIds.txt', 'w')
            arq.write(str(new_since_id))
            arq.close()

            print(new_since_id)
            api.update_status(status=random.choice(ans), in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
    return new_since_id

def main():
    api = create_api()
    arq = open('sinceIds.txt', 'r')
    since_id = int(arq.read().rstrip())
    arq.close()

    while True:
        since_id = check_mentions(api, ["rate"], since_id)
        logging.info("Waiting...")
        time.sleep(30)

if __name__ == "__main__":
    main()
