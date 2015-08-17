from keystoneclient.auth.identity import v3
from keystoneclient import session
from keystoneclient.v3 import client as keystoneclient
from subprocess import call, Popen, PIPE
import requests
import json
import testtools


keystone_url = "http://10.4.13.14:35357/v3"
cinder_url = "http://10.4.13.14:8776/v2/"
quota_url = "/os-quota-sets/"
project_url = keystone_url + "/projects"
domain_url = keystone_url + "/domains"
admin_role = '33971aadbc144a63a8ba727560dfcb58'
member_role = 'bff83b7970c34528b2ad80afd0af4c4f'

def get_token_json(name, project_id):
    return '{ "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "domain": { "name": "Domain" }, "name": "%s", "password": "secretsecret" } } }, "scope": { "project": { "domain": { "name": "Domain" }, "id": "%s" } } } }' % (name, project_id)

def default_token_json(name, project_id):
    return '{ "auth": { "identity": { "methods": [ "password" ], "password": { "user": { "domain": { "name": "Default" }, "name": "%s", "password": "nomoresecrete" } } }, "scope": { "project": { "domain": { "name": "Default" }, "name": "%s" } } } }' % (name, project_id)

def domain_json():
    return '{ "domain": { "desctiption": "My new domain", "enabled": true, "name": "Domain" } }' 

def project_json(name, domain_id, parent_id=None):
    return '{ "project": { "description": "My new project", "domain_id": "%s", "parent_id": "%s", "enabled": true, "name": "%s" } }' % (domain_id, parent_id, name) if parent_id else '{ "project": { "description": "My new project", "domain_id": "%s", "enabled": true, "name": "%s"} }' % (domain_id, name) 


def get_token(token_json):
    token_headers = {'Content-Type': 'application/json'}
    
    r = requests.post(keystone_url + "/auth/tokens",
    	              headers=token_headers,
                      data=token_json)
    return r.headers['x-subject-token']

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

    data = '{ "quota_set": { "snapshots": %s } }' % value
    r = requests.put(cinder_url + project_id + quota_url + target,
		   headers=headers,
		   data=data)
    quota = json.loads(r._content)['quota_set']['snapshots']
    return quota

def get_quota(token, project_id, target):
    headers = {'X-Auth-Token': token,
               'Content-Type': 'application/json'}

    r = requests.get(cinder_url + project_id + quota_url + target,
		   headers=headers)
    quota = json.loads(r._content)['quota_set']['snapshots']
    return quota


def dict_to_list(item, final_list):
    if isinstance(item, dict):
        for key in item:
            final_list.append(key)
            dict_to_list(item[key], final_list)
    return None
    
def tear_down(token, projects, domain):
    for project_id in projects:
        disable_project(token, project_id)
        delete_project(token, project_id)
    disable_domain(token, domain)
    delete_domain(token, domain)

def main():
    token = 0
    domain_id, production_project_id, cms_project_id, atlas_project_id = (0, )*4
    computing_project_id, visualisation_project_id, services_project_id = (0, )*3
    operations_project_id = 0
    try:
	token_json = default_token_json('admin', 'demo')
        token = get_token(token_json)
     
        # Create a new domain
        domain = domain_json()
        domain_id = create_domain(domain, token)
        print 'Domain: %s' % domain_id
     
        # Create project ProductionIT
        production_project_json = project_json('ProductionIT', domain_id)
        production_project_id = create_project(production_project_json, token)
        print "ProductionIT: %s" % production_project_id
        
        # Create Project CMS 
        cms_project_json = project_json('CMS', domain_id, production_project_id)
        cms_project_id = create_project(cms_project_json, token)
        print "CMS: %s" % cms_project_id
        
        # Create Project Atlas
        atlas_project_json = project_json('ATLAS', domain_id, production_project_id)
        atlas_project_id = create_project(atlas_project_json, token)
        print "ATLAS: %s" % atlas_project_id
        
        # Create Project computing
        computing_project_json = project_json('computing', domain_id, cms_project_id)
        computing_project_id = create_project(computing_project_json, token)
        print "Computing: %s" % computing_project_id
     
        # Create Project visualisation
        visualisation_project_json = project_json('visualisation', domain_id,  cms_project_id)
        visualisation_project_id = create_project(visualisation_project_json, token)
        print "Visualisation: %s" % visualisation_project_id
     
        # Create Project services
        services_project_json = project_json('services', domain_id, atlas_project_id)
        services_project_id = create_project(services_project_json, token)
        print "Services: %s" % services_project_id
     
        # Create Project operations
        operations_project_json = project_json('operations', domain_id, atlas_project_id)
        operations_project_id = create_project(operations_project_json, token)
        print "Operations: %s" % operations_project_id
     
        # Creating users
	# Creating and grant admin role to mike in production
        mike = create_user(token, 'Mike', domain_id)
	print "Mike: %s" % mike
        grant_user_role(token, mike, admin_role, [production_project_id])

	# Creating and grant admin role to jay in cms
	jay = create_user(token, 'Jay', domain_id)
	print "Jay: %s" % jay 
        grant_user_role(token, jay, admin_role, [cms_project_id])

	# Creating and grant admin role to john in atlas
	john = create_user(token, 'John', domain_id)
	print "John: %s" % john 
        grant_user_role(token, john, admin_role, [atlas_project_id])

	# Creating and grant admin role to eric in operations
	eric = create_user(token, 'Eric', domain_id)
	print "Eric: %s" % eric 
        grant_user_role(token, eric, admin_role, [operations_project_id])

	# Creating and grant admin role to xing in services
	xing = create_user(token, 'Xing', domain_id)
	print "Xing: %s" % xing 
        grant_user_role(token, xing, admin_role, [services_project_id])

	# Creating and grant admin role to walter in computing
	walter = create_user(token, 'Walter', domain_id)
	print "Walter: %s" % walter 
        grant_user_role(token, walter, admin_role, [computing_project_id])

	# Creating and grant admin role to duncan in visualisation
	duncan = create_user(token, 'Duncan', domain_id)
	print "Ducnan: %s" % duncan 
        grant_user_role(token, duncan, admin_role, [visualisation_project_id])

	# Get a token for Mike in ProductionIT
	mike_token_json = get_token_json('Mike', production_project_id)
        mike_token = get_token(mike_token_json)

	# Update the Prduction Quota to 100
	quota_value = 100 
	production_quota = update_quota(mike_token, production_project_id, production_project_id, quota_value)
	print "New Production Quota: %s" % production_quota

	# Verify that the default quotas for CMS is zero
	cms_quota = get_quota(mike_token, production_project_id, cms_project_id)
	print "Get Default CMS Quota: %s" % cms_quota
     
	# Update the CMS Quota to 45
	quota_value = 45 
	new_cms_quota = update_quota(mike_token, production_project_id, cms_project_id, quota_value)
	print "New CMS Quota: %s" % new_cms_quota

    except Exception:
        tear_down(token, [production_project_id,
	          cms_project_id, 
                  atlas_project_id,
                  computing_project_id,
                  visualisation_project_id,
                  services_project_id,
                  operations_project_id], domain_id)
	raise Exception
         
    tear_down(token, [production_project_id,    
              cms_project_id, 
              atlas_project_id,
	      computing_project_id,
	      visualisation_project_id,
	      services_project_id,
	      operations_project_id], domain_id)

if __name__ == "__main__":
    main()
