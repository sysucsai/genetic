import random
import readin
import read_ans

class Life():
    def __init__(self, path = None):
        self.gene_path = path
        self.score = -1

class GA():
    def __init__(self, crate = 0.7, mrate = 0.02, lcount = 100, tsp = r"data\eil101.tsp", opt = r"data\eil101.opt.tour"):
        self.cross_rate = crate
        self.mutation_rate = mrate
        self.life_count = lcount
        self.map = []
        self.std_path = []
        self.city_count = 0
        self.lives = []
        self.best_life = None
        self.best_dis = 0.0
        self.relate_error = 1.0
        self.generation = 1
        self.cross_count = 0
        self.mutation_count = 0
        self.bounds = 0.0
        self.dis = []
        self.reinitialize(tsp, opt)

    def reinitialize(self, tsp, opt):
        #readin
        n, mp = readin.readin(tsp)
        self.city_count = n
        self.map = mp
        sp = read_ans.read_ans(n, opt)
        self.std_path = sp
        #initial lives
        self.lives = []
        for i in range(self.life_count):
            path = [x for x in range(self.city_count)]
            random.shuffle(path)
            life = Life(path)
            self.lives.append(life)
        self.best_life = None
        self.best_dis = 0.0
        self.relate_error = 1.0
        self.generation = 1
        self.cross_count = 0
        self.mutation_count = 0
        #initial distance tuple
        self.dis = []
        for i in range(n):
            self.dis.append([])
            for j in range(n):
                self.dis[i].append(((mp[i][0]-mp[j][0])**2 + (mp[i][1]-mp[j][1])**2) ** 0.5)
            self.dis[i] = tuple(self.dis[i])
        self.dis = tuple(self.dis)
        self.std_dis = self.dis_cal(self.std_path)

    def dis_cal(self, path):
        distance = 0
        for i in range(self.city_count):
	        distance += self.dis[path[i]][path[(i+1)%self.city_count]]
        return distance

    def judge(self):
        self.bounds = 0.0
        self.best_life = self.lives[0]
        for i in range(self.life_count):
            self.lives[i].score = 10000.0/self.dis_cal(self.lives[i].gene_path)
            self.bounds += self.lives[i].score
            if self.best_life.score < self.lives[i].score:
                self.best_life = self.lives[i]
        self.best_dis = self.dis_cal(self.best_life.gene_path)
        self.relate_error = (self.best_dis - self.std_dis)/self.std_dis

    def cross(self, parent1, parent2):
        index1 = random.randint(0, self.city_count - 1)
        index2 = random.randint(index1, self.city_count - 1)
        temp_path = parent2.gene_path[index1:index2]
        new_path = []
        p1len = 0
        for g in parent1.gene_path:
            if p1len == index1:
                new_path.extend(temp_path)
                p1len += 1
            if g not in temp_path:
                new_path.append(g)
                p1len += 1
        self.cross_count += 1
        return new_path

    def mutation(self, path):
        index1 = random.randint(0, self.city_count - 1)
        index2 = random.randint(0, self.city_count - 1)
        new_path = path[:]
        new_path[index1], new_path[index2] = new_path[index2], new_path[index1]
        self.mutation_count += 1
        return new_path

    def getOne(self):
        r = random.uniform(0, self.bounds)
        for i in range(self.life_count):
            r -= self.lives[i].score
            if r <= 0:
                return self.lives[i]

    def newChild(self):
        parent1 = self.getOne()
        
        rate1 = random.random()
        if rate1 < self.cross_rate:
            parent2 = self.getOne()
            path = self.cross(parent1, parent2)
        else :
            path = parent1.gene_path
        
        rate2 = random.random()
        if rate2 < self.mutation_rate:
            path = self.mutation(path)
        
        return Life(path)

    def next_(self):
        self.judge()
        newLives = []
        newLives.append(self.best_life)
        while len(newLives) < self.life_count:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1
        show_path = [(self.map[i][0], self.map[i][1]) for i in self.best_life.gene_path]
        show_path.append((self.map[self.best_life.gene_path[0]][0], self.map[self.best_life.gene_path[0]][1]))
        return show_path, self.relate_error

def initialize():
    pass

def next():
    pass

if __name__ == '__main__':
    ga = GA(0.8, 0.05, 200)
    while(ga.relate_error > 0.10):
        ga.next_()
        print(ga.generation, " distance: ", ga.best_dis, ", relative error: ", ga.relate_error*100, "%")


