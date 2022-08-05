import pickle
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
from Resources import ENTITIES
from Resources import DEGREES_IMPORTANCE


class JobInfoExtraction:

    def __init__(self, labels, jobs, nlp):
        self.labels = labels
        self.jobs = jobs[['Qualifications']]
        self.nlp = nlp
        self.entities = ENTITIES
        self.degrees_importance = DEGREES_IMPORTANCE

    def add_section_patterns(self, entities, section, matcher):
        """add section patterns to the matcher"""
        sub_sections = []
        for key, value in self.labels[section].items():
            sub_sections.append(key)
            # if section != "SKILL":
                # sections[key] = section
        for sub_section in sub_sections:
            entities.append(sub_section)
            sub_section_pattern_name = str(sub_section)
            pattern_name = str(sub_section) + '-' + 'patterns'
            pattern_name = []
            for j in self.labels[section][sub_section]:
                pattern_name.append(self.nlp(j))
            matcher.add(sub_section_pattern_name, pattern_name)
        return entities

    def build_matcher(self, section):
        """building section's matcher"""
        matcher = PhraseMatcher(self.nlp.vocab)
        entities = []
        # adding section entity and patterns

        entities = self.add_section_patterns(entities, section, matcher)
        return matcher, entities

    def get_matcher(self, section):
        """loading matcher
        with open('Resources/models/' +str(section) + 'matcher.pkl', 'rb') as f:
            my_matcher = pickle.load(f)"""
        my_matcher, entities = self.build_matcher(section)
        return my_matcher

    def match_by_spacy(self, nlp, job, section):
        """applying matcher to extract entities"""
        for i in self.entities:
            nlp.vocab.strings.add(str(i))
        text = job.lower()
        doc = nlp(text)
        matcher = self.get_matcher(section)
        matches = matcher(doc)
        result = []

        for match_id, start, end in matches:
            # create a new Span for each match
            span = Span(doc, start, end, label=match_id)
            doc.ents = list(doc.ents) + [span]  # add span to doc.ents
            label = nlp.vocab.strings[match_id]
            item = span.text
            if (section == "MAJOR") and (item not in result):
                result.append(item)
            elif (section == "DEGREE") and (label not in result):
                result.append(label)
            elif section == "SKILL":
                result.append(item)
        return result

    @staticmethod
    def get_minimum_degree(self, degrees):
        """get the minimum degree that the candidate has"""
        d = {degree: self.degrees_importance[degree] for degree in degrees}
        return min(d, key=d.get)

    def extract_entities(self, jobs):
        # recognize and extract entities
        jobs['Minimum degree level'] = ""
        jobs['Acceptable majors'] = ""
        jobs['Skills'] = ""
        for i, row in jobs.iterrows():
            job = jobs['Qualifications'][i].replace('. ', ' ')
            degrees = self.match_by_spacy(self.nlp, job, "DEGREE")
            jobs['Minimum degree level'][i] = self.get_minimum_degree(self,degrees)
            jobs['Acceptable majors'][i] = self.match_by_spacy(self.nlp, job, "MAJOR")
            jobs['Skills'][i] = self.match_by_spacy(self.nlp, job, "SKILL")
        return jobs
