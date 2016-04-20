#printing
#
#throw this at the end of function 1

f = open("test.txt")
query = f.readline()
print "Query:", query
f.close()
print
print "Results: (%d Total)" %(len(actors))
actors.sort()
for a in actors:
	print "\t" + a
print
print "Method 1 total cost: %d" %(num_pages['actor_table']+ num_pages['movie_table'] + num_pages['movie_idx'] + num_pages['actor_idx'])

if num_pages['movie_idx'] >= 0:
	print "\t" + str(num_pages['movie_idx']), "page movieroles_ma_idx index"
if num_pages['actor_idx'] >= 0:
	print "\t" + str(num_pages['actor_idx']), "page actors_id_idx index"
if num_pages['actor_table'] >= 0:
	print "\t" + str(num_pages['actor_table']), "page actors_table"

#throw this at the end of function 2

print
print "Method 2 total cost: %d" %(num_pages['actor_table']+ num_pages['movie_table'] + num_pages['movie_idx'] + num_pages['actor_idx'])
if num_pages['movie_idx'] >= 0:
	print "\t" + str(num_pages['movie_idx']), "page movieroles_ma_idx index"
if num_pages['actor_table'] >= 0:
	print "\t" + str(num_pages['actor_table']), "page actors_table"

#throw this at the end of function 3

print
print "Method 3 total cost: %d" %(num_pages['actor_table']+ num_pages['movie_table'] + num_pages['movie_idx'] + num_pages['actor_idx'])
if num_pages['movie_table'] >= 0:
	print "\t" + str(num_pages['movie_idx']), "page movieroles_table"
if num_pages['actor_table'] >= 0:
	print "\t" + str(num_pages['actor_table']), "page actors_table"