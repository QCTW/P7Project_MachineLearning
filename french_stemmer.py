import treetaggerwrapper

class FrenchStemmer:
    def __init__(self):
        self.tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')


    def stem(self, s):
        tags = self.tagger.tag_text(s)
        tags_list = treetaggerwrapper.make_tags(tags, exclude_nottags=True)
        stems = []
        for t in tags_list:
            ss = t.lemma.split("|")
            stems = stems + ss
        return stems

