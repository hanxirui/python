#/usr/local/bin python3
#-*- coding:utf-8 -*-
import re
'''https://automatetheboringstuff.com/chapter7/'''

# phoneNumRegex = re.compile(r'\d{3}-\d{3}-\d{4}')

# mo = phoneNumRegex.search('My number is 415-555-4242.')

# print('Phone number found: ' + mo.group())

# pr = re.compile(r'(\d{3})-(\d{3}-\d{4})')
# mo = pr.search('My number is 415-555-4242.')
# print(mo.group(1))
# print(mo.group(2))
# print(mo.group(0))
# print(mo.group())
# print(mo.groups())

# areaCode, mainNumber = mo.groups()
# print(areaCode)
# print(mainNumber)

# heroRegex = re.compile (r'Batman|Tina Fey')
# mo1 = heroRegex.search('Batman and Tina Fey.')
# print(mo1.group())
# mo1 = heroRegex.findall('Batman and Tina Fey.')
# print(mo1)


# mo2 = heroRegex.search('Tina Fey and Batman.')
# print(mo2.groups())
# print(mo2.group())


# batRegex = re.compile(r'Bat(man|mobile|copter|bat)')
# mo = batRegex.search('Batmobile lost a wheel Batman')
# print(mo.group())
# print(mo.groups())

# batRegex = re.compile(r'Bat(wo)?man')
# mo1 = batRegex.search('The Adventures of Batman')
# print(mo1.group())


# mo2 = batRegex.search('The Adventures of Batwoman')
# print(mo2.group())



# batRegex = re.compile(r'Bat(wo)+man')
# mo1 = batRegex.search('The Adventures of Batwoman')
# print(mo1.group())


# mo2 = batRegex.search('The Adventures of Batwowowowoman')
# print(mo2.group())


# mo3 = batRegex.search('The Adventures of Batman')
# print(mo3 == None)

# \d
# Any numeric digit from 0 to 9.
# \D
# Any character that is not a numeric digit from 0 to 9.
# \w
# Any letter, numeric digit, or the underscore character. (Think of this as matching “word” characters.)
# \W
# Any character that is not a letter, numeric digit, or the underscore character.
# \s
# Any space, tab, or newline character. (Think of this as matching “space” characters.)
# \S
# Any character that is not a space, tab, or newline.

# beginsWithHello = re.compile(r'^Hello')
# print(beginsWithHello.search('Hello world!'))

# print(beginsWithHello.search('He said hello.') == None)


# endsWithNumber = re.compile(r'\d$')
# print(endsWithNumber.search('Your number is 42'))
# print(endsWithNumber.search('Your number is forty two.') == None)


# The . (or dot) character in a regular expression is called a wildcard and will match any character except for 
# a newline. For example, enter the following into the interactive shell:

atRegex = re.compile(r'.at')
print(atRegex.findall('The cat in the hat sat on the flat mat.'))

nameRegex = re.compile(r'First Name: (.*) Last Name: (.*)')
mo = nameRegex.search('First Name: Al Last Name: Sweigart')
print(mo.group())

print(mo.group(1))

print(mo.group(2))


noNewlineRegex = re.compile('.*')
print(noNewlineRegex.search('Serve the public trust.\nProtect the innocent.\nUphold the law.').group())


newlineRegex = re.compile('.*', re.DOTALL)
print(newlineRegex.search('Serve the public trust.\nProtect the innocent.\nUphold the law.').group())


# re.IGNORECASE or re.I
robocop = re.compile(r'robocop', re.I)
robocop.search('Robocop is part man, part machine, all cop.').group()


robocop.search('ROBOCOP protects the innocent.').group()


robocop.search('Al, why does your programming book talk about robocop so much?').group()


namesRegex = re.compile(r'Agent \w+')
namesRegex.sub('CENSORED', 'Agent Alice gave the secret documents to Agent Bob.')

agentNamesRegex = re.compile(r'Agent (\w)\w*')
agentNamesRegex.sub(r'\1****', 'Agent Alice told Agent Carol that Agent Eve knew Agent Bob was a double agent.')




























