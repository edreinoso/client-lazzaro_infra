import re

regex_string = '^[a-zA-Z]{3,}$'  # would probably have to change


def isValidString(string):
    print(string)
    return re.match(regex_string, string)


name = 'DnsName'

# res = '/^[a-zA-Z] +$/'.test('sfjd')

if isValidString(name):
    print('passed')
else:
    print('did not pass')
