import os
import sys
import argparse
from pprint import pprint
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


##
#Creating dictionary to map providers to images
imageMap = {
    'digitalocean' : {
                     'cent6': '14782952'
                  }
}
##
#Creating dictionary to map providers to locations
locationMap = {
    'digitalocean' : {
                      'ny': 'nyc3'
                    }
}

sizeMap = {
    'digitalocean' : {
                      '512mb': '512mb'
                     }
}

##
#
driverMap = {
    'digitalocean' : {
                     'apikey' : "%s" % os.environ['DIGITAL_OCEAN_API'],
                     'driver' : 'DIGITAL_OCEAN',
                     'options' : {
                                 'backups': False,
                                 'private_networking': False,
                                 'ssh_keys': ['c0:b7:81:d8:23:03:f9:2b:5b:1a:05:c8:e5:ef:11:b7']
                                 } 
                     }
}

actions = [
            'build',
            'list',
            'power-on',
            'power-off',
            'delete',
          ]



##
#Name:arg_check
#Function: Requires a name of the missing argument passed and will exit with error code 20 for missing required argument
def arg_check(argcheck):
	print 'ERROR: Missing argument for %s' % argcheck
	sys.exit(20)



def build(driver, provider, size, image, location, name, options=None):
    imageObj = getImageObj(driver, provider, image)
    locationObj = getLocationObj(driver, provider, location)
    sizeObj = getSizeObj(driver, provider, size)

    if provider == 'digitalocean':
    	node = driver.create_node(name, sizeObj, imageObj, locationObj, ex_create_attr=driverMap[provider]['options'])
    	return node

##
#
def getImageObj( driver, provider, image):
    if provider == 'digitalocean':
        for x in driver.list_images():
            if x.id == image:
                imageObj = x 
                break
        return imageObj

def getLocationObj( driver, provider, location):
    if provider == 'digitalocean':
        for x in driver.list_locations():
            if x.id == location:
                locationObj = x 
                break
        return locationObj

def getSizeObj( driver, provider, size):
    if provider == 'digitalocean':
        for x in driver.list_sizes():
            if x.id == size:
                sizeObj = x 
                break
        return sizeObj
##
#
class __main__():

##
#Building parsed arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help="Build, list, delete, power-on, power-off")
    parser.add_argument('-i', '--image', type=str, help='Image Type')
    parser.add_argument('-n', '--name', type=str, help='Name of node')
    parser.add_argument('-s', '--size', type=str, help='Size of node')
    parser.add_argument('-l', '--location', type=str, help='Location of node')
    parser.add_argument('-d', '--driver', type=str, help='Name of provider(digitalocean, linode, vultr)')
    args = parser.parse_args()



    if not args.action:
		arg_check("ACTION")

    if args.action:
	    if args.action not in actions:
	    	arg_check("Action: %s, not valid please use %s" % (args.action, actions)) 

    if args.action == "build":


    	
    	provider = args.driver
    	image = args.image
    	size = args.size
    	location = args.location
    	name = args.name

        try:
        	if driverMap[provider] is None:
        	    print 'ERROR: %s is not a configured Provider' % provider
        	    sys.exit(1)
        except KeyError:
            print 'ERROR: %s is not a configured Provider' % provider
            sys.exit(1)
##
#Will need to break out into a def
        apikey = driverMap[provider]['apikey']
        if provider == 'digitalocean':
           cls = get_driver(Provider.DIGITAL_OCEAN)
           driver = cls(apikey, api_version='v2')

        if sizeMap[provider][size] is None:
        	print 'ERROR: %s is not a configured size for Provider %s' % (size, provider)
        	sys.exit(1)
        if locationMap[provider][location] is None:
        	print 'ERROR: %s is not a configured location for Provider %s' % (location, provider)
        	sys.exit(1)
        if imageMap[provider][image] is None:
        	print 'ERROR: %s is not a configured Image for Provider %s' % (image, provider)
        	sys.exit(1)
        if args.name is None:
        	print 'ERROR: Please specify a name for new node'
        	sys.exit(1)

    	node = build(driver, provider, sizeMap[provider][size], imageMap[provider][image], locationMap[provider][location], name)
    	print 'Huzzah test: %s' % `node`
