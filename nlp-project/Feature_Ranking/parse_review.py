import os,sys,nltk,re,pickle

def parseData(sourceDir, destDir):
	sourceFiles = os.listdir(sourceDir)
	html_tags = re.compile(r'<[^>]+>')
	count = 0
	grammar = r"""
NP:	{<JJ|JJR|JJS|VBG><NN|NNS>}
	{<RB><JJ>}
	{<RB|RBR|RBS><VB|VBD|VBG|VBP|VBZ>}
	{<VBP><VBG>}
				
"""	
	chunker = nltk.RegexpParser(grammar)		
	for file in sourceFiles:
		filepath = sourceDir+"/"+file;
		data = pickle.load(open(filepath,'rb'))
		result = []
		for review in data:
			temp = []
			for sent in review[1]:
				tree = chunker.parse(sent)
				for sub in tree:
					pair = []
					if type(sub) is nltk.Tree:
						for l in sub:
							pair.append(l[0].lower())
					if len(pair) > 0:
						temp.append(pair)
			result.append([review[0],temp])	 
		outFile = open(destDir+"/"+file,'wb')
		#outFile.write(str(result))
		pickle.dump(result,outFile)
		#outFile.close()
		count += 1
		sys.stderr.write(str(count*100/len(sourceFiles)) +"% completed.\n")

if __name__ == "__main__":
	parseData(str(sys.argv[1]),str(sys.argv[2]))
