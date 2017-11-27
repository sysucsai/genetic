import random
import math
import time
import read_ans
import readin
import show_path

class Genetic:
    def __init__(self, n, map):
        self._n = n
        self._map = map
        self._dis = [[None for i in range(self._n)] for j in range(self._n)]
        self._dis_init()
        self.finish = True

    def init(self, group_size, children_size, pc, pm, cross_type, cross_count, iter_count):
        self._group_size = group_size   # 种群大小
        self._children_size = children_size
        self._pc = pc         # 交叉概率
        self._pm = pm        # 变异概率
        self._cross_type = cross_type
        self._cross_count = cross_count
        self._iter_count = iter_count

        self._best_path = [i for i in range(self._n)]
        self._best_ans = self._fit(self._best_path)
        self._group = [None for i in range(self._group_size)]
        self._group_init()
        self._children = []
        self._step = 0
        self.finish = False

    def start(self):
        while not self.finish:
            self.next_step()

    def next_step(self):
        self._children = []
        # 选择
        mother_index, father_index = self._select()
        # 交叉
        self._cross(mother_index, father_index)
        # 变异
        self._mutate()
        # 排序淘汰
        ans_2_path = [(self._fit(i), i) for i in self._group] + [(self._fit(i), i) for i in self._children]
        ans_2_path.sort()
        if ans_2_path[0][0] < self._best_ans:
            self._best_ans = ans_2_path[0][0]
            self._best_path = ans_2_path[0][1][:]
            #print(self._step, self._best_ans)
        self._group = [ans_2_path[i][1] for i in range(self._group_size)]

        self._step += 1
        #print(self._step)
        if self._step == self._iter_count:
            self.finish = True

    def _cross(self, mother_index, father_index):
        for i in range(self._children_size // 2):
            if self._cross_type == 1:
                self._one_point_cross(mother_index, father_index)
            elif self._cross_type == 2:
                self._two_points_cross(mother_index, father_index)
            elif self._cross_type == 3:
                self._multy_points_cross(mother_index, father_index)
            elif self._cross_type == 4:
                self._uniform_cross(mother_index, father_index)
        self._group.extend(self._children)

    def _mutate(self):
        for target in self._group:
            if random.random() < self._pm:
                index1 = random.randint(0, self._n-1)
                index2 = random.randint(0, self._n-1)
                temp = target[index1]
                target[index1] = target[index2]
                target[index2] = temp

    def _one_point_cross(self, mother_index, father_index):
        if random.random() < self._pc:
            mother = self._group[mother_index]
            father = self._group[father_index]

            index = random.randint(0, self._n - 1)
            temp = mother[index:]
            mother = mother[:index] + father[index:]
            father = father[:index] + temp

            for j in range(index, self._n):
                repeat = mother.index(mother[j])
                while repeat != j:
                    mother[j] = father[repeat]
                    repeat = mother.index(mother[j])
            for j in range(index, self._n):
                repeat = father.index(father[j])
                while repeat != j:
                    father[j] = mother[repeat]
                    repeat = father.index(father[j])
            self._children.append(mother)
            self._children.append(father)

    def _uniform_cross(self, mother_index, father_index):
        mother = self._group[mother_index][:]
        father = self._group[father_index][:]
        for j in range(self._n):
            if random.random() < self._pc / self._n:
                temp = mother[j]
                mother[j] = father[j]
                father[j] = temp
        for j in range(self._n):
            repeat = mother.index(mother[j])
            while repeat != j:
                mother[j] = father[repeat]
                repeat = mother.index(mother[j])
        for j in range(self._n):
            repeat = father.index(father[j])
            while repeat != j:
                father[j] = mother[repeat]
                repeat = father.index(father[j])

        self._children.append(mother)
        self._children.append(father)

    def _two_points_cross(self, mother_index, father_index):
        if random.random() < self._pc:
            mother = self._group[mother_index][:]
            father = self._group[father_index][:]

            index1 = random.randint(0,self._n - 1)
            index2 = random.randint(0,self._n - 1)
            while index2 == index1:
                index2 = random.randint(0,self._n - 1)
            if index1 > index2:
                index_temp = index1
                index1 = index2
                index2 = index_temp

            change_section = mother[index1:index2]
            mother[index1:index2] = father[index1:index2]
            father[index1:index2] = change_section

            mother_unchange = mother[:index1] + mother[index2:]
            father_unchange = father[:index1] + father[index2:]
            for i in range(index1, index2):
                while mother[i] in mother_unchange:
                    mother[i] = father_unchange[mother_unchange.index(mother[i])]
            for i in range(index1, index2):
                while father[i] in father_unchange:
                    father[i] = mother_unchange[father_unchange.index(father[i])]

            self._children.append(mother)
            self._children.append(father)

    def _multy_points_cross(self, mother_index, father_index):
        if random.random() < self._pc:
            mother = self._group[mother_index][:]
            father = self._group[father_index][:]

            change_points = []
            for i in range(self._cross_count * 2):
                change_points.append(random.randint(0, self._n - 1))
            change_points.sort()

            mother_unchange = []
            father_unchange = []
            last_index = 0
            for i in range(self._cross_count):
                index1 = change_points[i * 2]
                index2 = change_points[i * 2 + 1]
                if index2 - index1 > 0:
                    temp = mother[index1:index2]
                    mother[index1:index2] = father[index1:index2]
                    father[index1:index2] = temp
                    if index1 != last_index:
                        mother_unchange.extend(mother[last_index:index1])
                        father_unchange.extend(father[last_index:index1])
                    last_index = index2
            if last_index != self._cross_count - 1:
                mother_unchange.extend(mother[last_index:self._cross_count])
                father_unchange.extend(father[last_index:self._cross_count])

            for i in range(self._cross_count):
                for j in range(change_points[i * 2], change_points[i * 2 + 1]):
                    while mother[j] in mother_unchange:
                        mother[j] = father_unchange[mother_unchange.index(mother[j])]

            for i in range(self._cross_count):
                for j in range(change_points[i * 2], change_points[i * 2 + 1]):
                    while father[j] in father_unchange:
                        father[j] = mother_unchange[father_unchange.index(father[j])]

            self._children.append(mother)
            self._children.append(father)

    def _select(self):
        ans_2_path = [(self._fit(i), i) for i in self._group]
        ans_2_path.sort()

        total_fit = 0
        for i in range(len(ans_2_path)):
            total_fit += ans_2_path[i][0]

        sorted_group = []
        rate = [ans_2_path[0][0] / total_fit]
        sorted_group.append(ans_2_path[0][1])
        for i in range(1, len(ans_2_path)):
            rate.append(ans_2_path[i][0] / total_fit)
            sorted_group.append(ans_2_path[i][1])
        rate.reverse()
        for i in range(1, len(ans_2_path)):
            rate[i] += rate[i - 1]

        mother_index = None
        choose = random.random()
        for p in range(len(rate)):
            if rate[p] > choose:
                mother_index = p
                break

        father_index = None
        choose = random.random()
        for p in range(len(rate)):
            if rate[p] > choose:
                father_index = p
                break
        while father_index == mother_index:
            choose = random.random()
            for p in range(len(rate)):
                if rate[p] > choose:
                    father_index = p
                    break
        self._group = sorted_group[:]
        return mother_index, father_index

    def _dis_init(self):
        for i in range(self._n):
            for j in range(self._n):
                self._dis[i][j] = (((self._map[i][0] - self._map[j][0]) ** 2 + (self._map[i][1] - self._map[j][1]) ** 2) ** 0.5)

    def _group_init(self):
        for i in range(self._group_size):
            sample_list = [i for i in range(self._n)]
            random.shuffle(sample_list)
            self._group[i] = sample_list[:]

    def _fit(self, path):
        ans = 0
        for i in range(self._n):
            ans += self._dis[path[i]][path[(i + 1) % self._n]]
        return ans

    def get_result(self):
        return self._best_ans, self._best_path

if __name__ == "__main__":
    #n, map = readin.readin(r"data\att48.tsp")
    n, map = readin.readin(r"data\eil101.tsp")
    g = Genetic(n, map)
    # def init(self, group_size, children_size, pc, pm, cross_type, cross_count, iter_count):
    std_path = read_ans.read_ans(n, r"data\eil101.opt.tour")
    std_ans = g._fit(std_path)

    group_size = 30
    children_size = 30
    pc = 0.8
    pm = 0.2
    cross_type = 2
    cross_count = None
    iter_count = 1500
    g.init(group_size, children_size, pc, pm, cross_type, None, iter_count)
    g.start()
    ans, path = g.get_result()
    print(ans, (ans - std_ans) / std_ans)

    '''
    # 调教模块
    best = None
    for cross_type in range(1,3):
        for iter_count in range(1000,10000,499):
            for group_size in range(20,100, 10):
                for children_size in range(20 , 100, 10):
                    for pc in [i / 10 for i in range(2, 11, 2)]:
                        for pm in [i / 1000 for i in range(1, int(pc * 1000), 9)]:
                            g.init(group_size, children_size, pc, pm, cross_type, None, iter_count)
                            g.start()
                            ans, path = g.get_result()
                            if best == None:
                                best = [ans, (ans - std_ans) / std_ans, cross_type, iter_count, group_size, children_size, pc, pm]
                            elif ans < best[0]:
                                best = [ans, (ans - std_ans) / std_ans, cross_type, iter_count, group_size, children_size, pc, pm]
                            print(ans, (ans - std_ans) / std_ans, " :", cross_type, iter_count, group_size, children_size, pc, pm)
    print("the best data is:")
    print(best)
    '''
