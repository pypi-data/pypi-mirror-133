# This file is part of the SecureFlag Platform.
# Copyright (c) 2022 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sfsdk import log
from sfsdk import authsettings
import boto3
import requests
import time

r = requests.Session()

remote_archive_format = '%s-%s-%d.zip'

hub_url = None
hub_token = None
role = None

def login_to_hub(username, password, management_hub_url):

    global hub_token, hub_url

    hub_url = management_hub_url
    
    source = authsettings.current_source
    r.headers.update(
            authsettings.settings['sources'][source].get('headers', {})
        )

    res = r.post(
            hub_url + '/rest/api/login-developer',
            json = {
                "username": username,
                "password": password
                } 
            )

    hub_repr = 'SecureFlag' if management_hub_url == authsettings.default_hub_url else source

    if res.status_code != 200:
        raise log.FatalMsg("Failed authentication to the %s hub as user %s, check credentials in %s" % (hub_repr, username, authsettings.settings_path))
    else:
        log.success("Logged in the %s hub as user %s" % (hub_repr, username))
        hub_token = res.json()

def get_s3_creds_via_hub():

    res = r.get(
            hub_url + '/rest/user/uploads/credentials',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    return res.json()

def get_arn_via_hub():

    res = r.get(
            hub_url + '/rest/user/uploads/bucket',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    return res.json()['arn']
    
def get_frameworks_via_hub():

    res = r.get(
            hub_url + '/rest/user/frameworks',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            })
    
    if res.status_code == 204:
        return []

    return res.json()

def get_technologies_via_hub():

    res = r.get(
            hub_url + '/rest/user/technologies',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )
    
    if res.status_code == 204:
        return []

    return res.json()

def get_technology_via_hub_by_uuid(uuid):

    res = r.get(
            hub_url + '/rest/user/technologies/%s' % uuid,
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return {}

    return res.json()

def get_vulnerabilities_via_hub():

    res = r.get(
            hub_url + '/rest/user/vulnerabilities',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return []

    return res.json()

def get_vulnerability_via_hub_by_uuid(uuid):

    res = r.get(
            hub_url + '/rest/user/vulnerabilities/%s' % uuid,
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return {}

    return res.json()

def get_exercises_via_hub():

    res = r.get(
            hub_url + '/rest/user/exercises',
            headers = {
                'Authorization': 'Bearer %s' % (hub_token['value'])
            }
        )

    if res.status_code == 204:
        return {}

    return res.json()

def push_to_s3(archive_path, aws_creds, username, aws_arn):

    stsclient = boto3.client(
        'sts',
        aws_access_key_id=aws_creds['accessKeyId'],
        aws_secret_access_key=aws_creds['secretAccessKey'],
        aws_session_token=aws_creds['sessionToken'],
    )
    account_identity = stsclient.get_caller_identity()

    s3client = boto3.client(
        's3',
        aws_access_key_id=aws_creds['accessKeyId'],
        aws_secret_access_key=aws_creds['secretAccessKey'],
        aws_session_token=aws_creds['sessionToken'],
    )

    remote_archive_name = remote_archive_format % (
        account_identity['Account'],
        username,
        int(time.time())
    )

    bucket = aws_arn.split(":")[5]

    try:
        res = s3client.upload_file(
            archive_path + '.zip', 
            bucket, 
            remote_archive_name
        )
    except boto3.exceptions.S3UploadFailedError as e:
        raise log.FatalMsg(str(e))

    log.success('Exercise has been published as %s' % (remote_archive_name))