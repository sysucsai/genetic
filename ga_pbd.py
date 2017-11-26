import random
import readin
import read_ans

def initial_dis(n, map):
	global dis
	for i in range(n):
	    dis.append([])
	    for j in range(n):
	        dis[i].append(((map[i][0]-map[j][0])**2 + (map[i][1]-map[j][1])**2) ** 0.5)
	    dis[i] = tuple(dis[i])
	dis = tuple(dis)


def dis_cal(path):
    distance = 0
    for i in range(n):
	    distance += dis[path[i]][path[(i+1)%n]]
    return distance

class Life():
    def __init__(self, order = None):
        self.city_coordinate = order
        self.score = -1

class GA():
    def __init__(self, iordinate, bordinate, crate, mrate, lcount, ccount):
        self.init_ordinate = iordinate
        self.best_ordinate = bordinate
        self.cross_rate = crate
        self.mutation_rate = mrate
        self.life_count = lcount
        self.city_count = length
        self.lives = []
        self.best_life = None
        self.generation = 1
        self.cross_count = 0
        self.mutation_count = 0
        self.bounds = 0.0

        self.start_up()
        initial_dis(self.city_count, self.init_ordinate)

    def start_up(self):
        self.lives = []
        for i in range(self.life_count):
            gene = self.init_ordinate
            random.shuffle(gene)
            life = Life(gene)
            self.lives.append(life)
    
    def judge(self):
        self.bounds = 0.0
        self.best_life = self.lives[0]
        for i in range(self.life_count):
            self.lives[i].score = 1.0/dis_cal(self.lives[i].city_coordinate)
            self.bounds += self.lives[i].score
            if self.best_life.score < self.lives[i].score:
                self.best_life = self.lives[i]

    def cross(self, parent1, parent2):
        index1 = random.randint(0, self.city_count - 1)
        index2 = random.randint(index1, self.city_count - 1)
        tempGene = parent2.city_coordinate[index1:index2]
        newGene = []
        tempCount = 0
        for g in parent1.city_coordinate:
            if tempCount == index1:
                newGene.extend(tempGene)
                tempCount += 1
            if g not in tempGene:
                newGene.append(g)
                tempCount += 1
        self.cross_count += 1
        return newGene

    def mutation(self, order):
        index1 = random.randint(0, self.city_count - 1)
        index2 = random.randint(0, self.city_count - 1)
        newGene = order[:]
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        self.mutation_count += 1
        return newGene

    def getOne(self):
        r = random.uniform(0, self.bounds)
        for i in range(self.city_count):
            r -= self.lives[i].score
            if r <= 0:
                return self.lives[i]

    def newChild(self):
        parent1 = self.getOne()
        
        rate1 = random.random()
        if rate < self.cross_rate:
            parent2 = self.getOne()
            order = self.cross(parent1, parent2)
        else :
            order = parent1.city_coordinate
        
        rate2 = random.random()
        if rate2 < self.mutation_rate:
            order = self.mutation(order)
        
        return Life(order)

    def next_(self):
        self.judge()
        newLives = []
        newLives.append(self.best_life)
        while len(newLives) < self.life_count:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1
        self.judge()
        return self.best_life.city_coordinate

def read(tsp, opt):
    n, map = readin.readin(tsp)
    std_path = read_ans.read_ans(n, opt)
    global ga = GA(map, std_path, 0.7, 0.02, 100, n)

def next():
    ga.next_()
    bd = dis_cal(ga.best_life.coordinate)
    print(ga.generation, " : ", bd)
    #return ga.next_()

if __name__ == '__main__':
    read(r"data\eil101.tsp", r"data\eil101.opt.tour")
    for i in range(100):
        next()



        

    

            


