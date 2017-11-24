#
#
from bson.objectid import ObjectId
#from bson.json_util import bson
import tornado
from tornado import websocket, web, ioloop
import json
import time
import datetime
#
# datoformat for json  
dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
#
#	  
cl = []

def check_origin(self,origin):
    parsed_origin = urllib.parse.urlparser(origin)
    return parsed_origin.netloc.endswith(".svc")

#

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self,origin):
        return True 
    print "socket haandler"
    def open(self):
       # print "SocketHandler open"
        if self not in cl:
            cl.append(self)
            print "socket handler: open"  

    def on_close(self):
        #print "socket handler: close"
        if self in cl:
            print "socket handler: close"
            cl.remove(self)

class ApiHandler(web.RequestHandler):
    

    @web.asynchronous
    def post(self):
        #print "ApiHandler post ()"
        #print self.request.body
        try:
            json_dict = tornado.escape.json_decode(self.request.body)
            #print json_dict
        except:
            json_dict = None
        self.finish()

        id = json_dict['loc']
        amount = json_dict['amount']
        game = json_dict['event']
        try:
            g = ddict[id]
            
            g1 = g.split(';')
            flat = float(g1[0])
            flng = float(g1[1])
            data = {"event":game, "lat":flat, "lng":flng, "amount":amount}
            print "data",data 
            for c in cl:
                #push new values to browser
                item = json.dumps(data, default=dthandler)
                print item
                c.write_message(item)
        except:
            print "not found ", id   


app = web.Application([
    (r'/ws', SocketHandler),
    (r'/api', ApiHandler)
])

table = []
id = []
lat = []
lng = []
geo = []
ddict = {}
dctTable = {}
if __name__ == '__main__':
    for line in open('/opt/app-root/src/geoloc.txt'):
        w = line.strip().split(' ')
        id.append(w[2])
        geo.append( w[3] + ";" + w[4])
        lat.append(w[3])
        lng.append(w[4])
    ddict = dict( zip(id,geo))
    print ddict
    app.listen(8765)
    print "starting up"
    main_loop = ioloop.IOLoop.instance()
    main_loop.start()