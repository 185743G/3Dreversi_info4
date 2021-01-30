import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
# fp = FontProperties(fname=r'/Library/Fonts/Osaka.ttf', size=16)
import japanize_matplotlib



white_tar = "Whiteの勝利数: "
black_tar = "Blackの勝利数: "
white_lis = []
black_lis = []
while  True:
	input_dat = input()
	if input_dat == "":
		break
	if white_tar in input_dat:
		white_lis.append(int(input_dat.lstrip(white_tar)))
	elif black_tar in input_dat:
		black_lis.append(int(input_dat.lstrip(black_tar)))

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
	step_b =  b - black_sum
	step_d = step - (step_w + step_b)
	white_steps.append(step_w)
	black_steps.append(step_b)
	draw_steps.append(step_d)
	
	white_sum = w
	black_sum = b
	
win_rate = [white_steps[i]/step for i in range(len(white_steps))]
mask = 10
print(win_rate)
win_rate = [calc_ave(win_rate[i:i+mask]) for i in range(0, len(white_steps), mask)]

# print(white_steps)
# print(black_steps)
# 
# print(win_rate)
x = [i*step*mask for i in range(len(win_rate))]
y = win_rate
fig = plt.figure()
plt.xlabel('試合数')
plt.ylabel('勝率')
plt.plot(x, y)

print(win_rate)
plt.show()


		
	
	

