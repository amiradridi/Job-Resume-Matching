# Job Resume Matching Project

## Problem
Matching the best profiles to a job description may be a difficult and time-consuming task.
In fact, the traditional way that recruiters are using to select candidates doesn't take into consideration all important details. Recruiters have to screen all the applications manually and then calculate the similarity in an efficient way.

## Solution

The idea is to calculate the similarity between the resume and the job description and then return the resumes with the highest similarity score.

* 1st step: information retrieval
  Information Extraction is the task of automatically extracting structured information such as entities, relationships between entities, and attributes describing
entities from unstructured sources. Our system uses spacy PhraseMatcher to extract the information from job descriptions.
We prepared a dictionary that has all education degrees categories, all majors and skills categories related to computer engineering field. We fed that dictionary to the Spacy rule-based PhraseMatcher in order to detect and recognize entities in our job description.
The job information extraction would look like:

<p align="center">
  <img src="./Resources/Project documentation/Job entities example1.png" width="650" title="Majors matching rule" alt="Majors matching rule">
</p>
  
Our structured job descriptions data :

<p align="center">
  <img src="./Resources/Project documentation/Job data.png" width="650" title="Majors matching rule" alt="Majors matching rule">
 </p>

* 2nd step: Matching rules
  We implemented matching rules to calculate the similarity between the resume and the job description. Those matching rules don't only use simple keywords matching but also ontology matching techniques.
 
  * Education section matching rules
  <p align="center">
  <img src="./Resources/Project documentation/Education rules.png" width="650" title="Education matching rule" alt="Education matching rule">
  </p>
  
  * Majors section matching rules
  <p align="center">
  <img src="./Resources/Project documentation/Majors rules.png" width="650" title="Majors matching rule" alt="Majors matching rule">
  </p>
  
  * Skills section matching rules
  <p align="center">
  <img src="./Resources/Project documentation/Skills rules.png" width="650" title="Skills matching rule" alt="Skills matching rule">
  </p>
 
* 3rd step: 
  We Calculated the final similarity score and returned the resumes with the highest similarity score.
