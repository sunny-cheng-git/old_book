from django.test import TestCase

# Create your tests here.
# dic = {'key':'value'}
# d = dic.get('key')
# print(d)


import re
dd = re.search('media','media/book_imgs/英莲.jpg')
print(dd.group())