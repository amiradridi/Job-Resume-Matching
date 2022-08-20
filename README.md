# Job Resume Matching Project

# Problem
Matching the best profiles to a job description may be a difficult and time-consuming task.
In fact, the traditional way that recruiters are using to select candidates doesn't take into consideration all important details. Recruiters have to screen all the applications manually and then calculate the similarity in an efficient way.

# Solution
<p align="center">
  <img src="./Resources/Project documentation/ai in recruitement.png" width="650" title="AI in recruitement" alt="benefits of AI in recruitement">
 </p>

The idea is to calculate the similarity between the resume and the job description and then return the resumes with the highest similarity score.

## 1st step: information retrieval
  Information Extraction is the task of automatically extracting structured information such as entities, relationships between entities, and attributes describing
entities from unstructured sources. Our system uses spacy PhraseMatcher to extract the information from job descriptions.
We prepared a dictionary that has all education degrees categories, all majors and skills categories related to computer engineering field. We fed that dictionary to the Spacy rule-based PhraseMatcher in order to detect and recognize entities in our job description.
The job information extraction would look like:

<p align="center">
  <img src="./Resources/Project documentation/Job entities example1.png" width="700" title="Job information extraction example" alt="Job information extraction example">
</p>
  
Our structured job descriptions dataset :

<p align="center">
  <img src="./Resources/Project documentation/Job data.png" width="650" title="Job descriptions dataset" alt="Job descriptions dataset">
 </p>

