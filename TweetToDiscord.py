import tweepy, discord, time, requests 
from discord import Webhook, RequestsWebhookAdapter

#auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth=tweepy.OAuthHandler("", "");
#auth.set_access_token(access_token, access_token_secret)
auth.set_access_token("", "");
api = tweepy.API(auth);
#get the discord webhook URL from creating a webhook in the prefered channel in your discord server
discordWebhookURL = "";

#Create a StreamListener.
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api;
        self.me = api.me();
    def process_data(self, status):
        print(status.text);
    def on_status(self, tweet):
        photos = []
        #Handle media.
        if 'media' in tweet.entities:
            for image in tweet.entities['media']:
                photos.append(image['media_url']);
                print("adding image to photos");
        #Create webhook on discord server and include URL here.
        webhook = Webhook.from_url(discordWebhookURL, adapter=RequestsWebhookAdapter());
        print(len(photos))
        if len(photos) < 1:
            webhook.send(f"{tweet.user.name} tweeted : {tweet.text}");
        if len(photos) == 1:
            webhook.send(f"{tweet.user.name} tweeted : {tweet.text} {photos[0]}");
        if len(photos) == 2:
            webhook.send(f"{tweet.user.name} tweeted : {tweet.text} {photos[0]} {photos[1]}");
        if len(photos) == 3:
            webhook.send(f"{tweet.user.name} tweeted : {tweet.text} {photos[0]} {photos[1]} {photos[2]}");
        if len(photos) == 4:
            webhook.send(f"{tweet.user.name} tweeted : {tweet.text} {photos[0]} {photos[1]} {photos[2]} {photos[3]}");
    def on_exception(self, exception):
        time.sleep(60);
        print('Took a minute break.');
        #Re-establish stream params in order to check if the stream is not running
        api = tweepy.API(auth);
        myStreamListener = MyStreamListener(api);
        stream = tweepy.Stream(api.auth,  myStreamListener);
        if not stream.running:
            main();
        else:
            print('Failed to continue.');
def main():
    #Create a Stream
    api = tweepy.API(auth);
    myStreamListener = MyStreamListener(api);
    stream = tweepy.Stream(api.auth,  myStreamListener);
    #Update this list of Twitter Ids (string) to follow. 
    #Can find Twitter Id at https://codeofaninja.com/tools/find-twitter-id/
    stream.filter(follow=['']);
#Continuously look out for Twitter events
if __name__ == "__main__":
    while True:
        main()