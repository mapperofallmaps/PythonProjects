
ipAddress = input("Please enter your IP address: ")
if ipAddress[-1] != '.':
    ipAddress += "."

segments = 0
count = 0
# character = ""

for character in ipAddress:
    if character == '.':
        print("Segment {} contains {} characters".format(segments, count))
        segments += 1
        count = 0
    else:
        count += 1

# if character != '.':
#     print("Segment {} contains {} characters".format(segments, count))
