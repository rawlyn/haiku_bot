
import syllables


def extract_line(words, desired_syllable_count, debug=False):
	"""
	attempt to group words from the start of word list
	to make the desired number of syllables
	(i.e. get a five syllable line for a haiku)
	return (line, remaining_words)
	where line will be an empty string if it fails to match the syllable count
	"""
	
	line = ""
	remaining = words[:]
	syllable_count = 0
	
	while (syllable_count < desired_syllable_count) and (len(remaining) > 0):
		# count syllables in word
		word = remaining[0]
		word_syllables = syllables.count_text_syllables(word, debug)
		
		syllable_count += word_syllables
		
		# if still in range, add word to line and remove word from remaining
		if syllable_count <= desired_syllable_count:
			line = "{0} {1}".format(line, word)
			remaining = remaining[1:]
	
	# if the syllable count is good, return the line
	if syllable_count == desired_syllable_count:
		return line.strip(), remaining
	
	# failed, return empty string
	return "", remaining


def suitable_text(text, debug=False):
	"""
	return text if text is suitable for processing
	else return empty string	
	"""
	# broad phase test - only accept ASCII-friendly text
	try:
		ascii_text = text.encode("ascii", "xmlcharrefreplace")
	except UnicodeEncodeError, e:
		return ""
	
	# workaround for "OP" - add a space to the start
	ascii_text = " " + ascii_text
		
	# broad phase test - only likely lengths should be checked
	if 20 >= len(ascii_text) >= 150:
		return ""
	
	# broad phase cleanup - remove double exclamations and dots (espeak reads them out)
	while ascii_text.find("!!") != -1:
		ascii_text = ascii_text.replace("!!", "!")
		
	while ascii_text.find("..") != -1:
		ascii_text = ascii_text.replace("..", ".")
		
	# replace "." with ". " so that it doesn't get read as "dot" between sentences
	ascii_text = ascii_text.replace(".", ". ")
		
	# remove asterisks (espeak reads them out)
	ascii_text = ascii_text.replace("*", "")
	
	# remove hashes for same reason
	ascii_text = ascii_text.replace("#", "")
	
	# and > and <
	ascii_text = ascii_text.replace("&gt;", "")
	ascii_text = ascii_text.replace("&lt;", "")
	
	# remove smileys (espeak just gets confused)
	ascii_text = ascii_text.replace(":)", "")
	ascii_text = ascii_text.replace(";)", "")
	ascii_text = ascii_text.replace(":P", "")
	ascii_text = ascii_text.replace(";P", "")
	ascii_text = ascii_text.replace(":D", "")
	ascii_text = ascii_text.replace(";D", "")
	ascii_text = ascii_text.replace("(:", "")
	
	# replace "OP" with "O.P." (espeak reads as "op" as in "hop")
	ascii_text = ascii_text.replace(" OP", " O.P.")
	
	# replace "plz" with "please" (espeak reads "P.L.Z")
	ascii_text = ascii_text.replace(" plz", " please")
	
	# broad phase test - see if there are 17 syllables
	syllable_count = syllables.count_text_syllables(ascii_text, debug)
	
	if syllable_count != 17:
		return ""
		
	# all tests passed, return text
	return ascii_text
	

def get_haiku(text, debug=False):
	"""
	return empty string if text is not a haiku
	else return text formatted as a haiku
	"""
	
	# check suitability
	ascii_text = suitable_text(text, debug)
	if ascii_text == "":
		return ""
		
	# break text into words
	words = []
	for line in ascii_text.split("\n"):
		for word in line.split():
			words.append(word)
			
	# try to extract a first line (5 syllables)
	first_line, remaining = extract_line(words, 5, debug)
	if first_line == "":
		return ""
		
	if debug:
		print "first line ok: {0}".format(first_line)
		
	# try to extract a second line (7 syllables)
	second_line, remaining = extract_line(remaining, 7, debug)
	if second_line == "":
		return ""
		
	if debug:
		print "second line ok: {0}".format(second_line)
		
	# try to extract a third line (5 syllables)
	third_line, remaining = extract_line(remaining, 5, debug)
	if third_line == "":
		return ""
	if len(remaining) > 0:
		return ""
	
	if debug:
		print "third line ok: {0}".format(third_line)
		
	# compose haiku
	haiku = "{0}\n{1}\n{2}".format(first_line, second_line, third_line)
		
	return haiku


if __name__ == "__main__":
	print get_haiku("This reminds me of Randy's bong from Trailer Park Boys hehehe...good times", True)
	
