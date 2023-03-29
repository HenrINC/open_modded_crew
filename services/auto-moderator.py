from services.abstract_service import AbstractService
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class Service(AbstractService):
    """
Builtin service that moderates the crew messages based on the "unitary/toxic-bert" model
In the future admin should be able to tweak the model and the threshold    
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed: list[str]
        if "processed" in kwargs:
            self.processed = kwargs["processed"]
        else:
            self.processed = []
        self.model_name = "unitary/toxic-bert"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.threshold = 0.01
        self.processed = []
    
    def get_toxicity(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=-1)
        toxicity = probabilities[:, 1].item()
        
        return toxicity

    def on_post(self, posts):
        for post in posts[:50]:
            post_id = post["id"]
            #TODO Add broadcast messages
            if post["type"] == "wrote_crew_wall_message" and \
                post_id not in self.processed: 
                content = post["content"]
                toxicity = self.get_toxicity(content)
                #For some reason the more toxic, the lower the toxicity
                if toxicity < self.threshold: 
                    self.connector.delete_post(post_id)
                print(f"Toxicity : {toxicity}, content : {content}")
                self.processed.append(post_id)
        self.processed = self.processed[:50]
                
    def start(self):
        self.running = True
