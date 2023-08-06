import signal
import logging
import requests
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('stayAwake')

# Callback function to try to keep the service alive
def stayAwake(signum, frame):
    logger.info("Attempt to keep the service alive : signal n°{} received".format(signum))

    projectid = requests.get("http://metadata.google.internal/computeMetadata/v1/project/project-id", headers={"Metadata-Flavor" : "Google"})
    regions_req = requests.get("http://metadata.google.internal/computeMetadata/v1/instance/region", headers={"Metadata-Flavor" : "Google"})
    regions = regions_req.text.split("/")
    region = "" 
    if len(regions) <= 4:
        region = regions[3]

    metadata_server_url = "https://{}-run.googleapis.com/apis/serving.knative.dev/v1/namespaces/{}/services/{}".format(region, projectid.text, os.environ['K_SERVICE'])
    token_response = requests.get("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token?scopes=https://www.googleapis.com/auth/cloud-platform", headers={'Metadata-Flavor': 'Google'})
    jwt = token_response.json()
    function_headers = {'Authorization': 'Bearer {}'.format(jwt["access_token"])}
    r = requests.get(metadata_server_url, headers=function_headers)
    if r:
        js = r.json()
        if "status" in js and "url" in js["status"]:
            url =js["status"]["url"]
            metadata_server_url = 'http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience='+ url
            token_response = requests.get(metadata_server_url, headers={'Metadata-Flavor': 'Google'})
            jwtIdToken = token_response.text
            function_headers = {'Authorization': f'Bearer {jwtIdToken}', 'User-Agent': 'CloudRunStayAwake/1.0'}
            r = requests.get(url, headers=function_headers)
            if r:
                logger.info("Successful attempt to keep the service alive and minimizing the cold start")
            else:
                logger.error("Unable to keep alive {}".format(url))
        else:
            logger.error("Unable to find an URL for this service")
    else:
        logger.error("Unable to retrieve Cloud Run url based on : {}".format(metadata_server_url))
