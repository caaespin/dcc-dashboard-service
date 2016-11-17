import json
import urllib2

'''
TODO:
* How to capture stdout/stderr?
'''

def get_error(server, job_id):    
    error_url = server + 'fetch_error?data=%7B%22task_id%22%3A%22' + job_id + '%22%7D'
    req_data = urllib2.Request(error_url)
    response_data = urllib2.urlopen(req_data)
    text_data = response_data.read()
    json_data = json.loads(text_data)

    err_parameters = json_data['response']
    return err_parameters['error']

server = 'http://localhost:8082/api/'

running_url   = server + 'task_list?data=%7B%22status%22%3A%22RUNNING%22%2C%22upstream_status%22%3A%22%22%2C%22search%22%3A%22%22%7D'
batch_url     = server + 'task_list?data=%7B%22status%22%3A%22BATCH_RUNNING%22%2C%22upstream_status%22%3A%22%22%2C%22search%22%3A%22%22%7D'
failed_url    = server + 'task_list?data=%7B%22status%22%3A%22FAILED%22%2C%22upstream_status%22%3A%22%22%2C%22search%22%3A%22%22%7D'
upfail_url    = server + 'task_list?data=%7B%22status%22%3A%22PENDING%22%2C%22upstream_status%22%3A%22UPSTREAM_FAILED%22%2C%22search%22%3A%22%22%7D'
disable_url   = server + 'task_list?data=%7B%22status%22%3A%22DISABLED%22%2C%22upstream_status%22%3A%22%22%2C%22search%22%3A%22%22%7D'
updisable_url = server + 'task_list?data=%7B%22status%22%3A%22PENDING%22%2C%22upstream_status%22%3A%22UPSTREAM_DISABLED%22%2C%22search%22%3A%22%22%7D'
pending_url   = server + 'task_list?data=%7B%22status%22%3A%22PENDING%22%2C%22upstream_status%22%3A%22%22%2C%22search%22%3A%22%22%7D'
done_url      = server + 'task_list?data=%7B%22status%22%3A%22DONE%22%2C%22upstream_status%22%3A%22%22%2C%22search%22%3A%22%22%7D'


list_of_URLs = [running_url, batch_url, failed_url, upfail_url, 
                disable_url, updisable_url, pending_url, done_url]

relevant_attributes = ["status", "name", "start_time", "params"]

required_parameters = ["project", "donor_id", "sample_id", "pipeline_name"]

for URL in list_of_URLs:
    name = URL[62:]
    suffix = ''
    if 'UPSTREAM' in name:
        if 'FAILED' in name:
            name = 'UPSTREAM_FAILED'
        else:
            name = 'UPSTREAM_DISABLED'
    else:
        name = name.split('%')[0] + suffix
    print "\n", name

    error_text = None

    # Retrieve api tool dump from URL and read it into json_tools
    req = urllib2.Request(URL)
    response = urllib2.urlopen(req)
    text_tools = response.read()
    json_tools = json.loads(text_tools)

    job_list = json_tools['response']

    if not job_list:
        # Just skip an empty response
        continue

    for job_id in job_list:

        # Get error information
        if job_list[job_id]['status'] == "FAILED":
            error_text = get_error(server, job_id)
            
        for attr in relevant_attributes:

            node = job_list[job_id][attr]

            if attr == 'params':
                for parameter in node:
                    print parameter, node[parameter]
            else:
                print attr, node

        print "Error:", error_text
        print "\n"



