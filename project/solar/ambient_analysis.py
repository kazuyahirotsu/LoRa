import ambient
ambi = ambient.Ambient(53835, "b68eaa4a9767851b", "	47b5ae58fb80f2f3")

try:
    data = ambi.read(n=100)
except Exception as e:
    print(e)
print(data)