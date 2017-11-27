def read_file(file_name):
	file_name = file_name
	with open(file_name) as file_reader:
		data = file_reader.read().splitlines()
		data = [i.lstrip() for i in data if i != ""]
		return data


def get_city_list(n, data):
	p = 0
	for i in range(len(data)):
		if data[i].startswith("TOUR_SECTION"):
			p = i
			break
	city_list = []
	'''b = data[p+1][:]
	for i in range(n-1):
		a, space, b = b.partition(' ')
		city_list.append(int(a))
	city_list.append(int(b))'''
	p += 1
	for p in range(p, p+n):
		city_list.append(int(data[p]))
	return city_list


def read_ans(n, file):
	data = read_file(file)
	city_list = get_city_list(n, data)
	for i in range(n):
		city_list[i] -= 1
	return city_list

if __name__ == '__main__':
	city_list = read_ans(130, r"data\ch130.opt.tour")
	print(city_list)
