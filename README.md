# python_sis_uploader
This is a simple proof of concept python script to upload a feed file to a Blackboard Learn SIS Data Integration Endpoint.

This was written with Python 2.7 in mind, should work in Python 3.6 as well. If not, please report the issue.

Example usage

# IMS-XML example
```
[hxnguyen@HXNGUYEN450 py_test]$ python sis_uploader.py -s blackboard.local -u 54939fb0-da12-4cab-a1b2-e5c9f807db47 -p '!33tP@ssw0rd' -t ims-xml -f feedfile.xml
Starting upload to blackboard.local
Upload completed!
You can check on the status of SIS Processing via https://blackboard.local/webapps/bb-data-integration-ims-xml-BBLEARN/endpoint/dataSetStatus/13cbea95068c49b086a7d9b4ed7502e6
```

# Flatfile example
```
[hxnguyen@HXNGUYEN450 py_test]$ python sis_uploader.py -s blackboard.local -u 8c19ab94-d3ea-48c9-b20d-e4aa8c2fe430 -p simplePassword -t flatfile -d person -o store -f feedfile.txt
Starting upload to blackboard.local
Upload completed!
You can check on the status of SIS Processing via https://blackboard.local/webapps/bb-data-integration-flatfile-BBLEARN/endpoint/dataSetStatus/415e53000d4a45cb85ee5756062f182d
```

For more option information, run the help command

```
python sis_uploader.py -h
```
