
import subprocess


def get_phoneme_strings(text, debug=False):
	"""
	return phoneme string generated by
	$ espeak -x -q "@text"
	"""
	
	# remove double quotes,
	# and double square brackets (used to denote phoneme text in espeak, so will confuse it)
	prepared_text = text.replace("\"", "").replace("[[", "").replace("]]", "")
	# surround with double quotes
	quoted_text = "\"{0}\"".format(prepared_text)
	
	if debug:
		print prepared_text
	
	# translate with espeak
	result = subprocess.check_output(["espeak", "-x", "-q", quoted_text])
	
	# split at newlines, strip whitespace
	result_lines = []
	for line in result.split("\n"):
		stripped = line.strip()
		if len(stripped) > 0:
			result_lines.append(stripped)
	
	if debug:
		for line in result_lines:
			print "->\t{0}".format(line)
	
	return result_lines
	
	
