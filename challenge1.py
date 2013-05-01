import os
import time
import pyrax
import pyrax.exceptions as exc

print
print "using credentials file"

try:
    pyrax.set_credential_file('/home/ryan/api_python/.python_cred_file')
except exc.AuthtenticationFailed:
    print "Authentication Failed"
print "Authenticated", pyrax.identity.authenticated
print

cs = pyrax.cloudservers

flvs = cs.flavors.list()
flvnum = -1
for flv in flvs:
    flvnum += 1
    print "For this selection, input number:", flvnum 
    print "Name:", flv.name
    print " ID:", flv.id
    print " RAM:", flv.ram
    print " Disk:", flv.disk
    print " VCPUs:", flv.vcpus
    print ""


flv = int(raw_input("Choose Flavor: "))

print
print

if flv > flvnum:
    print "Try again, flavor value not possible"
elif flv < 0:
    print "Try again, flavor value not possible"
else:
    print "You have chosen:", cs.flavors.list()[flv]

print
print 

imgs = cs.images.list()
imgnum = -1
for img in imgs:
    imgnum += 1
    print "Input number %s\n for %s" % (imgnum,img.name)
    print 

print
print

img = int(raw_input("Choose Image: "))

print
print

if img > imgnum:
    print "Try again, image value not possible"
elif img < 0:
    print "Try again, image value not possible"
else:
    print "You have chosen:", cs.images.list()[img]

print
print

servers = []

num_servers = int(raw_input("Enter the amount of servers to create: "))
name = raw_input("Enter a name for the server/s: ")

i = 0
while (i < num_servers):
    i = i + 1
    server_name = name + str(i)
    print "Creating Server # " , i
    server = cs.servers.create(server_name, cs.images.list()[img].id, cs.flavors.list()[flv].id)
    servers.append(server)
#    print "Name:", server.name
#    print "ID:", server.id
#    print "Status:", server.status
#    print "Admin Password:", server.adminPass
#    print "Networks:", server.networks

print

while True:
    print "Checking Servers..."
    time.sleep(5)
    count = 0
    for s in servers:
        server = cs.servers.get(s.id)
        if server.status == 'ACTIVE':
            count += 1
        else:
            print "Server: %s building...%s" % (s.name,server.progress)
    if count == len(servers):
        for s in servers:
            server = cs.servers.get(s.id)
            print "Name:", s.name
            print "ID:", s.id
            print "Status:", server.status
            print "Admin Password:", s.adminPass
            print "Networks:", server.networks
        break
