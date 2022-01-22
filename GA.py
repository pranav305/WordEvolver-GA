import random as rand

target = "quick brown fox"  #Target Phrase
characters = list("abcdefghijklmnopqrstuvwxyz !") #Character Pool
init_size = 500  # Generation Size
m_rate = 0.7    #Mutation Rate


gen_nums = 0

class DNA:
    def __init__(self, size = len(target), chromo = []):
        self.chromo = chromo
        self.size = size
        self.fitness = 0
        self.elite = False

    def reset(self):
        self.chromo = []

    def calc_fitness(self):
        score = 0
        for t, g in enumerate(self.chromo):
            if g == target[t]:
                score += 1

        self.fitness = float(score / len(target))
        return self.fitness
    
    def random_init(self):
        self.reset()
        for i in range(self.size):
            self.chromo.append(rand.choice(characters))
        
        self.calc_fitness()
    
    def mutate(self, rate):
        for i in self.chromo:
            if rand.randrange(1) < rate:
                i = rand.choice(characters)
            

class Population:
    def __init__(self, size = init_size, generation = []):
        self.size = size
        self.generation = generation

    def select(self):
        return tuple(rand.choices(
            population=self.generation,
            weights=[i.calc_fitness() for i in self.generation],
            k=2
        ))
    
    def best(self):
        highest = -1
        which = None
        for i in self.generation:
            i.calc_fitness()
            if i.fitness > highest:
                highest = i.fitness
                which = i
                i.elite = True
            else:
                continue
        return highest, which

    def random_population(self):
        for i in range(self.size):
            myDNA = DNA()
            myDNA.random_init()
            self.generation.append(myDNA)


def crossover(a: DNA, b: DNA):
    point = rand.randint(0,len(a.chromo))
    offspring_ab = DNA(chromo=(a.chromo[:point] + b.chromo[point:]))
    offspring_ba = DNA(chromo=(b.chromo[:point] + a.chromo[point:]))

    return (offspring_ab, offspring_ba)

def list_to_str(x):
    a = ""
    for i in x:
        a = a + i
    return a

myPop = Population(init_size)
myPop.random_population()

while myPop.best()[0] != 1:
    new_gen = []
    for i in range(int(init_size/2)):
        p1, p2 = myPop.select()
        new_gen.extend(crossover(p1,p2))
    
    myPop.generation = [i for i in new_gen]
    for i in range(len(myPop.generation)):
        myPop.generation[i].calc_fitness()
    
    x, y = myPop.best()
    y = y.chromo
    for i in myPop.generation:
        if not i.elite:
            i.mutate(m_rate)
    
    gen_nums += 1
    print(str(gen_nums) + "\t" + str(round(x,3)) + "\t" + list_to_str(y))
    

print("\nIt took", gen_nums, "generations to find the phrase:", target)