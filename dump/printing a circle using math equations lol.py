import math

def draw_heart(counter):
	string = ''
	for y in range(-25, 25):
		for x in range(-50, 50):
			f = -1/counter
			lhs = ((f*x)**2+(f*1.5*y)**2-1.0)**3
			rhs = ((f*x)**2)*((f*1.5*y)**3)
			if (lhs) <= (rhs):
				string += "#"
			elif x == 0:
				string += ' '
			elif y == 0:
				string += " "
			else:
				string += " "
		string += '\n'
	print(string)


counter = 100
while True:
	if counter >= 10:
		counter -= 0.1
	else:
		break

	draw_heart(counter)

for i in range(0, 10):
	counter = 10
	while True:
		if counter <= 20:
			counter += 0.1
		else:
			break

		draw_heart(counter)

	counter = 20
	while True:
		if counter >= 10:
			counter -= 0.1
		else:
			break

		draw_heart(counter)

print('just doing some timepass lol')