import french_stemmer as fs

class TermFrequencyWithRef:
    def __init__(self, ref_path):
        self.dict = {}
        self.count = 0
        self.stemmer = fs.FrenchStemmer()
        try:
            with open(ref_path, 'r') as f:
                for line in f:
                    one_line = line.strip()
                    if( (len(one_line)!=0) and not (one_line.startswith("#")) ):
                        self.count+=1
                        self.dict[one_line] = 0
                f.close()
                print("Total: "+str(self.count)+" words found in the referenced file.")
        except IOError as e:
            print("Unable to open file: "+ref_path+ "; "+e)

    def freq(self, phrase):
        stems = self.stemmer.stem(phrase)
        if (len(stems)==0) :
            return 0
        count = 0
        for t in stems:
            if t in self.dict:
                count+=1
        
                
        return float(count)/len(stems)