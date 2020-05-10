import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import cgi
import random
from playsound import playsound
with open('pointdjconfig.txt','r') as inf:
    mydict = eval(inf.read())

# you can find your channel id in your stream key between the first two underscores
# channels are defined via https://dev.twitch.tv/docs/pubsub with their required rights
topics=mydict["topics"]
# register your app, copy the client id. go to this url (replace YOURAPPLCIENTIDHERE:
# https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=YOURAPPCLIENTIDHERE&redirect_uri=http://localhost&state=tQlBKW4OEJSn3SQ&scope=channel:read:redemptions+chat:read
# you'll authorize, be redirected to an invalid url for localhost.
# the url will include your oauth token as "access_token="
# Put it in your config file
oauth=str(mydict["oauth"])

connect_to={
  "type": "LISTEN",
  "nonce": "ASDJDJASDNASDNASDNasdkasdlkasdj",
  "data": {
    "topics": topics,
    "auth_token": oauth
  }
}
connect_to=str(connect_to).replace("'",'"')
print(connect_to)
def playSound(soundname):
  if soundname=="random":
    path=os.path.dirname(os.path.realpath(__file__))
    randomfile = os.listdir(path)
    sanitized=[]
    for thing in randomfile:
      if "mp3" in thing:
        sanitized.append(thing)
        file = path + '\\' + random.choice(sanitized)
        playsound(file)
  else:
    mysong=soundname
    try:
      playsound('./'+cgi.escape(str(mysong).replace('.','').replace('/','').replace("\\",'').replace('"','').replace("'","").replace('?','').replace('!','').replace('*','').replace('$',''))+'.mp3')
    except Exception as e:
      print ("EXCEPTION: "+str(e))
      pass

def on_message(ws, message):

    if "data" in message:
      messagesan=json.loads(message)
      
      print("MESSAGESAN:"+str(json.dumps(messagesan, indent=4, sort_keys=True)))
      messagesub=json.loads(messagesan["data"]["message"])
      print("MESSAGESANsub:"+str(json.dumps(messagesub, indent=4, sort_keys=True)))
      redeemed_by=str(messagesub["data"]["redemption"]["user"]["display_name"])
      user_input=str(messagesub["data"]["redemption"]["user_input"])
      reward_name=str(messagesub["data"]["redemption"]["reward"]["prompt"])
      print("SPECIAL REWARD REDEEMED: "+reward_name+" "+user_input+" "+redeemed_by)
      playSound(user_input)
    else:
      print(json.dumps(json.loads(message), indent=4, sort_keys=True))

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        print("sending ping")
        ws.send('{"type":"PING"}')
        time.sleep(1)
        ws.send(connect_to)
        print("ok?")
        print("entering loop")
        while True:
          ws.send('{"type":"PING"}')
          print("Sending ping...")
          time.sleep(30)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://pubsub-edge.twitch.tv",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()