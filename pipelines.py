from gensim.summarization.summarizer import summarize
from nltk.tokenize import sent_tokenize
from docx import Document

     
class Extractor:
    '''
       A class to extract paragraph texts.
       Attributes will be modified when integrating with Firebase
       Current implementation includes taking docx file from local drive
       In future, this will be fetched from firebase storage. 
    '''
    def __init__(self,docPath):
        self.path = docPath
        self.document = Document(docPath)
    
    def extract(self):
        extracted_text=""
        for para in self.document.paragraphs:
            s=sent_tokenize(para.text)
            
            if(len(s)>1):extracted_text+=para.text
        return extracted_text
        

class Summarizer:
    
    def __init__(self,text,num_question):
        self.num_question = num_question
        self.text = text
    
    def _calculate_ratio(self):
        num_sentences = len(sent_tokenize(self.text))
        if(num_sentences==0): raise Exception("Empty Document!!! At least one sentance required")
        min_ratio = self.num_question/num_sentences
        return min_ratio

    def summarize(self):
        ratio = self._calculate_ratio()
        if(ratio>=1): raise Exception("Number of questions greater than document length")
        summarized_text = summarize(self.text, ratio=ratio)
        return summarized_text
