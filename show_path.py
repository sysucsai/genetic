import matplotlib.pyplot as plt
import matplotlib.animation as animation
import readin
import read_ans
'''def initialize(std_path):
	global right_path
	right_path = std_path'''

def plot(city_coordinate, std_path, dif):
	'''使用这个函数前必须安装包，请使用“pip install matplotlib”包
	传进来一个关于城市坐标的list即可，如：
	[(38.24, 20.42), (39.57, 26.15), (40.56, 25.32), (36.26, 23.12), (33.48, 10.54), (37.56, 12.19)]'''
	n, map = readin.readin(r"data\eil101.tsp")
	std_path = read_ans.read_ans(n, r"data\eil101.opt.tour")
	plt.clf()
	right_path = [(map[i][0],map[i][1]) for i in std_path]
	right_path.append((map[std_path[0]][0], map[std_path[0]][1]))
	plt.subplot(1, 2, 1)
	plt.scatter(*zip(*city_coordinate))
	plt.plot(*zip(*city_coordinate))
	lf_title = "Similarity degree:" + str(dif)
	plt.title(lf_title)
	plt.subplot(1, 2, 2)
	plt.scatter(*zip(*right_path))
	plt.plot(*zip(*right_path))
	plt.show()

def animation(city_coordinate, std_path, dif):
	n, map = readin.readin(r"data\eil101.tsp")
	std_path = read_ans.read_ans(n, r"data\eil101.opt.tour")
	plt.clf()
	'''plt.scatter(*zip(*city_coordinate))
	plt.plot(*zip(*city_coordinate))
	plt.pause(0.000001)'''
	right_path = [(map[i][0],map[i][1]) for i in std_path]
	right_path.append((map[std_path[0]][0], map[std_path[0]][1]))
	plt.subplot(1, 2, 1)
	plt.scatter(*zip(*city_coordinate))
	plt.plot(*zip(*city_coordinate))
	lf_title = "Similarity degree:" + str(dif)
	plt.title(lf_title)
	plt.subplot(1, 2, 2)
	plt.scatter(*zip(*right_path))
	plt.plot(*zip(*right_path))
	plt.pause(0.00000001)
	#plt.pause(0.000000000000000000000000000000001)
	plt.show()

def animation_only_myAns(city_coordinate):
	plt.clf()
	plt.scatter(*zip(*city_coordinate))
	plt.plot(*zip(*city_coordinate))
	plt.pause(0.000001)


def test(fig):
	ani = animation.FuncAnimation(fig,None, None, fames = 50, interval=2 * 1000)
	plt.show()
	plt.show()
	#plt.pause(0.000000000000000000000000000000001)
