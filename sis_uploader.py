# Python Script to upload Feed File to SIS Data Integration Endpoints
# supports Snapshot Flat File, Snapshot XML, and IMS XML 1.1
# example command
# python sis_uploader.py -s blackboard.community.edu -u username -p 'l33tP@ssw0rd!' -t ims-xml -f feedfile.xml
import httplib2
import re
import base64
import sys
import argparse
import codecs


# CONFIGURABLE
###################################################################################################################################################
# schema either, bb_bb60 or BBLEARN, verify on your environment. Check the HTTP Endpoints for your Data Integration
schema = "BBLEARN"


# DO NOT EDIT BELOW HERE
###################################################################################################################################################
def formatInput(arg_str):
    return codecs.decode(str(arg_str), 'utf8')


# ARGUMENTS
###################################################################################################################################################
data_intgr_type = [ 'flatfile', 'ss-xml', 'ims-xml' ]
flatfile_objects = [ 'course', 'courseassociation', 'coursecategory', 'coursecategorymembership',
                    'membership', 'standardsassociation', 'node', 'associateobserver', 'organization',
                    'organizationassociation', 'organizationcategory', 'organizationcategorymembership',
                    'organizationmembership', 'person', 'term', 'userassociation', 'secondaryinstrole' ]
flatfile_operations = [ 'store', 'refresh', 'refreshlegacy', 'delete' ]
# Argument Parser
parser = argparse.ArgumentParser(description='This is a simple Data Integration Feed File Uploader Program using Python.')
parser.add_argument('--server','-s',help='Server FQDN i.e.: blackboard.test.edu',required=True)
parser.add_argument('--username','-u',help='Data Integration Username',required=True)
parser.add_argument('--password','-p',type=formatInput,help='Data Integration Password, if you have special characters, please encapsulate within single quotes',required=True)
parser.add_argument('--type','-t',help='Data Integration Type',choices=data_intgr_type,required=True)
parser.add_argument('--feed','-f',help='Feed File',required=True)
parser.add_argument('--data','-d',default='',help='Flatfile Data Type',choices=flatfile_objects)
parser.add_argument('--operation','-o',default='',help='Flatfile Operation',choices=flatfile_operations)
args = parser.parse_args()

# FUNCTIONS
###################################################################################################################################################

# check for additional arguments if using --type = flatfile
def dataIntgrTypeCheck():
    # if snapshot flatfile
    if ( args.type == "flatfile" ): 
        # print("Checking for additional arguments when using flatfile")
        if ( args.data == '' ):
            print("flatfile --data cannot be empty")
            sys.exit(1)
        if ( args.operation == '' ):
            print("flatfile --operation cannot be empty")
            sys.exit(1)

# build the Data Integration URL Endpoint
def formURLEndpoint():
    # forming the URL ENDPOINT
    endpoint_url = "https://" + args.server.lower() + "/webapps/bb-data-integration-" + args.type.lower() + "-" + schema + "/endpoint"

    # if flatfile, add the additional flatfile data type
    if ( args.type == "flatfile" and args.data != "" ):
        endpoint_url += "/" + args.data.lower()

    # adds the operation type for flatfile and ss-xml (snapshot xml)
    if ( args.type == "flatfile" or args.type == "ss-xml" and args.operation != ""):
        endpoint_url += "/" + args.operation.lower()

    # for debugging uncomment
    #print("ENDPOINT_URL: {}".format(endpoint_url))
    return endpoint_url

# upload feed file to endpoint url
def uploadFeedFile(feed_file):
    print("Starting upload to {}".format(args.server))

    # specify Content-Type, base don snapshot flatfile or other
    if ( args.type == "flatfile" ):
        content_type = "text/plain"
    else:
        content_type ="text/xml"

    # needed to add the following due to CERTIFICATE_VERIFY_FAILED, if using Self Signed Certs
    h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
    # auth parameters i.e. data integration username + password
    auth = base64.encodestring( args.username + ':' + args.password )

    # sending POST request
    resp, content = h.request( formURLEndpoint(), "POST", body=feed_file, headers={ "Content-Type": content_type, "Authorization": "Basic " + auth })
    
    # verify status code,
    if (resp.status != 200):
        print("Something went wrong, STATUS CODE: {}".format(resp.status))
        sys.exit(1)

    reference_code = re.search(r"(\w{32})", str(content)).group(0)
    checkendpoint_url = "https://" + args.server.lower() + "/webapps/bb-data-integration-" + args.type.lower() + "-" + schema + "/endpoint/dataSetStatus/" + reference_code

    # tell users how they can check the status
    print("Upload completed!")
    print("You can check on the status of SIS Processing via {}".format(checkendpoint_url))

# main
def mainProg():
    try:
        with open( args.feed, 'rb' ) as f:
            # call our upload process
            uploadFeedFile( f.read() )
            f.close()
    except IOError:
        print ( "feed file doesn't exist, exting..." )
        sys.exit(1)

###################################################################################################################################################
# argument check, based on flatfile vs other to see if additional arguments are set or not
dataIntgrTypeCheck()
# main call
mainProg()