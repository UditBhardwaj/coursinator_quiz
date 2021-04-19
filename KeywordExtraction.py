import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm


class KeywordExtraction :
    def __init__(self , text):
        self.text = text
        self.nlp = en_core_web_sm.load()
        self.doc = self.nlp(self.text)
    def extract(self):
        sentences = [x for x in self.doc.sents]
        sentkeyword = []
        for sent in sentences:
            keywords=[]
            for named_entity in self.nlp(str(sent)).ents:
                keywords.append({
                    "text":str(named_entity.text),
                    "start":int(named_entity.start_char),
                    "end":int(named_entity.end_char),
                    "tag":str(named_entity.label_)
                })
                
            if len(keywords) == 0 :
                continue
                
            sentkeyword.append({"sentence":sent.text,"keywords":keywords})
            
        return sentkeyword