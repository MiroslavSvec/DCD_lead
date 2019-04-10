


def get_results(data):
		""" Create list of dictionaries from form data"""
		
		# Create a temporary list for storing the filters
		filters = list()
		# Create a loop to loop trough each of the key from form
		for key in data:
			# Store the original key for later use (cuisines-03)
			value_key = key
			# Split the key by "-"
			# You will get list of 2 values ([cuisines,03])
			key = key.split("-")
			# Take the first value of the list (cuisines) as we do not need the number
			key = key[0]
			# Create temporary dictionary to which will be our single filter
			# Each filter MUST be a valid dictionary
			search_filter = dict()
			# Create new k,v pars in above dictionary
			# {"cuisines" : "asian"}

			search_filter[key] = data[value_key]
			# Append the new created filter to our list of filters
			filters.append(search_filter)
	
		return filters
