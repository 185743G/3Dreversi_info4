import matplotlib.pyplot as plt
import sys
import os
args = sys.argv

# from matplotlib.font_manager import FontProperties
# fp = FontProperties(fname=r'/Library/Fonts/Osaka.ttf', size=16)
import japanize_matplotlib


filename = args[1]
white_tar = "Whiteの勝利数: "
black_tar = "Blackの勝利数: "
white_lis = []
black_lis = []

with open(filename, "r") as f:
	content = f.read()

content = content.split("\n")
for row in content:
	if white_tar in row:
		white_lis.append(int(row.lstrip(white_tar)))
	elif black_tar in row:
		black_lis.append(int(row.lstrip(black_tar)))

white_sum = 0
black_sum = 0
step = 100

def calc_ave(lis):
	return sum(lis)/len(lis)


white_steps = []
black_steps = []
draw_steps = []
for i in range(len(white_lis)):
	w = white_lis[i]
	b = black_lis[i]
	
	step_w = w - white_sum
	step_b = b - black_sum
	step_d = step - (step_w + step_b)
	white_steps.append(step_w)
	black_steps.append(step_b)
	draw_steps.append(step_d)
	
	white_sum = w
	black_sum = b
	
win_draw_rate = [(white_steps[i] + draw_steps[i]) / step for i in range(len(white_steps))]
mask = 20
# print(win_draw_rate)
win_draw_rate = [calc_ave(win_draw_rate[i:i + mask]) for i in range(0, len(white_steps), mask)]

win_rate = sum(white_steps)/(len(white_steps)*step)
draw_rate = sum(draw_steps)/(len(draw_steps)*step)
lose_rate = sum(black_steps)/(len(black_steps)*step)

print(win_rate)
print(draw_rate)
print(lose_rate)


# print(white_steps)
# print(black_steps)
# 
# print(win_rate)
x = [i * step * mask for i in range(len(win_draw_rate))]
y = win_draw_rate

write_str = ""
for xy_i in zip(x, y):
	write_str += "{} {}\n".format(xy_i[0], xy_i[1])

write_dat_f = "{}.dat".format(filename)
# with open (write_dat_f, "w") as f:
f = open(write_dat_f, 'w')
f.write(write_str)
f.close()



# fig = plt.figure()
# plt.xlabel('試合数')
# plt.ylabel('勝率')
# plt.ylim(0, 1.0)
# plt.plot(x, y)
#
# print(win_rate)
# plt.show()


		
	
	

