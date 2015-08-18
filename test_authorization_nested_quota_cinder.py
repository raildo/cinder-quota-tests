import utils

admin_role = '33971aadbc144a63a8ba727560dfcb58'
member_role = 'bff83b7970c34528b2ad80afd0af4c4f'

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
    token = 0
    domain_id, production_project_id, cms_project_id, atlas_project_id = (0, )*4
    computing_project_id, visualisation_project_id, services_project_id = (0, )*3
    operations_project_id = 0
    try:
	token_json = utils.default_token_json('admin', 'demo')
        token = utils.get_token(token_json)
     
        # Create a new domain
        domain = utils.domain_json()
        domain_id = utils.create_domain(domain, token)
        print 'Domain: %s' % domain_id
     
        # Create project ProductionIT
        production_project_json = utils.project_json('ProductionIT', domain_id)
        production_project_id = utils.create_project(production_project_json,
						     token)
        print "ProductionIT: %s" % production_project_id
        
        # Create Project CMS 
        cms_project_json = utils.project_json('CMS', domain_id,
					      production_project_id)
        cms_project_id = utils.create_project(cms_project_json, token)
        print "CMS: %s" % cms_project_id
        
        # Create Project Atlas
        atlas_project_json = utils.project_json('ATLAS',
					        domain_id,
						production_project_id)
        atlas_project_id = utils.create_project(atlas_project_json, token)
        print "ATLAS: %s" % atlas_project_id
        
        # Create Project computing
        computing_project_json = utils.project_json('computing',
						    domain_id,
					            cms_project_id)
        computing_project_id = utils.create_project(computing_project_json,
						    token)
        print "Computing: %s" % computing_project_id
     
        # Create Project visualisation
        visual_project_json = utils.project_json('visualisation',
	            			         domain_id,
					         cms_project_id)
        visualisation_project_id = utils.create_project(visual_project_json,
						        token)
        print "Visualisation: %s" % visualisation_project_id
     
        # Create Project services
        services_project_json = utils.project_json('services',
						   domain_id,
						   atlas_project_id)
        services_project_id = utils.create_project(services_project_json,
						   token)
        print "Services: %s" % services_project_id
     
        # Create Project operations
        operations_project_json = utils.project_json('operations',
						     domain_id,
					             atlas_project_id)
        operations_project_id = utils.create_project(operations_project_json,
						     token)
        print "Operations: %s" % operations_project_id
     
        # Creating users
	# Creating and grant admin role to mike in production
        mike = utils.create_user(token, 'Mike', domain_id)
	print "Mike: %s" % mike
        utils.grant_user_role(token, mike,
			      admin_role, [production_project_id])

	# Creating and grant admin role to jay in cms
	jay = utils.create_user(token, 'Jay', domain_id)
	print "Jay: %s" % jay 
        utils.grant_user_role(token, jay,
			      admin_role, [cms_project_id])

	# Creating and grant admin role to john in atlas
	john = utils.create_user(token, 'John', domain_id)
	print "John: %s" % john 
        utils.grant_user_role(token, john,
			      admin_role, [atlas_project_id])

	# Creating and grant admin role to eric in operations
	eric = utils.create_user(token, 'Eric', domain_id)
	print "Eric: %s" % eric 
        utils.grant_user_role(token, eric,
			      admin_role, [operations_project_id])

	# Creating and grant admin role to xing in services
	xing = utils.create_user(token, 'Xing', domain_id)
	print "Xing: %s" % xing 
        utils.grant_user_role(token, xing,
			      admin_role, [services_project_id])

	# Creating and grant admin role to walter in computing
	walter = utils.create_user(token, 'Walter', domain_id)
	print "Walter: %s" % walter 
        utils.grant_user_role(token, walter,
			      admin_role, [computing_project_id])

	# Creating and grant admin role to duncan in visualisation
	duncan = utils.create_user(token, 'Duncan', domain_id)
	print "Ducnan: %s" % duncan 
        utils.grant_user_role(token, duncan,
			      admin_role, [visualisation_project_id])

	# Get a token for Mike in ProductionIT
	mike_token_json = utils.get_token_json('Mike',
					       production_project_id)
        mike_token = utils.get_token(mike_token_json)

	# Update the Prduction Quota to 100
	quota_value = 100 
	production_quota = utils.update_quota(mike_token, 
					      production_project_id,
					      production_project_id,
					      quota_value)
	print "Mike updating Production Quota: %s" % production_quota

	# Verify that the default quotas for CMS is zero
	cms_quota = utils.get_quota(mike_token,
				    production_project_id,
				    cms_project_id)
	print "Mike getting CMS Quota: %s" % cms_quota
     
	# Update the CMS Quota to 45
	quota_value = 45 
	new_cms_quota = utils.update_quota(mike_token,
					   production_project_id,
					   cms_project_id,
					   quota_value)
	print "Mike updating CMS Quota: %s" % new_cms_quota

	# Get a token for Jay in CMS
	jay_token_json = utils.get_token_json('Jay', cms_project_id)
        jay_token = utils.get_token(jay_token_json)

	# Raise a exception when try update the CMS Quota with
	# only a project_admin
	quota_value = 50 
	forbidden_error = 403
	new_cms_quota = utils.update_quota(jay_token,
					   cms_project_id,
					   cms_project_id,
					   quota_value)
	if new_cms_quota == forbidden_error:
		print 'Cannot update the quota for CMS with user Jay' 

	# Verify that the default quotas for Visualisation is zero
	cms_quota = utils.get_quota(jay_token, cms_project_id, cms_project_id)
	print "Jay getting the CMS Quota: %s" % cms_quota

	# Raise a exception when try update the Visualisation Quota with a
	# project_admin in a non-root project
	quota_value = 10 
	new_visualisation_quota = utils.update_quota(jay_token,
						     cms_project_id,
                                                     visualisation_project_id,
					             quota_value)
	if new_visualisation_quota == forbidden_error:
		print 'Cannot update the quota for Visualisation with user Jay' 

	# Raise a exception when try get the Visualisation Quota with a
	# project_admin in a non-root project
	visualisation_quota = utils.get_quota(jay_token,
					      cms_project_id,
					      visualisation_project_id)
	if visualisation_quota == forbidden_error:
		print 'Cannot get the quota for Visualisation with user Jay' 

	# Raise a exception when try get the Atlas Quota with a project_admin
	# in a non-root project
	atlas_quota = utils.get_quota(jay_token,
				      cms_project_id,
				      atlas_project_id)
	if atlas_quota == forbidden_error:
		print 'Cannot get the quota for Atlas with user Jay' 
	
	# Get a token for Duncan in Visualisation
	duncan_token_json = utils.get_token_json('Duncan',
						 visualisation_project_id)
        duncan_token = utils.get_token(duncan_token_json)

	# Raise a exception when try get the Atlas Quota with a project_admin
	# in a subproject
	cms_quota = utils.get_quota(duncan_token,
				    visualisation_project_id,
				    cms_project_id)
	if cms_quota == forbidden_error:
		print 'Cannot get the quota for CMS with user Duncan' 
	
	# Raise a exception when try update the Visualisation Quota
	# with a project_admin in a non-root project
	quota_value = 10 
	new_visualisation_quota = utils.update_quota(duncan_token,
						     visualisation_project_id,
						     visualisation_project_id,
						     quota_value)
	if new_visualisation_quota == forbidden_error:
	    print ('Cannot update the quota for Visualisation with user Duncan')

	# Verify that the default quotas for Visualisation is zero
	visual_quota = utils.get_quota(duncan_token,
	        		       visualisation_project_id,
				       visualisation_project_id)
	print ('Duncan getting the Visualisation Quota: %s' % visual_quota)

    except Exception as e:
	print 'Error'
        tear_down(token, [production_project_id,
	          cms_project_id, 
                  atlas_project_id,
                  computing_project_id,
                  visualisation_project_id,
                  services_project_id,
                  operations_project_id], domain_id)
        print e 
    tear_down(token, [production_project_id,    
              cms_project_id, 
              atlas_project_id,
	      computing_project_id,
	      visualisation_project_id,
	      services_project_id,
	      operations_project_id], domain_id)

if __name__ == "__main__":
    main()
