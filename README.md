# cinder-quota-tests

Scripts to create a hierarchy and make some funciontal tests related to
nested quotas driver

test_authorization_nested_quota_cinder
-------------------------------------

We make some tests to verify the access control in the quota operations.

test_values_nested_quota_cinder
-------------------------------

We make some tests to verify that the quota calculation are working in 
the correct way.

Execution
---------

$ python test_authorization_nested_quota_cinder.py 

$ python test_values_nested_quota_cinder.py


Note: After run this command you can see the full log in the files:

* log_test_values_cider.txt
* log_test_authorization_cider.txt
