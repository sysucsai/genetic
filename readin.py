import re
<<<<<<< HEAD
import show_path

=======
>>>>>>> 51477b6f368ff680995da1a5fae5bf5a78a56d74

def read_file(file_name):
	file_name = file_name
	with open(file_name) as file_reader:
		data = file_reader.read().splitlines()
		data = [i.lstrip() for i in data if i != ""]
		return data


def detect_city_num(data):
	non_numeric = re.compile(r'[^\d]+')
	for element in data:
		if element.startswith("DIMENSION"):
			return int(non_numeric.sub("", element))


def get_city_coordinate(data, city_num):
	city_coordinate = []
	now = 0
	for row in data:
		if now == 0:
			if row.startswith('1'):
				now = 1
		if now > 0:
			index, space, coordinate = row.partition(' ')
			x, space, y = coordinate.partition(' ')
			x = float(x)
			y = float(y)
			city_coordinate.append((x, y))
			now += 1
		if now == city_num + 1:
			break
	return city_coordinate


def readin(file = r"data\ulysses16.tsp"):
	'''只需要调用这个函数就好
	参数是文件名字符串，因为数据都在data文件夹下，所以要加路径名
	返回两个值
	第一个是城市的数量 city_num
	第二个是 city_num 个城市的坐标，每个坐标是int类型的二元组
	返回数据示例：
	(16, [(38.24, 20.42), (39.57, 26.15), (40.56, 25.32), (36.26, 23.12), (33.48, 10.54), (37.56, 12.19), (38.42, 13.11), (37.52, 20.44), (41.23, 9.1), (41.17, 13.05)])'''
	data = read_file(file)
	city_num = detect_city_num(data)
	city_coordinate = get_city_coordinate(data,city_num)
	return city_num, city_coordinate
<<<<<<< HEAD

if __name__ == '__main__':
	'''运行sample'''
	print(readin())
	show_path.plot(readin()[1])
=======
>>>>>>> 51477b6f368ff680995da1a5fae5bf5a78a56d74
