#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple
import random
from pprint import pprint
import copy

class parent_t:
	def __init__(self, **kwds):
		self.__dict__.update(kwds)

GENETIC_LENGTH = 4        # 基因長度
POPULATION_CNT = 10       # 母群數量
ITERA_CNT = 100    # 迭代次數
CROSSOVER_RATE = 0.5  # 交配率
MUTATION_RATE = 0.1  # 突變率
population = range(POPULATION_CNT)
pool = range(POPULATION_CNT)
best_gene = parent_t(genes=range(GENETIC_LENGTH), fitness=float(), dec_value=float())


def GAPosRand():
	return random.randint(0,GENETIC_LENGTH-1)

def BinaryRand():
	return random.randint(0,1)

def SRand():
	# pass
	return random.uniform(0,1)

def cal_xvalue(parent):
	dec = 0
	for i in range(GENETIC_LENGTH):
		if parent.genes[i] == 1:
			dec += pow(2,i)
	parent.dec_value = dec

def cal_fitness(parent, best_gene):

	# print 'best2-1',best_gene.fitness
	# print 'best2-fitness',parent.fitness
	# print 'best2-dec_value',parent.dec_value

	parent.fitness = pow(parent.dec_value,2)
	# print 'best2-4',best_gene.fitness

def initialize():
	global best_gene
	for i in range(0,POPULATION_CNT):
		population[i] = parent_t(genes=range(GENETIC_LENGTH), fitness=float(), dec_value=float())
		for j in range(0,GENETIC_LENGTH):
			population[i].genes[j]=BinaryRand()
			# print population
		cal_xvalue(population[i])
		cal_fitness(population[i], best_gene)

		if i == 0:
			best_gene = copy.deepcopy(population[i])

		elif population[i].fitness > best_gene.fitness:
			best_gene = copy.deepcopy(population[i])

	for parent in population:
		print parent.fitness
	print '-----end of fitness print-----'

	# return best_gene

def reproduction():
	fitness_sum = 0.0
	cnt = 0
	copy = 0
	slack = POPULATION_CNT
	for i in range(0,POPULATION_CNT):
		# print population[i].fitness
		fitness_sum += population[i].fitness 
	print 'end of fitness_sum', fitness_sum
	# return fitness_sum
	for i in range(0,POPULATION_CNT):
		if slack == 0:
			break
		cnt = int(round((population[i].fitness/fitness_sum)*POPULATION_CNT))
		if cnt > slack:
			cnt = slack
		print cnt
		for j in range(0,cnt):
			pool[copy] = population[i]
			copy +=1
		slack -= cnt
	print 'end of cnt'

	while copy < POPULATION_CNT:
		pos1 = random.randint(0,POPULATION_CNT-1)
		pos2 = random.randint(0,POPULATION_CNT-1)
		while pos1 == pos2:
			pos2 = random.randint(0,POPULATION_CNT-1)

		if population[pos1].fitness > population[pos2].fitness:
			i = pos1
		else:
			i = pos2
		pool[copy] = population[i]
		copy += 1

	for first_gen in pool:
		print first_gen.fitness
	print 'end of first generation'


def crossover():
	cnt = 0
	i = 0
	p1 = 0
	p2 = 0
	pos = 0
	if_crossover = float()

	while cnt < POPULATION_CNT:
		p1 = random.randint(0,POPULATION_CNT-1)
		p2 = random.randint(0,POPULATION_CNT-1)
		while p1 == p2:
			p2 = random.randint(0,POPULATION_CNT-1)

		if_crossover = SRand()

		if if_crossover > CROSSOVER_RATE:
			print "crossover!"
			population[cnt] = pool[p1]
			cnt+=1 
			population[cnt] = pool[p2]
			cnt+=1
			
		else:
			while pos == 0:
				pos = GAPosRand()
			for i in range(0,pos):
				population[cnt].genes[i]=pool[p1].genes[i]
				population[cnt+1].genes[i]=pool[p2].genes[i]
			for i in range(0,GENETIC_LENGTH):
				population[cnt+1].genes[i]=pool[p1].genes[i]
				population[cnt].genes[i]=pool[p2].genes[i]
			cnt += 2

def mutation(best_gene):
	# global best_gene
	# print best_gene.genes[],best_gene.dec_value,。best_gene.fitness
	print 'enter mutant', best_gene.fitness
	for i in range(0,POPULATION_CNT):
		if_mutation = SRand()
		if if_mutation < MUTATION_RATE:
			pos = GAPosRand()
			# print 'best0',best_gene.fitness
			population[i].genes[pos] = 1-population[i].genes[pos]
			print 'mutant!'
		# print 'best1',best_gene.fitness
		cal_xvalue(population[i])
		# print 'best2',best_gene.fitness
		cal_fitness(population[i], best_gene)
		# print 'best3',best_gene.fitness
		print 'fit',population[i].fitness
		
		if population[i].fitness > best_gene.fitness:
			best_gene = copy.deepcopy(population[i])
			print 'replace', best_gene.fitness
	return best_gene

initialize()
print best_gene.fitness

for i in range(0,ITERA_CNT):
	try:
		reproduction()
		crossover()
		best_gene = mutation(best_gene)
		# print 'best', best_gene.genes[:] ,best_gene.dec_value, best_gene.fitness
	except:
		pass
