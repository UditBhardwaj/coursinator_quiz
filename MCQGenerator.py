import random
from pipelines import Summarizer
from KeywordExtraction import KeywordExtraction
from distractor import get_distractors_conceptnet

class MCQGenerator:
    def __init__(self,text,num_question):
        self.num_question = num_question
        self.summarizer = Summarizer(text,num_question)
        # Will Summarize depending on the length of content when uploaded in Courses
        # self.summary = self.summarizer.summarize() 
        self.keyword_extractor = KeywordExtraction(text)
    
    def generate(self):
        sent_key = self.keyword_extractor.extract()
        questions=[]
        for candidate in sent_key:
            sentence,keys = candidate["sentence"],candidate["keywords"]
            qualified_distractors=[]
            qualified_key=""
            for key in keys:
                distractors = get_distractors_conceptnet(key['text'])
                if(len(distractors)>3):
                    qualified_distractors=distractors
                    qualified_key=key['text']
                    sentence_with_blank = sentence[:key['start']]+"_"*10 + sentence[key['end']:]
                    break
            if(len(qualified_distractors)<3):continue
            options=qualified_distractors[:3]+[qualified_key]
            random.shuffle(options)
            more_wrong_choices = [] if len(qualified_distractors)<4 else qualified_distractors[3:]
            questions.append({
                "sentence":sentence_with_blank,
                "key": qualified_key,
                "options":options,
                "more_wrong_choices":more_wrong_choices
            })
            if(len(questions)==self.num_question):break
        return questions