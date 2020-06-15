import utils.utils as utils
from cereproc.cerecloud_rest import CereprocRestAgent


# Rootio account
# restagent = CereprocRestAgent("https://cerevoice.com/rest/rest_1_1.php", "5aec2e36c429d", "VkZmL42e5L")
# Kristen account
restagent = CereprocRestAgent("https://cerevoice.com/rest/rest_1_1.php", "5ced1a69273fe", "z6rqSLhjNV")

credits = restagent.cprc_get_credit()

for c in credits:
	print("free credit " + str(c[0].text))
	print("Paid credit " + str(c[1].text))
	print("All credit " + str(c[2].text))

# voices = restagent.cprc_list_voices()[0]

# for v in voices:
# 	for f in v:
# 		print(f.text.encode('UTF-8'))
# 	print('\n')