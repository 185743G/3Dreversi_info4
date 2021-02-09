import sys
import os
args = sys.argv

filename = args[1]
with open(filename, "r") as f:
    content = f.read()

result_str = ""
content = content.split("\n")
if content[-1] == "":
    content.pop(-1)

step = 100
mask = 20
for line_i in range(0, len(content), mask):
    lines = content[line_i:line_i+mask]
    new_line = []
    new_line.append(line_i*step)
    print(lines)
    ave = sum([float(line.split()[1]) for line in lines])/len(lines)
    new_line.append(ave)  # 数字
    result_str += "{} {}".format(new_line[0], new_line[1]) + "\n"

print(result_str)

# with open("logs/{}.dat".format(filename), "w") as f:
#     f.write(result_str)

f = open("{}.dat".format(filename), 'w')
f.write(result_str)
f.close()