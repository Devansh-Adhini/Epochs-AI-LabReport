import random
from music21 import stream, note, midi

raagasc=['C','C#','E','F','G','G#','B']
raagdesc=['C','B','G#','G','F','E','C#']

def gmel(length):
    melody = []
    for _ in range(length):
        s=random.choice(raagasc if random.random() > 0.5 else raagdesc)
        melody.append(s)
    return melody

def fitness(melody):
    fitness = 0
    for i in range(len(melody) - len(raagdesc) + 1):
        if melody[i:i + len(raagdesc)] == raagdesc:
            fitness += 10  
        for j in range(2, len(raagdesc)):
            if melody[i:i + j] == raagdesc[:j]:
                   fitness += j 
    for i in range(len(melody)-len(raagasc) + 1):
        if melody[i:i + len(raagasc)] == raagasc:
            fitness += 10 
        for j in range(2, len(raagasc)):
            if melody[i:i + j] == raagasc[:j]:
                fitness += j  
    return fitness

def crossover(p1,p2):
    split=random.randint(1,len(p1)-1)
    c1=p1[:split]+p2[split:]
    c2=p2[:split]+p1[split:]
    return c1,c2

def mutate(melody,_):
    for i in range(len(melody)):
        if random.random() < 0.1:
            melody[i] = random.choice(raagasc if random.random() > 0.5 else raagdesc)
    return melody

def genealgo(generations=1000, population_size=100,mutation_rate=0.6,melody_length=60):
    population=[gmel(melody_length) for _ in range(population_size)]
    for _ in range(generations):
        fitness_scores=[(melody, fitness(melody)) for melody in population]
        fitness_scores.sort(key=lambda x: x[1],reverse=True)  
        bm=fitness_scores[0][0]  
        selected=[melody for melody, _ in fitness_scores[:population_size//2]]
        next_population = []
        while len(next_population) < population_size:
            p1, p2=random.sample(selected, 2)
            c1, c2=crossover(p1, p2)
            next_population.append(mutate(c1, mutation_rate))
            next_population.append(mutate(c2, mutation_rate))
        population = next_population
    return bm

def melody_to_stream(melody):
    s = stream.Stream()
    for swara in melody:
        n = note.Note(swara)
        s.append(n)
    return s

bm=genealgo()
s=melody_to_stream(bm)
mf=midi.translate.music21ObjectToMidiFile(s)
mf.open("raag_bhairav.mid",'wb')
mf.write()
mf.close()
