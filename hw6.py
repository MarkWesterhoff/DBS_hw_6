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
NUM_ACTOR_PAGES = 2104
NUM_MOVIE_PAGES = 4017


class Query:
	

	def __init__(self, csvvals):
		'''
		Constructs a Query class from a given input query
		'''
		assert len(csvvals) == 4
		self.query = csvvals

		# Replaces '*'s with the lowest or largest id
		if self.query['movieid_low'] == '*':
			self.movieid_low = MIN_MOVIE_ID
		else:
			self.movieid_low = int(self.query['movieid_low'])

		if self.query['movieid_high'] == '*':
			self.movieid_high = MAX_MOVIE_ID
		else:
			self.movieid_high = int(self.query['movieid_high'])

		if self.query['actorid_low'] == '*':
			self.actorid_low = MIN_ACTOR_ID
		else:
			self.actorid_low = int(self.query['actorid_low'])

		if self.query['actorid_high'] == '*':
			self.actorid_high = MAX_ACTOR_ID
		else:
			self.actorid_high = int(self.query['actorid_high'])

		self.results = dict()


	def run(self):
		self.results[1] = self.method_one()
		self.results[2] = self.method_two()
		self.results[3] = self.method_three()
		# return self.print_results()



	def get_actor_ids_from_movie_index_table(self):
		'''
		Goes through movie_ma_idx and returns the actor ids,
		along the the number of index pages traversed.
		'''
		file = 'root.txt'
		next_file = None
		num_pages = 0
		actorids = list()
		done = False
		found = False
		# Loop through each file it goes through
		while not done:
			with open(BASE+'movieroles_ma_idx/'+file) as f:
				next_file = None
				# plus one for each node it goes to
				num_pages += 1;
				node = f.readline().strip()
				assert node in ('internal', 'leaf')
				reader = csv.DictReader(f, delimiter=",", fieldnames = ['movieid', 'actorid', 'pageid'])
				# doesn't correctly handle last line of files because it isnt in csv format
				for row in reader:
					# last line; move onto next file
					if '.txt' in row['movieid']:
						next_file = row['movieid']
						break

					# Internal node
					if node == 'internal':
						if int(row['movieid']) >= self.movieid_low:
							next_file = row['pageid']
							break

					# leaf node
					elif node == 'leaf':
						if int(row['movieid']) >= self.movieid_low and int(row['movieid']) <= self.movieid_high:
							found = True
							if int(row['actorid']) >= self.actorid_low and int(row['actorid']) <= self.actorid_high:
								actorids.append(row['actorid'])
						# end of sequential block of movie ids that fit the requirements
						elif found == True:
								found = False
								break
			# i.e. last file
			if next_file is None:
				done = True

			file = next_file
		return actorids, num_pages


	def get_actor_pages_from_actor_index_table_given_actor_ids(self, actorids):
		'''
		Goes through actor_id_idx, given actor ids, and returns the corresponding
		pageids (and the number of index pages traversed)
		'''
		
		pageids = list()
		
		# Loop through each file it goes through
		for aid in actorids:
			file = 'root.txt'
			next_file = None
			num_pages = 0
			done = False
			found = False
			while not done:
				with open(BASE+'actors_id_idx/'+file) as f:
					next_file = None
					# plus one for each node it goes to
					num_pages += 1;
					node = f.readline().strip()
					assert node in ('internal', 'leaf')
					reader = csv.DictReader(f, delimiter=",", fieldnames = ['id', 'pageid'])
					# doesn't correctly handle last line of files because it isnt in csv format
					for row in reader:
						# last line; move onto next file
						if '.txt' in row['id']:
							next_file = row['id']
							break

						# Internal node
						if node == 'internal':
							if int(row['id']) >= int(aid):
								next_file = row['pageid']
								break

						# leaf node
						elif node == 'leaf':
							if row['id'] == aid:
								pageids.append(row['pageid'])
								done = True
								break

				if next_file is None:
					done = True

				file = next_file
			return pageids, num_pages


	def get_actor_names_from_actor_table_given_pages(self, pageids, actorids):
		'''
		Goes through actor_table, given actor ids and corresponding page ids, 
		and returns the corresponding actors (and the number of table pages traversed)
		'''
		num_pages = 0
		actors = list()
		for page, aid in zip(pageids, actorids):
			file = 'page%s.txt' % (page);
			with open(BASE+'actors_table/'+file) as f:
				num_pages += 1;
				reader = csv.DictReader(f, delimiter=",", fieldnames = ['atype', 'id', 'name', 'surname'])
				for row in reader:
					if row['id'] == aid:
						actors.append(" ".join([row['name'], row['surname']]))
						break
		return actors, num_pages


	def get_actor_names_from_actor_table_given_ids(self, actorids):
		'''
		Goes through actor_table, given ONLY actor ids, 
		and returns the corresponding actors (and the number of table pages traversed)
		'''
		actors = list()
		num_pages = 0
		done = False
		page = 1
		while not done and page <= NUM_ACTOR_PAGES:
			file = 'page%s.txt' % (page);
			with open(BASE+'actors_table/'+file) as f:
				num_pages += 1;
				reader = csv.DictReader(f, delimiter=",", fieldnames = ['atype', 'id', 'name', 'surname'])
				for row in reader:
					if row['id'] in actorids:
						actors.append(" ".join([row['name'], row['surname']]))
						actorids.remove(row["id"])
						if len(actorids) == 0:
							done = True
							break
			page += 1

		return actors, num_pages


	def get_actor_ids_from_movie_table(self):
		'''
		Goes through movie_table and returns the corresponding actors 
		(and the number of table pages traversed).
		'''
		actorids = list()
		num_pages = 0
		done = False
		for page in xrange(1, NUM_MOVIE_PAGES+1):
			file = 'page%s.txt' % (page);
			with open(BASE+'movieroles_table/'+file) as f:
				num_pages += 1;
				reader = csv.DictReader(f, delimiter=",", fieldnames = ['actorid', 'info_1', 'info_2', 'movieid', 'role'])
				for row in reader:
					if ( int(row['movieid']) >= self.movieid_low and int(row['movieid']) <= self.movieid_high and 
					int(row['actorid']) >= self.actorid_low and int(row['actorid']) <= self.actorid_high and
					row['actorid'] not in actorids ):
						actorids.append(row['actorid'])
			page += 1

		return actorids, num_pages


	def method_one(self):
		'''
		Scans movieroles_ma_idx index to find all actors,
		 then actors_id_idx to find the names of these actors.
		'''
		num_pages = {'movieroles_idx' : 0, 'movieroles_table' : 0, 'actors_idx' : 0, 'actors_table' : 0}

		actorids = list()
		actorids, num_pages['movieroles_idx'] = self.get_actor_ids_from_movie_index_table()

		pageids = list()
		pageids, num_pages['actors_idx'] = self.get_actor_pages_from_actor_index_table_given_actor_ids(actorids)

		actors = list()
		actors, num_pages['actors_table'] = self.get_actor_names_from_actor_table_given_pages(pageids, actorids)
		
		return actors, num_pages

    				
	def method_two(self):
		'''
		Scans movieroles_ma_idx index to find all actors,
		 then scan the whole actors_table to find the names 
		 of these actors (if their id is in the set of actor ids found).
		'''
		
		num_pages = {'movieroles_idx' : 0, 'movieroles_table' : 0, 'actors_idx' : 0, 'actors_table' : 0}

		actorids = list()
		actorids, num_pages['movieroles_idx'] = self.get_actor_ids_from_movie_index_table()

		pageids = list()
		pageids, num_pages['actors_idx'] = self.get_actor_pages_from_actor_index_table_given_actor_ids(actorids)

		actors = list()
		actors, num_pages['actors_table'] = self.get_actor_names_from_actor_table_given_ids(actorids)

		return actors, num_pages
		

	def method_three(self):
		'''
		Scan both tables to answer the question; no indices.
		 Scan movieroles_table first, then actors_table.
		'''
		
		num_pages = {'movie_idx' : 0, 'movie_table' : 0, 'actor_idx' : 0, 'actor_table' : 0}

		actorids = list()
		actorids, num_pages['movie_table'] = self.get_actor_ids_from_movie_table()

		actors = list()
		actors, num_pages['actors_table'] = self.get_actor_names_from_actor_table_given_ids(actorids)

		return actors, num_pages


	# def print_results():
	# 	'''
	# 	Prints the results of a query
	# 	Unfinished
	# 	'''
	# 	assert self.results[1]
	# 	assert self.results[2]
	# 	assert self.results[3]
	# 	output = "Query: " + ','.join(str(self.vals['movieid_low']),
	# 							str(self.vals['movieid_high']),
	# 							str(self.vals['actorid_low']),
	# 							str(self.vals['actorid_high'])) + '\n'
	# 	output += '\n'
	# 	output += 'Results:\n' + [ str(i)+'\n' for i in self.results['results']]
	# 	output += '\n'
	# 	For i in range(1,4):
	# 		output += "Method %i total cost: %i pages\n" % (i, self.results[i]['Total'])
	# 				+ ""
	# 	return output


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("input_file_name")
	args = parser.parse_args()
	with open(args.input_file_name) as f:
		reader = csv.DictReader(f, delimiter=",",fieldnames=['movieid_low','movieid_high','actorid_low','actorid_high'])
		for row in reader:
			q = Query(row)
			q.run()
	        #print q.print_results()
	        print '\n' + '*'*20 + '\n'