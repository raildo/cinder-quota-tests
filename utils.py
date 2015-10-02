from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as keystoneclient
from subprocess import call, Popen, PIPE

import json
import requests
import testtools

keystone_url = "http://localhost:35357/v3"
nova_url = "http://localhost:8774/v2.1/"
quota_url = "/os-quota-sets/"
project_url = keystone_url + "/projects"
domain_url = keystone_url + "/domains"

def get_token_json(name, project_id):
    return '{ "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "domain": { "name": "DomainX" }, "name": "%s", "password": "secretsecret" } } }, "scope": { "project": { "domain": { "name": "DomainX" }, "id": "%s" } } } }' % (name, project_id)

def default_token_json(name, project_id):
    return '{ "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "domain": { "name": "Default" }, "name": "%s", "password": "d3v5t4ck@LSD1" } } }, "scope": { "project": { "domain": { "name": "Default" }, "name": "%s" } } } }' % (name, project_id)

def domain_json():
    return '{ "domain": { "desctiption": "My new domain", "enabled": true, "name": "DomainX" } }' 

def project_json(name, domain_id, parent_id=None):
    return '{ "project": { "description": "My new project", "domain_id": "%s", "parent_id": "%s", "enabled": true, "name": "%s" } }' % (domain_id, parent_id, name) if parent_id else '{ "project": { "description": "My new project", "domain_id": "%s", "enabled": true, "name": "%s"} }' % (domain_id, name) 


def get_token(token_json):
    token_headers = {'Content-Type': 'application/json'}
    
    r = requests.post(keystone_url + "/auth/tokens",
    	              headers=token_headers,
                      data=token_json)
    return r.headers['x-subject-token']

def get_role(token, name):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}

    r = requests.get(keystone_url + '/roles?name=%s' % name,
           	     headers=headers)
    return json.loads(r._content)['roles'][0]['id']

def create_domain(data, token):
    create_domain_headers = {'X-Auth-Token': token,
                             'Content-Type': 'application/json'}
    
    r = requests.post(domain_url,
                      headers=create_domain_headers,
                      data=data) 
    
    return json.loads(r._content)['domain']['id']

def create_project(data, token):
    create_project_headers = {'X-Auth-Token': token,
                              'Content-Type': 'application/json'}
    
    r = requests.post(project_url,
                      headers=create_project_headers,
                      data=data) 
    
    return json.loads(r._content)['project']['id']
    
def disable_domain(token, domain_id):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    
    data = '{ "domain": {"enabled": false}}'
    
    r = requests.patch(domain_url+ "/%s" % domain_id,
                       headers=headers,
                       data=data) 
    print "Disabled domain %s" % domain_id

def disable_project(token, project_id):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    
    data = '{ "project": {"enabled": false}}'
    
    r = requests.patch(project_url+ "/%s" % project_id,
                       headers=headers,
                       data=data) 
    print "Disabled project %s" % project_id


def delete_domain(token, domain_id):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    
    r = requests.delete(domain_url+ "/%s" % domain_id,
                        headers=headers) 
    print "Deleted domain %s" % domain_id

def delete_project(token, project_id):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    
    r = requests.delete(project_url+ "/%s" % project_id,
                        headers=headers) 
    print "Deleted project %s" % project_id

def create_user(token, user_name, domain_id):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}

    data = '{ "user": {"description": "User", "domain_id": "%s", "email": "jdoe@example.com", "enabled": true, "name": "%s", "password": "secretsecret" } }' % (domain_id, user_name)
    
    r = requests.post(keystone_url + '/users',
                      headers=headers,
                      data=data)


    user_id = json.loads(r._content)['user']['id']
    print "Created user %s in project %s" % (user_id, domain_id)
    return json.loads(r._content)['user']['id']

def grant_user_role(token, user_id, role, projects):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}

    for project in projects:
        grant_role = requests.put(project_url + "/%s/users/%s/roles/%s" % (project, user_id, role),
                                 headers=headers)
        print "Granted role for user %s in project %s" % (user_id, project)

def update_quota(token, project_id, target, value):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}

    data = '{ "quota_set": { "security_groups": %s } }' % value
    r = requests.put(nova_url + project_id + quota_url + target,
		   headers=headers,
		   data=data)
    if 'forbidden' in json.loads(r._content):
	quota = json.loads(r._content)['forbidden']['code']
    elif 'badRequest' in json.loads(r._content):
	quota = json.loads(r._content)['badRequest']['message']
    else:
	quota = json.loads(r._content)['quota_set']['security_groups']
    return quota

def get_quota(token, project_id, target):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}

    r = requests.get(nova_url + project_id + quota_url + target,
		   headers=headers)
    if 'forbidden' in json.loads(r._content):
	quota = json.loads(r._content)['forbidden']['code']
    else:
	quota = json.loads(r._content)['quota_set']['security_groups']
    return quota

def quota_show(token, project_id, target):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}

    r = requests.get(nova_url + project_id + quota_url + target + '?usage=true',
     		      headers=headers)
    quota = json.loads(r._content)['quota_set']['security_groups']
    return quota

def create_security_group(token, project_id, name):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}
    data = '{ "security_group": { "name": "%s" , "description": "test" } }' % name
    r = requests.post(nova_url + project_id + '/os-security-groups', 
		      headers=headers,
		      data=data)
    return json.loads(r._content)['security_group']['id']


class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()
