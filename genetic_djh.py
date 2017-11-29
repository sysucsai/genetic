import random
import math
import time
import read_ans
import readin
import show_path

class object:
    def __init__(self, path = None, fit = None):
        self.path = path[:]
        self.live = 2
        self.fit = fit

class Genetic:
    def __init__(self, n, map):
        self._n = n
        self._map = map
        self._dis = [[None for i in range(self._n)] for j in range(self._n)]
        self._dis_init()
        self.finish = True

    def init(self, group_size, children_size, pc, pm, cross_type, cross_count, mutate_type, select_type, iter_count, goal):
        self._group_size = group_size   # 种群大小
        self._children_size = children_size
        self._pc = pc         # 交叉概率
        self._pm = pm        # 变异概率
        self._cross_type = cross_type
        self._mutate_type = mutate_type
        self._select_type = select_type
        self._cross_count = cross_count
        self._iter_count = iter_count
        self._goal = goal

        self._best_fit = 0
        self._best_path = None
        self._group = []
        self._group_init()
        self._children = []
        self._step = 0
        self._stay = 0
        self.deep = 2
        self.finish = False

    def start(self):
        while not self.finish:
            self.next_step()

    def next_step(self):
        choose_list = [i for i in range(self._group_size)]
        random.shuffle(choose_list)
        for i in range(len(choose_list)):
            if random.random() < self._pc:
                # 随机选择
                mother = self._group[choose_list[i]]
                father = self._group[choose_list[(i+1) % self._group_size]]
                self._children = []
                while len(self._children) < self._children_size:
                    # 交叉
                    self._children.append(self._cross(mother, father))
                # 变异
                self._mutate()
                self._local_search(self._children)
                self._children.sort(key=lambda x: x.fit, reverse=True)
                if self._children[0].fit > mother.fit:
                    self._group.remove(mother)
                    self._group.append(self._children[0])
                    if self._children[0].fit > self._best_fit:
                        self._best_fit = self._children[0].fit
                        self._best_path = self._children[0].path[:]
                        #self._stay = 0
                        #self._children_size = 20
                else:
                    #self._stay += 1
                    #if self._stay > 100:
                    #    self._children_size *= 2
                    #    self._stay = 0
                    pass

        self._step += 1
        print(self._step, 1 / self._best_fit)
        if self._best_fit >= 1.0 / (1.1 * self._goal):
        #if self._step == self._iter_count:
            self.finish = True

    def _select(self, set):
        if self._select_type == 1:
            return self._select1(set)
        elif self._select_type == 2:
            return self._select2()

    def _cross(self, mother = None, father = None):
        #while len(self._children) < self._children_size:
            #mother_index, father_index = self._select()
        if self._cross_type == 1:
            self._one_point_cross(mother_index, father_index)
        elif self._cross_type == 2:
            return self._two_points_cross2(mother, father)
        elif self._cross_type == 3:
            self._multy_points_cross(mother_index, father_index)
        elif self._cross_type == 4:
            self._uniform_cross(mother_index, father_index)

    def _mutate(self):
        if self._mutate_type == 1:
            self._mutate_one()
        elif self._mutate_type == 2:
            self._mutate_one_all()
        elif self._mutate_type == 3:
            self._mutate_all()

    # =======================================================================
    # 变异算子
    def _mutate_one_all(self):
        for target in self._children:
            if random.random() < self._pm:
                for j in range(self._n):
                    if random.random() < self._pm:
                        index1 = random.randint(0, self._n - 1)
                        index2 = random.randint(0, self._n - 1)
                        temp = target.path[index1]
                        target.path[index1] = target.path[index2]
                        target.path[index2] = temp
                        target.fit = self._fit(target.path)

    def _mutate_all(self):
        #for target in self._group:
        for target in self._children:
            for j in range(self._n):
                if random.random() < self._pm:
                    index1 = random.randint(0, self._n - 1)
                    temp = target.path[index1]
                    target.path[index1] = target.path[j]
                    target.path[j] = temp
                    target.fit = self._fit(target.path)

    def _mutate_one(self):
        for target in self._children:
            if random.random() < self._pm:
                index1 = random.randint(0, self._n - 1)
                index2 = random.randint(0, self._n - 1)
                temp = target.path[index1]
                target.path[index1] = target.path[index2]
                target.path[index2] = temp
                target.fit = self._fit(target.path)

    # =======================================================================
    # 交叉算子
    def _one_point_cross(self, mother_index, father_index):
        if random.random() < self._pc:
            mother = self._group[mother_index][:]
            father = self._group[father_index][:]

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

    def _two_points_cross2(self, mother, father):
        parent1 = mother.path[:]
        parent2 = father.path[:]
        index1 = random.randint(0, self._n - 1)
        index2 = random.randint(index1, self._n - 1)
        temp_path = parent2[index1:index2]
        new_path = []
        p1len = 0
        for g in parent1:
            if p1len == index1:
                new_path.extend(temp_path)
                p1len += 1
            if g not in temp_path:
                new_path.append(g)
                p1len += 1

        return object(new_path, self._fit(new_path))

    def _uniform_cross(self, mother_index, father_index):
        mother = self._group[mother_index][:]
        father = self._group[father_index][:]
        for j in range(self._n):
            if random.random() < self._pc:# / self._n:
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

    def _multy_points_cross(self, mother_index, father_index):
        parent1 = mother.path[:]
        parent2 = father.path[:]
        index1 = random.randint(0, self._n - 1)
        index2 = random.randint(index1, self._n - 1)
        temp_path = parent2[index1:index2]
        new_path = []
        p1len = 0
        for g in parent1:
            if p1len == index1:
                new_path.extend(temp_path)
                p1len += 1
            if g not in temp_path:
                new_path.append(g)
                p1len += 1

        return object(new_path, self._fit(new_path))

    # =======================================================================
    # 选择算子
    def _select1(self, set):
        total_fit = sum([i.fit for i in set])
        rate = [i.fit / total_fit for i in set]
        for i in range(1, len(rate)):
            rate[i] += rate[i-1]
        choose = random.random()
        for p in range(len(rate)):
            if rate[p] > choose:
                return set[p]

    def _select2(self, set):
        total_fit = sum([math.exp((0.0 - i.fit) / self._step) for i in set])
        rate = [i.fit / total_fit for i in set]
        for i in range(1, len(rate)):
            rate[i] += rate[i-1]
        choose = random.random()
        for p in range(len(rate)):
            if rate[p] > choose:
                return set[p]

    # =======================================================================
    # 适应值函数
    def _fit(self, path):
        ans = 0
        for i in range(self._n):
            ans += self._dis[path[i]][path[(i + 1) % self._n]]
        return 1.0 / ans

    # =======================================================================
    # 辅助函数
    def _dis_init(self):
        for i in range(self._n):
            for j in range(self._n):
                self._dis[i][j] = (((self._map[i][0] - self._map[j][0]) ** 2 + (self._map[i][1] - self._map[j][1]) ** 2) ** 0.5)

    def _local_search(self, set):
        for target in set:
            local_best = target.path[:]
            local_best_fit = target.fit
            for i in range(1):
                temp_best = local_best[:]
                temp_best_fit = local_best_fit
                for j in range(20):
                    index1 = random.randint(0, self._n-1)
                    index2 = random.randint(0, self._n-1)
                    neighbour = temp_best[:]
                    temp = neighbour[index1]
                    neighbour[index1] = neighbour[index2]
                    neighbour[index2] = temp
                    neighbour_fit = self._fit(neighbour)
                    if neighbour_fit > temp_best_fit:
                        temp_best = neighbour
                        temp_best_fit = neighbour_fit
                if temp_best_fit > local_best_fit:
                    local_best = temp_best
                    local_best_fit = temp_best_fit
            target.path = local_best[:]
            target.fit = local_best_fit

    def _group_init(self):
        initial_list = []
        while len(self._group) < self._group_size:
            sample_list = [i for i in range(self._n)]
            random.shuffle(sample_list)
            if sample_list not in initial_list:
                o = object(sample_list, self._fit(sample_list))
                self._group.append(o)
                if o.fit > self._best_fit:
                    self._best_fit = o.fit
                    self._best_path = o.path[:]

    def get_result(self):
        return 1 / self._best_fit, self._best_path

if __name__ == "__main__":
    #n, map = readin.readin(r"data\att48.tsp")
    n, map = readin.readin(r"data\eil101.tsp")
    g = Genetic(n, map)
    # def init(self, group_size, children_size, pc, pm, cross_type, cross_count, iter_count):
    std_path = read_ans.read_ans(n, r"data\eil101.opt.tour")
    #std_path = read_ans.read_ans(n, r"data\att48.opt.tour")
    std_ans = 1 / g._fit(std_path)

    group_size = 100
    children_size = 10
    pc = 0.6
    pm = 0.01
    cross_type = 2
    cross_count = None
    mutate_type = 3
    select_type = 2
    iter_count = 1000
    g.init(group_size, children_size, pc, pm, cross_type, None, mutate_type, select_type, iter_count, std_ans)

    g.start()
    ans, path = g.get_result()
    print(std_ans, ans, "%", (ans - std_ans) / std_ans * 100)

