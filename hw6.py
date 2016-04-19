#!/usr/bin/python
'''
Mark Westerhoff
Stephen Romano
'''

import argparse
import csv
import os


BASE='hw6_files/hw6_files/'

MIN_ACTOR_ID = 1
MAX_ACTOR_ID = 149374 #note: there is a line for leaf374.txt, which doesnt exist
MIN_MOVIE_ID = 119182
MAX_MOVIE_ID = 3619455


class fileReader():
	def __init__(filename):
		self.f = filename



class Query():
	self.query = dict()
	self.movieids = list()
	self.actorids = list()
	self.results = dict()
	def __init__(self, csvvals):
		'''
		Constructs a query
		'''
		assert len(csvvals) == 4
		self.query = csvvals
		if self.query['movieid_low'] == '*':
			self.movieid_low = MIN_MOVIE_ID
		else
			self.movieid_low = self.query['movieid_low']

		if self.query['movieid_high'] == '*':
			self.movieid_high = MAX_MOVIE_ID
		else
			self.movieid_high = self.query['movieid_high']

		if self.query['actorid_low'] == '*':
			self.actorid_low = MIN_ACTOR_ID
		else
			self.actorid_low = self.query['actorid_low']

		if self.query['actorid_high'] == '*':
			self.actorid_high = MAX_ACTOR_ID
		else
			self.actoridhigh = self.query['actord_high']

		#probably a bad idea
		self.movieids = [i for i in range(self.movieid_low, self.movieid_high+1)]
		self.actorids = [i for i in range(self.actorid_low, self.actorid_high+1)]

	def run():
		self.results[1] = self.method_one()
		# self.results[2] = self.method_two()
		# self.results[3] = self.method_three()
		# return self.print_results()


	def method_one():
		'''
		Scans movieroles_ma_idx index to find all actors,
		 then actors_id_idx to find the names of these actors.
		'''
		node = 'internal'
		file = 'root.txt'
		range_pairs = list()
		with open(BASE+'movieroles_ma_idx/'+file) as f:
			node = f.readline()
			assert node in ('internal', 'leaf')
    		reader = csv.DictReader(f, delimiter=",",fieldnames=['movieid', 'actorid', 'pageid'])
    		last_val = 0
    		for row in reader:
    			#check if the node is necessary to go to
    			for i in self.movieids:

    			if row['movieid'] >= self.movieid_low and self.movieid_low >= last_val:

    			elif row['movieid'] <= 
    			  range_pairs.append( () )

    			last_val = row['movieid']

	def method_two():
		'''
		Scans movieroles_ma_idx index to find all actors,
		 then scan the whole actors_table to find the names 
		 of these actors (if their id is in the set of actor ids found).
		'''
		pass

	def method_three():
		'''
		Scan both tables to answer the question; no indices.
		 Scan movieroles_table first, then actors_table.
		'''
		pass

	def print_results():
		'''
		Prints the results of a query
		Unfinished
		'''
		assert self.results[1], self.results[2], self.results[3]
		output = "Query: " + ','.join(str(self.vals['movieid_low']),
								str(self.vals['movieid_high']),
								str(self.vals['actorid_low']),
								str(self.vals['actorid_high'])) + '\n'
		output += '\n'
		output += 'Results:\n' + [ str(i)+'\n' for i in self.results['results']]
		output += '\n'
		For i in range(1,4):
			output += "Method %i total cost: %i pages\n" % (i, self.results[i]['Total'])
					+ ""
		return output


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("input_file_name")
	parser.parse_args()
	with open(parser.input_file_name) as f:
    	reader = csv.DictReader(f, delimiter=",",fieldnames=['movieid_low','movieid_high','actorid_low','actorid_high'])
    	for row in reader:
	    	q = Query(row)
	        q.run()
	        print q.print_results()
	        print '\n' + '*'*20 + '\n'