## 2nd step: Matching rules
  We implemented matching rules to calculate the similarity between the resume and the job description. Those matching rules don't only use simple keywords matching but also ontology matching techniques.
 
  #### * Education section matching rules
  <p align="center">
  <img src="./Resources/Project documentation/Education rules.png" width="650" title="Education matching rule" alt="Education matching rule">
  </p>
  
  #### * Majors section matching rules
  <p align="center">
  <img src="./Resources/Project documentation/Majors rules.png" width="600" title="Majors matching rule" alt="Majors matching rule">
  </p>
  
  #### * Skills section matching rules
  
  
  In this part, we will use semantic similarity-based approach to match resumes' skills and jobs' skills.
  Semantic similarity approach is the task of searching for documents or sentences (resumes) which contain semantically similar content to a search document           (the job description).
  
  We tried different pre-trained models to embed our words (GPT3 and SBERT 'all-mpnet-base-v2').
  Embeddings are a key part of modern NLP, they encode the meaning of words or other linguistic units into vectors of numbers.
  We evaluated the results on 27 skills and we chose the sbert model since it gives better semantic similarity and dissimilarity with respect to the skills           vocabulary context as shown below:
  
  SBERT skills matching results:
  
  <p align="center">
  <img src="./Resources/Project documentation/evaluation_sbert.png" width="650" title="evaluation_sbert" alt="evaluation_sbert">
  </p>
  
  GPT3 skills matching results:
  
  <p align="center">
  <img src="./Resources/Project documentation/evaluation_gpt.png" width="650" title="evaluation_gpt" alt="evaluation_gpt">
  </p>
  
  
  GPT3 and SBERT matching skills results comparaison:
  
  <p align="center">
  <img src="./Resources/Project documentation/evaluation_gpt_sbert.png" width="650" title="evaluation_gpt_sbert" alt="evaluation_gpt_sbert">
  </p>
  
  
  ***GPT3 doesn't make obvious difference between skills and it affects a high similarity score to all skills even dissimilar ones.***
  
  
  The steps that we followed later on to calculate the similarity between the job and the resume:
  
  1. We derive semantically meaningful word and sentence embeddings using the chosen Siamese BERT-Networks pretrained model ‘all-mpnet-base-v2’ that has these             specificities:
   <p align="center">
   <img src="./Resources/Project documentation/pre-trained sbert model.png" width="650" title="pre-trained sbert model" alt="pre-trained sbert model">
   </p>
   <p align="center">
   <img src="./Resources/Project documentation/sbert_models_differences.png" width="650" title="sbert_models_differences" alt="sbert_models_differences">
   </p>
   
   
  2. We compare those embeddings with cosine similarity to find the nearest resumes to the job description
     Cosine similarity is defined as the inner product of two vectors divided by the product of their length. Cosine similarity is defined as:
     <p align="center">
     <img src="./Resources/Project documentation/cosine similarity.png" width="650" title="cosine similarity" alt="cosine similarity">
     </p>
     where vectors a and b have the same number of dimensions N. Cosine similarity can be used to compare similarity between document vectors.
          
   We tried that approach on both skills words and skills sentences of four resumes’ levels: 
   
   * Lowest_resume: resume skills are far away from the job description required skills 
         
   * Low_resume: resume skills are a bit far from the job description required skills
         
   * Intermediate_resume: resume skills are related to the job description skills
         
   * High_resume: most resume skills exist or relate very well with the job description required skills
         
   * High_plus_resume: most resume skills existor relate very well with the job description required skills and there are extra skills
         
   These are our samples:
           
   Job description:
    <p align="center">
    <img src="./Resources/Project documentation/Job_description_example.png" width="650" title="Job_description_example" alt="Job_description_example">
    </p>
            
   Lowest_resume:
    <p align="center">
    <img src="./Resources/Project documentation/Lowest_resume_example.png" width="650" title="Lowest_resume_example" alt="Lowest_resume_example">
    </p>
            
   Low_resume:
    <p align="center">
            <img src="./Resources/Project documentation/Low_resume_example.png" width="650" title="Low_resume_example" alt="Low_resume_example">
    </p>
            
   Intermediate_resume:
    <p align="center">
    <img src="./Resources/Project documentation/Intermediate_resume_example.png" width="650" title="Intermediate_resume_example"                    alt="Intermediate_resume_example">
    </p>
            
   High_resume:
    <p align="center">
    <img src="./Resources/Project documentation/High_resume_example.png" width="650" title="High_resume_example" alt="High_resume_example">
    </p>
            
   High_plus_resume:
    <p align="center">
    <img src="./Resources/Project documentation/High_plus_resume_example.png" width="650" title="High_plus_resume_example" alt="High_plus_resume_example">
    </p>
            
            
            
   Evaluation:
   
   
 |                     | Semantic similarity on Word embeddings  | Semantic similarity on Sentence embeddings |
 | ------------------- | --------------------------------------- | ------------------------------------------ |
 | Lowest_resume       | 0.19                                    | 0.08                                       |
 | Low_resume          | 0.37                                    | 0.48                                       |
 | Intermediate_resume | 0.58                                    | 0.45                                       |
 | High_resume         | 0.74                                    | 0.82                                       |
 | High_plus_resume    | 0.77                                    | 0.74                                       |
    
    

  ***Semantic similarity on word embeddings approach works better for two reasons:***
   1.	It tries to find related skills if a required skill doesn’t exist in the resume
   2.	It values the fact that a resume has plus skills while sentence-based approach makes the resume’s vector representation with plus skills far a way                   from the job description

  <p>Visit <a href="https://github.com/amiradridi/Job-Resume-Matching/blob/master/services/Semantic%20similarity.ipynb">this notebook</a> for the full code of the semantic similarity approach.</p>

  

 
* 3rd step: 
  We Calculated the final similarity score and returned the resumes with the highest similarity score.
  
  
 ## Project summary
 
 1. We retrieved information from the job description using Spacy brule-based PhraseMatcher
 2. We implemented matching rules for the degrees' levels and the acceptable majors
 3. We compared between two powerful word embedding models gpt3 and sbert 'all-mpnet-base-v2' and we chose sbert for its efficiency
 4. We compared between word embedding and sentence embedding approaches and we chose word embedding as it produces accurate semantic similarity

 ## References
 
 <p><a href="https://arxiv.org/abs/1908.10084">Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks paper</a></p>
 <p><a href="https://www.sbert.net/docs/pretrained_models.html">Sbert pretrained models official documentation</a></p>
 <p><a href="https://pypi.org/project/sentence-transformers/0.3.2/">Sentence embeddings documentation</a></p>


