
import espeak


# vowel sounds (note "0" is a _zero_, not an uppercase "o")
# from http://espeak.sourceforge.net/phonemes.html
EXCEPTIONS_3 = ["dnt"] # didn't -> d'Idnt
VOWELS_3 = ["aI@", "aU@"]
VOWELS_2 = ["3:", "@L", "@2", "@5", "aa", "a#", "A:", "A@", "e@", "I2", "i:", "i@", "u:", "U@", "O:", "O@", "o@", "aI", "eI", "OI", "aU", "oU"]
VOWELS_1 = ["@", "3", "a", "E", "I", "i", "0", "V", "U", "e", "o", "y", "Y"]
VOWELS = EXCEPTIONS_3 + VOWELS_3 + VOWELS_2 + VOWELS_1


def count_phoneme_syllables(phoneme, debug=False):
	"""
	return number of syllables in a phoneme string
	"""
	
	count = 0
	remaining = phoneme
	
	for vowel in VOWELS:
		# count how many of this vowel
		vowel_count = remaining.count(vowel)
		
		if debug:
			if vowel_count > 0:
				print "{0}: {1} occurence".format(vowel, vowel_count)
			
		count += vowel_count
		
		# remove occurences of this vowel from remaining
		remaining = remaining.replace(vowel, "")
		
	return count
	


def count_text_syllables(text, debug=False):
	"""
	return number of syllables in text
	"""
	
	# convert to phonemes
	phoneme_strings = espeak.get_phoneme_strings(text.lower(), debug)
	
	# count syllables
	total_count = 0
	
	for line in phoneme_strings:
		line_count = count_phoneme_syllables(line, debug)
		
		if debug:
			print "{0} syllables: {1}".format(line_count, line)
			
		total_count += line_count

	return total_count
	
	
