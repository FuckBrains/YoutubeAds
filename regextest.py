import re

string = "http://www.google.com/search?client=firefox-b-1-d&q=python+regex"
string2 = "https://www.youtube.com/watch?v=PfgS405CdXk&asdfqqwef"

expression = "^https?:\/\/[^#?\/]+"
expression2 = "watch\?v=[\w]+"

print(re.search(expression, string)[0])
print(re.search(expression2, string2)[0][8:])