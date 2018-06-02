
##create student accounts
from accounts.models import User
from student.models import StudentProfile

for i in range(4, 4000):

    user = User.objects.create(username='student{0}'.format(i), password='student12345',email='student{0}@gmail.com'.format(i),\
                        is_student=True, first_name='firstname{0}'.format(i),last_name='lastneme{0}'.format(i))
    StudentProfile.objects.create(user=user)
    print(str(i))


##create instructor accounts
for i in range(45, 150):
    user = User.objects.create(username='instructor{0}'.format(i), password='instructor12345', email='instructor{0}@gmail.com'.format(i), \
                        is_instructor=True, first_name='firstname{0}'.format(i), last_name='lastneme{0}'.format(i))
    Instructor.objects.create(user=user)
    print(str(i))

##create observer accounts
for i in range(45, 150):
    User.objects.create(username='observer{0}'.format(i), password='observer12345', email='observer{0}@gmail.com'.format(i), \
                        is_observer=True, first_name='firstname{0}'.format(i), last_name='lastneme{0}'.format(i))
    print(str(i))


for i in range(45,9000):

    user = User(username='student{0}'.format(i), password='student12345',email='student{0}@gmail.com'.format(i),\
                        is_student=True, first_name='firstname{0}'.format(i),last_name='lastneme{0}'.format(i))
    users.append(user)
    print(str(i))
