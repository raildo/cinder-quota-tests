import utils
import sys

def dict_to_list(item, final_list):
    if isinstance(item, dict):
        for key in item:
            final_list.append(key)
            dict_to_list(item[key], final_list)
    return None
    
def tear_down(token, projects, domain):
    for project_id in projects:
        utils.disable_project(token, project_id)
        utils.delete_project(token, project_id)
    utils.disable_domain(token, domain)
    utils.delete_domain(token, domain)

def main():
    f = open('log_test_authorization_cider.txt', 'w')
    original = sys.stdout
    sys.stdout = utils.Tee(sys.stdout, f)

    token = 0
    domain_id, production_project_id, cms_project_id, atlas_project_id = (0, )*4
    computing_project_id, visualisation_project_id, services_project_id = (0, )*3
    operations_project_id = 0
    try:
	token_json = utils.default_token_json('admin', 'demo')
        token = utils.get_token(token_json)
	print '======================================================================='
        print 'This script will use the follow hierarchy to validate the authorization' 
	print 'actions related to Nested Quotas on Cinder'
	print '======================================================================='
	print 'Hierarchy:'
	print '                            Domain_X          '
	print '                               |'
	print '                          ProductionIT - Mike' 
	print '                     /                  \ '
	print '          Jay - CMS                       ATLAS - John'
	print '             /       \                   /       \ '
	print '      Computing   Visualisation   Operations   Services  '
	print '       Walter        Duncan          Eric         Xing'
	print ''
	print 'Actors:'
	print ''
	print 'Mike - Cloud Admin (i.e. role:cloud-admin) of ProductionIT'
	print 'Jay - Manager (i.e. role: project-admin) of Project CMS'
	print 'John - Manager (i.e. role: project-admin) of Project ATLAS'
	print 'Eric - Manager (i.e. role: project-admin) of Project Operations'
	print 'Xing - Manager (i.e. role: project-admin) of Project Services'
	print 'Walter - Manager (i.e. role: project-admin) of Project Computing'
	print 'Duncan - Manager (i.e. role: project-admin) of Project Visualisation'
	print '======================================================================='
	admin_role = utils.get_role(token, 'admin')
        # Create a new domain
 	print 'Creating the domain...'    
        domain = utils.domain_json()
        domain_id = utils.create_domain(domain, token)
        print 'Domain created: %s' % domain_id
	print '======================================================================='
 	print 'Creating the projects...'    
        # Create project ProductionIT
        production_project_json = utils.project_json('ProductionIT', domain_id)
        production_project_id = utils.create_project(production_project_json,
						     token)
        print "ProductionIT created: %s" % production_project_id
	print '======================================================================='
        
        # Create Project CMS 
        cms_project_json = utils.project_json('CMS', domain_id,
					      production_project_id)
        cms_project_id = utils.create_project(cms_project_json, token)
        print "CMS created: %s" % cms_project_id
	print '======================================================================='
        
        # Create Project Atlas
        atlas_project_json = utils.project_json('ATLAS',
					        domain_id,
						production_project_id)
        atlas_project_id = utils.create_project(atlas_project_json, token)
        print "ATLAS created: %s" % atlas_project_id
	print '======================================================================='
        
        # Create Project computing
        computing_project_json = utils.project_json('computing',
						    domain_id,
					            cms_project_id)
        computing_project_id = utils.create_project(computing_project_json,
						    token)
        print "Computing created: %s" % computing_project_id
	print '======================================================================='
     
        # Create Project visualisation
        visual_project_json = utils.project_json('visualisation',
	            			         domain_id,
					         cms_project_id)
        visualisation_project_id = utils.create_project(visual_project_json,
						        token)
        print "Visualisation created: %s" % visualisation_project_id
	print '======================================================================='
     
        # Create Project services
        services_project_json = utils.project_json('services',
						   domain_id,
						   atlas_project_id)
        services_project_id = utils.create_project(services_project_json,
						   token)
        print "Services created: %s" % services_project_id
	print '======================================================================='
     
        # Create Project operations
        operations_project_json = utils.project_json('operations',
						     domain_id,
					             atlas_project_id)
        operations_project_id = utils.create_project(operations_project_json,
						     token)
        print "Operations created: %s" % operations_project_id
	print '======================================================================='
     
        # Creating users
	# Creating and grant admin role to mike in production
 	print 'Creating the users...'    
        mike = utils.create_user(token, 'Mike', domain_id)
	print "Mike: %s" % mike
        utils.grant_user_role(token, mike,
			      admin_role, [production_project_id])

	print '======================================================================='
	# Creating and grant admin role to jay in cms
	jay = utils.create_user(token, 'Jay', domain_id)
	print "Jay: %s" % jay 
        utils.grant_user_role(token, jay,
			      admin_role, [cms_project_id])

	print '======================================================================='
	# Creating and grant admin role to john in atlas
	john = utils.create_user(token, 'John', domain_id)
	print "John: %s" % john 
        utils.grant_user_role(token, john,
			      admin_role, [atlas_project_id])

	print '======================================================================='
	# Creating and grant admin role to eric in operations
	eric = utils.create_user(token, 'Eric', domain_id)
	print "Eric: %s" % eric 
        utils.grant_user_role(token, eric,
			      admin_role, [operations_project_id])

	print '======================================================================='
	# Creating and grant admin role to xing in services
	xing = utils.create_user(token, 'Xing', domain_id)
	print "Xing: %s" % xing 
        utils.grant_user_role(token, xing,
			      admin_role, [services_project_id])

	print '======================================================================='
	# Creating and grant admin role to walter in computing
	walter = utils.create_user(token, 'Walter', domain_id)
	print "Walter: %s" % walter 
        utils.grant_user_role(token, walter,
			      admin_role, [computing_project_id])
	print '======================================================================='

	# Creating and grant admin role to duncan in visualisation
	duncan = utils.create_user(token, 'Duncan', domain_id)
	print "Ducnan: %s" % duncan 
        utils.grant_user_role(token, duncan,
			      admin_role, [visualisation_project_id])
	print '======================================================================='
	print 'Now, we will get a token for Mike in ProductionIT (root project)'
	print 'and show that Mike can update the quota for the root project.'
	print '======================================================================='
	# Get a token for Mike in ProductionIT
	mike_token_json = utils.get_token_json('Mike',
					       production_project_id)
        mike_token = utils.get_token(mike_token_json)
	print 'Token for mike: %s' % mike_token
	print '======================================================================='

	# Update the Production Quota to 100
	print 'Updating the ProductionIT quota for 100...'
	quota_value = 100 
	production_quota = utils.update_quota(mike_token, 
					      production_project_id,
					      production_project_id,
					      quota_value)
	print "Mike updating Production Quota: %s" % production_quota
	print '======================================================================='

	print 'Trying get the default quota for CMS...'
	# Verify that the default quotas for CMS is zero
	cms_quota = utils.get_quota(mike_token,
				    production_project_id,
				    cms_project_id)
	print "Mike getting CMS Quota: %s" % cms_quota
	print '======================================================================='
     
	print 'Trying update the CMS quota for 45...'
	# Update the CMS Quota to 45
	quota_value = 45 
	new_cms_quota = utils.update_quota(mike_token,
					   production_project_id,
					   cms_project_id,
					   quota_value)
	print "Mike updating CMS Quota: %s" % new_cms_quota
	print '======================================================================='
	
	print 'Now, we get a token for Jay in CMS and we will try update the CMS Quota'
	print '======================================================================='
	# Get a token for Jay in CMS
	jay_token_json = utils.get_token_json('Jay', cms_project_id)
        jay_token = utils.get_token(jay_token_json)
	print 'Token for Jay: %s ' % jay_token
	print '======================================================================='

	# Raise a exception when try update the CMS Quota with
	# only a project_admin
	print 'Trying update the CMS quota for 50'
	quota_value = 50 
	forbidden_error = 403
	new_cms_quota = utils.update_quota(jay_token,
					   cms_project_id,
					   cms_project_id,
					   quota_value)
	if new_cms_quota == forbidden_error:
		print 'Error: Cannot update the quota for CMS with user Jay' 

	print '======================================================================='
	# Verify that the default quotas for Visualisation is zero
	cms_quota = utils.get_quota(jay_token, cms_project_id, cms_project_id)
	print "Trying get the CMS Quota: %s" % cms_quota

	print '======================================================================='
	# Raise a exception when try update the Visualisation Quota with a
	# project_admin in a non-root project
	print 'Trying update the Visualisation Quota with Jay'
	quota_value = 10 
	new_visualisation_quota = utils.update_quota(jay_token,
						     cms_project_id,
                                                     visualisation_project_id,
					             quota_value)
	if new_visualisation_quota == forbidden_error:
	    print 'Error: Cannot update the quota for Visualisation with user Jay' 
	else:
	    print 'New Visualisation Quota: %s ' % new_visualisation_quota 
	print '======================================================================='

	# Raise a exception when try get the Visualisation Quota with a
	# project_admin in a non-root project
	print 'Trying get the Visualisation Quota with Jay'
	visualisation_quota = utils.get_quota(jay_token,
					      cms_project_id,
					      visualisation_project_id)
	if visualisation_quota == forbidden_error:
   	    print 'Error: Cannot get the quota for Visualisation with user Jay' 
	else:
	    print 'Get Visualisation Quota: %s ' % new_visualisation_quota 
	print '======================================================================='
	# Raise a exception when try get the Atlas Quota with a project_admin
	# in a non-root project
	atlas_quota = utils.get_quota(jay_token,
				      cms_project_id,
				      atlas_project_id)
	if atlas_quota == forbidden_error:
		print 'Error: Cannot get the quota for Atlas with user Jay' 
	print '======================================================================='
	
	# Get a token for Duncan in Visualisation
	duncan_token_json = utils.get_token_json('Duncan',
						 visualisation_project_id)
        duncan_token = utils.get_token(duncan_token_json)

	print 'Get a token for Duncan in Visualisation: %s ' % duncan_token
	# Raise a exception when try get the Atlas Quota with a project_admin
	# in a subproject
	cms_quota = utils.get_quota(duncan_token,
				    visualisation_project_id,
				    cms_project_id)
	if cms_quota == forbidden_error:
   	    print 'Error: Cannot get the quota for CMS with user Duncan' 
	print '======================================================================='
	
	# Raise a exception when try update the Visualisation Quota
	# with a project_admin in a non-root project
	quota_value = 10 
	new_visualisation_quota = utils.update_quota(duncan_token,
						     visualisation_project_id,
						     visualisation_project_id,
						     quota_value)
	if new_visualisation_quota == forbidden_error:
	    print ('Cannot update the quota for Visualisation with user Duncan')
	print '======================================================================='

	# Verify that the default quotas for Visualisation is zero
	visual_quota = utils.get_quota(duncan_token,
	        		       visualisation_project_id,
				       visualisation_project_id)
	print ('Duncan getting the Visualisation Quota: %s' % visual_quota)
	print '======================================================================='
	print 'Clean up...'

    except Exception as e:
	print 'Error'
        tear_down(token, [production_project_id,
	          cms_project_id, 
                  atlas_project_id,
                  computing_project_id,
                  visualisation_project_id,
                  services_project_id,
                  operations_project_id], domain_id)
    	f.close()
        print e 
    tear_down(token, [production_project_id,    
              cms_project_id, 
              atlas_project_id,
	      computing_project_id,
	      visualisation_project_id,
	      services_project_id,
	      operations_project_id], domain_id)
    f.close()

if __name__ == "__main__":
    main()
