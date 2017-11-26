# mapapp
openshift/minishift learning

pod1=mapapp: A python tornado server,  receives messages , with sales amount and retailer number.
pod2=map: Conncts to mapapp with websockets and uppdates map with a blink indicating a sale/event.

# get nginx image from redhat
oc import-image my-rhscl/nginx-18-rhel7 --from=registry.access.redhat.com/rhscl/nginx-18-rhel7 --confirm

# create pod to view map
oc new-app nginx-18-rhel7~https://github.com/oddta/map.git

# create python tornado server for receiving event posts (http) , and update map (websocket)
oc new-app python:2.7~https://github.com/oddta/mapapp.git
#
# create service and routes
oc create -f t.svc
oc expose service mapway
oc expose service map

# create test data d.txt

{"event":"Event1","loc":"498831", "amount":"98"}
# send message to mapapp pod

curl -d"@d.txt" -X POST http://mapway-mypro.192.168.99.100.nip.io/api
