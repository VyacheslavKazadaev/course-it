# Sets
a = {"Jake", "John", "Eric"}
print(f"{a = }")
b = {"John", "Jill"}
print(f"{b = }")

print(a.intersection(b))
print(b.intersection(a))

print(a.symmetric_difference(b))
print(b.symmetric_difference(a))

print(a.difference(b))
print(b.difference(a))

print(a.union(b))

for i, v in enumerate(a):
    print(i, v)

# Tuples

t = 12345, 54321, 'hello!'
print(f"{t[0] = } {t[2] = }")
u = t, (1, 2, 3, 4, 5)
print(u)
x, y = u
print(f"{x = } {y = }")

