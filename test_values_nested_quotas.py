import utils
import sqlalchemy
import sys

def tear_down(token, projects, domain):
    for project_id in projects:
        utils.disable_project(token, project_id)
        utils.delete_project(token, project_id)
    utils.disable_domain(token, domain)
    utils.delete_domain(token, domain)

def main():
    f = open('log_test_values_cider.txt', 'w')
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
        print 'This script will use the follow hierarchy to validate the quota values' 
	print 'related to Nested Quotas on Cinder'
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
     
	admin_role = utils.get_role(token, 'admin')
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
	print 'and show that the quota calculation in the hierarchy works well.'
	print '======================================================================='
	# Get a token for Mike in ProductionIT
	mike_token_json = utils.get_token_json('Mike',
					       production_project_id)
        mike_token = utils.get_token(mike_token_json)
	print 'Token for mike: %s' % mike_token
	print '======================================================================='

	# Update the Prduction Quota to 100
	print 'Updating the ProductionIT quota for 100...'
	quota_value = 100 
	production_quota = utils.update_quota(mike_token, 
					      production_project_id,
					      production_project_id,
					      quota_value)
	quota_show_production = utils.quota_show(mike_token,
						 production_project_id,
						 production_project_id)
	print '======================================================================='
	print "Production Quota: %s" % quota_show_production
	print '======================================================================='
	# Update the CMS Quota to 40
	print 'Updating the CMS quota for 40...'
	quota_value = 40 
	cms_quota = utils.update_quota(mike_token, 
				       production_project_id,
				       cms_project_id,
				       quota_value)
	quota_show_production = utils.quota_show(mike_token,
						 production_project_id, 
						 production_project_id)
	quota_show_cms = utils.quota_show(mike_token, production_project_id, cms_project_id)
	print 'Verify that allocated ProductionIT quota was updated to 40'
	print "Production Quota: %s" % quota_show_production
	print "CMS Quota: %s" % quota_show_cms
	print '======================================================================='
	# Update the Atlas Quota to 30 
	print 'Updating the Atlas quota for 30...'
	quota_value = 30 
	atlas_quota = utils.update_quota(mike_token, 
				         production_project_id,
				         atlas_project_id,
				         quota_value)
	quota_show_production = utils.quota_show(mike_token,
						 production_project_id,
						 production_project_id)
	quota_show_atlas = utils.quota_show(mike_token,
					    production_project_id,
					    atlas_project_id)
	print 'Verify that allocated ProductionIT quota was updated to 70'
	print "Production Quota: %s" % quota_show_production
	print "Atlas Quota: %s" % quota_show_atlas
	print '======================================================================='

	# Update the Computing Quota to 15 
	print 'Updating the Computing quota for 15...'
	quota_value = 15 
	computing_quota = utils.update_quota(mike_token, 
				             production_project_id,
				             computing_project_id,
				             quota_value)
	quota_show_cms = utils.quota_show(mike_token,
					  production_project_id,
					  cms_project_id)
	quota_show_computing = utils.quota_show(mike_token,
					        production_project_id,
					        computing_project_id)
	print 'Verify that allocated CMS quota was updated to 15'
	print "CMS Quota: %s" % quota_show_cms
	print "Computing Quota: %s" % quota_show_computing
	print '======================================================================='

	# Update the visualisaton Quota to 15 
	print 'Updating the Visualisation quota for 15...'
	quota_value = 15 
	visualisation_quota = utils.update_quota(mike_token, 
				            	 production_project_id,
				             	 visualisation_project_id,
				             	 quota_value)
	quota_show_cms = utils.quota_show(mike_token,
					  production_project_id,
					  cms_project_id)
	quota_show_visualisation = utils.quota_show(mike_token,
						    production_project_id,
						    visualisation_project_id)
	print 'Verify that allocated CMS quota was updated to 30'
	print "CMS Quota: %s" % quota_show_cms
	print "Visualisation Quota: %s" % quota_show_visualisation
	print '======================================================================='

	print 'Updating the Services quota for 10...'
	# Update the services Quota to 10 
	quota_value = 10 
	services_quota = utils.update_quota(mike_token, 
				           production_project_id,
				           services_project_id,
				           quota_value)
	quota_show_atlas = utils.quota_show(mike_token,
					    production_project_id,
					    atlas_project_id)
	quota_show_services = utils.quota_show(mike_token,
					       production_project_id,
					       services_project_id)
	print 'Verify that allocated Atlas quota was updated to 10'
	print "Atlas Quota: %s" % quota_show_atlas
	print "Service Quota: %s" % quota_show_services
	print '======================================================================='

	# Update the operations Quota to 10 
	quota_value = 10 
	operations_quota = utils.update_quota(mike_token, 
				           production_project_id,
				           operations_project_id,
				           quota_value)
	quota_show_atlas = utils.quota_show(mike_token,
					    production_project_id,
					    atlas_project_id)
	quota_show_operations = utils.quota_show(mike_token,
						 production_project_id,
						 operations_project_id)
	print 'Verify that allocated Atlas quota was updated to 20'
	print "Atlas Quota: %s" % quota_show_atlas
	print "Operations Quota: %s" % quota_show_operations
	print '======================================================================='
	# Update the CMS Quota to 40
	quota_value = 71 
	print 'Trying update the CMS quota for 71...'
	cms_quota = utils.update_quota(mike_token, 
				       production_project_id,
				       cms_project_id,
				       quota_value)
	print "Error: %s" % cms_quota
	print '======================================================================='
	print "Creating 10 Volumes in CMS..."
	# Get a token for Jay in CMS
	jay_token_json = utils.get_token_json('Jay', cms_project_id)
        jay_token = utils.get_token(jay_token_json)

	import pdb; pdb.set_trace()
	for i in range(0,9):
	    utils.create_security_group(jay_token, cms_project_id, i)
	quota_show_cms = utils.quota_show(jay_token, cms_project_id, cms_project_id)
	print "CMS Quota: %s" % quota_show_cms
	print 'Now, we dont have free quota in CMS'
	print '======================================================================='
	print "Trying update the computing quota to 16 (subproject for CMS)..."
	quota_value = 16 
	computing_quota = utils.update_quota(mike_token, 
				       production_project_id,
				       computing_project_id,
				       quota_value)
	print "Error: %s" % computing_quota
	print '======================================================================='
	print 'Clean up...'

    except Exception as e:
	print 'Error: %s' % e
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
