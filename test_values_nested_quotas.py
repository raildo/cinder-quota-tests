import utils
import sqlalchemy

admin_role = '33971aadbc144a63a8ba727560dfcb58'
member_role = 'bff83b7970c34528b2ad80afd0af4c4f'

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
	quota_show_production = utils.quota_show(mike_token, production_project_id, production_project_id)
	print '======== ---- ======='
	print "Production Quota: %s" % quota_show_production
	print '======== ---- ======='

	# Update the CMS Quota to 40
	quota_value = 40 
	cms_quota = utils.update_quota(mike_token, 
				       production_project_id,
				       cms_project_id,
				       quota_value)
	quota_show_production = utils.quota_show(mike_token, production_project_id, production_project_id)
	quota_show_cms = utils.quota_show(mike_token, production_project_id, cms_project_id)
	print "Production Quota: %s" % quota_show_production
	print "CMS Quota: %s" % quota_show_cms
	print '======== ---- ======='

	# Update the Atlas Quota to 30 
	quota_value = 30 
	atlas_quota = utils.update_quota(mike_token, 
				         production_project_id,
				         atlas_project_id,
				         quota_value)
	quota_show_production = utils.quota_show(mike_token, production_project_id, production_project_id)
	quota_show_cms = utils.quota_show(mike_token, production_project_id, cms_project_id)
	quota_show_atlas = utils.quota_show(mike_token, production_project_id, atlas_project_id)
	print "Production Quota: %s" % quota_show_production
	print "CMS Quota: %s" % quota_show_cms
	print "Atlas Quota: %s" % quota_show_atlas
	print '======== ---- ======='

	# Update the Computing Quota to 15 
	quota_value = 15 
	computing_quota = utils.update_quota(mike_token, 
				             production_project_id,
				             computing_project_id,
				             quota_value)
	quota_show_production = utils.quota_show(mike_token, production_project_id, production_project_id)
	quota_show_cms = utils.quota_show(mike_token, production_project_id, cms_project_id)
	quota_show_computing = utils.quota_show(mike_token, production_project_id, computing_project_id)
	print "Production Quota: %s" % quota_show_production
	print "CMS Quota: %s" % quota_show_cms
	print "Atlas Quota: %s" % quota_show_atlas
	print "Computing Quota: %s" % quota_show_computing
	print '======== ---- ======='

	# Update the visualisaton Quota to 15 
	quota_value = 15 
	visualisation_quota = utils.update_quota(mike_token, 
				            	 production_project_id,
				             	 visualisation_project_id,
				             	 quota_value)
	quota_show_production = utils.quota_show(mike_token, production_project_id, production_project_id)
	quota_show_cms = utils.quota_show(mike_token, production_project_id, cms_project_id)
	quota_show_computing = utils.quota_show(mike_token, production_project_id, computing_project_id)
	quota_show_visualisation = utils.quota_show(mike_token, production_project_id, visualisation_project_id)
	print "Production Quota: %s" % quota_show_production
	print "CMS Quota: %s" % quota_show_cms
	print "Atlas Quota: %s" % quota_show_atlas
	print "Computing Quota: %s" % quota_show_computing
	print "Visualisation Quota: %s" % quota_show_visualisation
	print '======== ---- ======='

	# Update the services Quota to 10 
	quota_value = 10 
	services_quota = utils.update_quota(mike_token, 
				           production_project_id,
				           services_project_id,
				           quota_value)
	quota_show_production = utils.quota_show(mike_token, production_project_id, production_project_id)
	quota_show_cms = utils.quota_show(mike_token, production_project_id, cms_project_id)
	quota_show_computing = utils.quota_show(mike_token, production_project_id, computing_project_id)
	quota_show_visualisation = utils.quota_show(mike_token, production_project_id, visualisation_project_id)
	quota_show_atlas = utils.quota_show(mike_token, production_project_id, atlas_project_id)
	quota_show_services = utils.quota_show(mike_token, production_project_id, services_project_id)
	print "Production Quota: %s" % quota_show_production
	print "CMS Quota: %s" % quota_show_cms
	print "Atlas Quota: %s" % quota_show_atlas
	print "Computing Quota: %s" % quota_show_computing
	print "Visualisation Quota: %s" % quota_show_visualisation
	print "Service Quota: %s" % quota_show_services
	print '======== ---- ======='

	# Update the operations Quota to 10 
	quota_value = 10 
	operations_quota = utils.update_quota(mike_token, 
				           production_project_id,
				           operations_project_id,
				           quota_value)
	quota_show_production = utils.quota_show(mike_token, production_project_id, production_project_id)
	quota_show_cms = utils.quota_show(mike_token, production_project_id, cms_project_id)
	quota_show_computing = utils.quota_show(mike_token, production_project_id, computing_project_id)
	quota_show_visualisation = utils.quota_show(mike_token, production_project_id, visualisation_project_id)
	quota_show_atlas = utils.quota_show(mike_token, production_project_id, atlas_project_id)
	quota_show_services = utils.quota_show(mike_token, production_project_id, services_project_id)
	quota_show_operations = utils.quota_show(mike_token, production_project_id, operations_project_id)
	print "Production Quota: %s" % quota_show_production
	print "CMS Quota: %s" % quota_show_cms
	print "Atlas Quota: %s" % quota_show_atlas
	print "Computing Quota: %s" % quota_show_computing
	print "Visualisation Quota: %s" % quota_show_visualisation
	print "Service Quota: %s" % quota_show_services
	print "Operations Quota: %s" % quota_show_operations
	print '======== ---- ======='
	# Update the CMS Quota to 40
	quota_value = 71 
	print 'Trying update the CMS quota for 71...'
	cms_quota = utils.update_quota(mike_token, 
				       production_project_id,
				       cms_project_id,
				       quota_value)
	print "CMS Quota: Error: %s" % cms_quota
	print "Creating Volumes..."
	# Get a token for Jay in CMS
	jay_token_json = utils.get_token_json('Jay', cms_project_id)
        jay_token = utils.get_token(jay_token_json)

	for i in range(0,10):
	    utils.create_volume(jay_token, cms_project_id)
	quota_show_cms = utils.quota_show(jay_token, cms_project_id, cms_project_id)
	print "CMS Quota: %s" % quota_show_cms
	print "Trying update the computing quota to 16..."
	quota_value = 16 
	computing_quota = utils.update_quota(mike_token, 
				       production_project_id,
				       computing_project_id,
				       quota_value)
	print "Computing Quota: Error: %s" % computing_quota

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
