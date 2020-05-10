This program will connect to twitch's "points" channel (or any of the pub/sub channels https://dev.twitch.tv/docs/pubsub) and return redemptions.

STEPS YOU NEED TO DO TO GET A VALID OAUTH TOKEN:

1. Create/register your twitch app at https://dev.twitch.tv/console/apps/ (localhost for the URL should be fine)

2. Copy the client id that gets created

3. Go to this URL (but substitute YOURAPPCLIENTIDHERE witht the client ID from step 2) https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=YOURAPPCLIENTIDHERE&redirect_uri=http://localhost&state=tQlBKW4OEJSn3SQ&scope=channel:read:redemptions+chat:read 

4. you'll authorize, be redirected to an invalid url for localhost. HOWEVER, the URL will include your oauth token as "access_token=" Put the in the config file

CHANNEL NAME IN CONFIG:

You can find your channel ID in your stream key inbetween the first two underscores, substitute it in the config file.

This is a purpose-built solution for my dear friend who streams, but it should hopefully get you started on your own application. I didn't see any other Python versions of this script so I hope this helps others.

It could also be reworked for bits or any of the other pub/sub twitch things, but this is for points.