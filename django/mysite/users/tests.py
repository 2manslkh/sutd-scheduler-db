from django.test import TestCase
from .models import myUser
from django.contrib.auth.models import User
import random
import string


class DBTestCase(TestCase):
    # Populate DB
    def setUp(self):
        num_users = 10
        N=6

        for i in range(num_users):
            myUsername = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
            User.objects.create(username=myUsername)
            print(myUsername + " created.")

        User.objects.create(username='tester')
        print("tester created.")
        

    def test_if_admin(self):
        myUsername = 'tester'

        # Get user_id
        user_id = User.objects.all()
        user_id = user_id.filter(username=myUsername)
        user_id = user_id.values_list("id",flat=True)[0]
        print("{} has id {}".format(myUsername,user_id))

        myUser.objects.create(user_id=user_id,access_level=3)
        print("{} access level changed to 3".format(myUsername))
        # print("Test Object created in my User DB")

        # Get access_level
        access_level = myUser.objects.filter(user_id=user_id).values_list("access_level",flat=True)[0]
        self.assertEqual(3,access_level)
   