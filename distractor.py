import requests
import json
import logging as log
import logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
log.basicConfig(level=log.DEBUG)
# class DistractorGenerator:

#     def __init__(self):
#         self.keyword = keyword

#     # Distractors from http://conceptnet.io/
def get_distractors_conceptnet(keyword):
    log.debug(f"Distractors for {keyword} ")
    word = keyword.lower()
    if (len(word.split())>0):
        word = word.replace(" ","_")
    distractor_list = []
    urls=[
        f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/PartOf&start=/c/en/{word}&limit=2",
        f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/IsA&start=/c/en/{word}&limit=2",
        f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/RelatedTo&start=/c/en/{word}&limit=2",
        f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/AtLocation&start=/c/en/{word}&limit=2",
        f"http://api.conceptnet.io/query?node=/c/en/{word}&rel=/r/Antonym&start=/c/en/{word}&limit=2",
    ]
    edges=[]
    for url in urls:
        obj = requests.get(url).json()
        edges+= obj['edges']
    edges = sorted(edges,key=lambda x:x['weight'],reverse=True)
    distractor_edges=[]
    for edge in edges:
        link = edge['end']['label'] 
        relation = edge['rel']['label']
        endurls={
            'PartOf': f'http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/PartOf&end=/c/en/{link}&limit=4',
            'IsA': f'http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/IsA&end=/c/en/{link}&limit=4',
            'RelatedTo': f'http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/RelatedTo&end=/c/en/{link}&limit=4',
            'AtLocation': f'http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/AtLocation&end=/c/en/{link}&limit=4',
            'Antonym': f"http://api.conceptnet.io/query?node=/c/en/{link}&rel=/r/Antonym&end=/c/en/{link}&limit=4",
        }
        if(relation=="Antonym"):
            edge['weight']*=20
            edge['start']['label']=edge['end']['label']
            distractor_edges.append(edge)
            continue
        obj2 = requests.get(endurls[relation]).json()
        distractor_edges+=obj2['edges']
        # print(f"{relation}, {link}\n{endurls[relation]}\nAdded {len(obj2['edges'])}")

        
    distractor_edges = sorted(distractor_edges,key=lambda x:x['weight'],reverse=True)
    for edge in distractor_edges:
        distractor = edge['start']['label']
        log.debug(f"(End:{edge['end']['label']},\t Start:{distractor},\t rel:{edge['rel']['label']},\t wt:{edge['weight']})")
        if(distractor.lower() not in distractor_list and distractor.lower()!= word ): distractor_list.append(distractor.lower())
            
    return distractor_list
