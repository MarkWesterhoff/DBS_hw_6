Mark Westerhoff
Stephen Romano

Tested with Python 2.7.6. Make sure the 
How to Run:
	- Make sure the file has executable permissions
	./hw6.py input_file_name
	- Alternatively:
	python hw6.py input_file_name

Input file:
	Used the format given to us. Each query is one line,
	with 4 comma-delimited values representing:
	movieid_low, movieid_high, actorid_low, actorid_high
	'*'s can be inputted to represent any value

Note:
	- Tested with all the sample input. Output matches, but added spacing and '*' lines
		for readability (and is requested in the pdf)
	- Any hardcoded values are at the top of the file.
	- Assumes txt files
		- Assumes 'page#.txt' exist in tables
		- Assumes 'root.txt' exists and files start w/ 'internal' or 'leaf' in indexes