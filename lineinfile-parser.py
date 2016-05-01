#!/usr/bin/env python3
import os
import re
import glob
import json
import logging

FORMAT = '%(levelname)s:	%(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

#, line 26, column 3,

expressions = [
#	"""[']?(\~?/?([[:letter:][:number:]._-]+/+)+[[:letter:][:number:]._-]+)[']?:(?:,?\sline\s)?(\d+)""",
#	""".*?[']?([\.\/~]?[^:\s]+)[']?:(\d+):?(?:,?\sline\s)?(\d+)?(?:,\scolumn\s)?(\d+)?.*?""",
	""".*?[']?([\.\/~]?[^:\s]+)[']?:(\d+):?(?:,?\sline\s)?(\d+)?(?:,\scolumn\s)?(\d+)?.*?""",
#	r""".*(\d+).*""",
]

matches = 0
for f in glob.glob('tests/*.txt'):
   logging.debug("file: %s", f)
   for expr in expressions:
       j = []
       for i in json.load(open(f.replace('.txt', '.json'))):
           item = [str(x) for x in i[1:]] 
           item.insert(0, i[0])
           if len(item) < 3:
               #logging.error(item)
               item.append('')
           j.append( tuple(item) )
       logging.info("expected=%s", j)

       pattern = re.compile(expr, re.UNICODE)
       results = pattern.findall(open(f).read())
       for x in results:
           x = tuple(x[:3])
           #logging.debug("found: %s", x)
           if x in j:
               #logging.debug("removing %s", x)
               j.remove(x)
               #logging.debug(j)
               matches += 1
       if j:
           logging.error("Failed to find all matches in %s\n\tmissing:%s\n\tresults: %s", f, j, results)


logging.info("Success with %s matches!" % matches)
