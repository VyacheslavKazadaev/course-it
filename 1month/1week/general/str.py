str1 = "строка"
print(str1)

str2 = """\
Строка с 
несколькими 
строками!
"""
print(str2)

print(str1 * 2)
str3 = 'при' + 'ве' + 'т'
print(str3)
print(str3[0])
print(str3[1:3])
print(len(str3[1:3]))

str4 = f'{str1} {str3}'
print(str4)
