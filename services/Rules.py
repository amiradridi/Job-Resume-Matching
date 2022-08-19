import ast
from Resources import DEGREES_IMPORTANCE
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Rules:

    def __init__(self, labels, resumes, jobs):
        self.labels = labels
        self.resumes = resumes
        self.jobs = jobs
        self.degrees_importance = DEGREES_IMPORTANCE

    def modifying_type_resume(self, resumes):
        for i in range(len(resumes["degrees"])):
            print(i)
            print(type(resumes["degrees"][i]))
            resumes["degrees"][i] = ast.literal_eval(resumes["degrees"][i])
        for i in range(len(resumes["skills"])):
            resumes["skills"][i] = ast.literal_eval(resumes["skills"][i])
        return resumes

    def modifying_type_job(self, jobs):
        for i in range(len(jobs["Skills"])):
            jobs["Skills"][i] = ast.literal_eval(jobs["Skills"][i])
        return jobs

    # degree matching
    @staticmethod
    def assign_degree_match(match_scores):
        """calculate a degree matching score"""
        match_score = 0
        if len(match_scores) != 0:
            if max(match_scores) >= 2:
                match_score = 0.5
            elif (max(match_scores) >= 0) and (max(match_scores) < 2):
                match_score = 1
        return match_score

    def degree_matching(self, resumes, jobs, job_index):
        """calculate the final degree matching scores between resumes and job description"""
        job_min_degree = self.degrees_importance[jobs['Minimum degree level'][job_index]]
        resumes['Degree job ' + str(job_index) + ' matching'] = 0
        for i, row in resumes.iterrows():
            match_scores = []
            for j in resumes['degrees'][i]:
                score = self.degrees_importance[j] - job_min_degree
                match_scores.append(score)
            resumes.loc[i, 'Degree job ' + str(job_index) + ' matching'] = self.assign_degree_match(match_scores)
        return resumes

    # majors matching
    def get_major_category(self, major):
        """get a major's category"""
        categories = self.labels['MAJOR'].keys()
        for c in categories:
            if major in self.labels['MAJOR'][c]:
                return c

    def get_job_acceptable_majors(self, jobs, job_index):
        """get acceptable job majors"""
        job_majors = jobs['Acceptable majors'][job_index]
        job_majors_categories = []
        for i in job_majors:
            job_majors_categories.append(self.get_major_category(i))
        return job_majors, job_majors_categories

    def get_major_score(self, resumes, resume_index, jobs, job_index):
        """calculate major matching score for one resume"""
        resume_majors = resumes['majors'][resume_index]
        job_majors, job_majors_categories = self.get_job_acceptable_majors(jobs, job_index)
        major_score = 0
        for r in resume_majors:
            if r in job_majors:
                major_score = 1
                break
            elif self.get_major_category(r) in job_majors_categories:
                major_score = 0.5
        return major_score

    def major_matching(self, resumes, jobs, job_index):
        """calculate major matching score for all resumes"""
        resumes['Major job ' + str(job_index) + ' matching'] = 0
        for i, row in resumes.iterrows():
            resumes.loc[i, 'Major job ' + str(job_index) + ' matching'] = self.get_major_score(resumes, i, jobs, job_index)
        return resumes

    # skills matching
    @staticmethod
    def unique_job_skills(jobs, job_index):
        """calculate number of unique skills in the job description"""
        unique_job_skills = []
        for i in jobs['Skills'][job_index]:
            if i not in unique_job_skills:
                unique_job_skills.append(i)
        num_unique_job_skills = len(unique_job_skills)
        return num_unique_job_skills, unique_job_skills

    def semantic_similarity(self, job, resume):
        model = SentenceTransformer('all-mpnet-base-v2')
        # Encoding:
        score = 0
        sen = job + resume
        sen_embeddings = model.encode(sen)
        for i in range(len(job)):
            if job[i] in resume:
                score += 1
            else:
                if max(cosine_similarity([sen_embeddings[i]], sen_embeddings[len(job):])[0]) >= 0.4:
                    score += max(cosine_similarity([sen_embeddings[i]], sen_embeddings[len(job):])[0])
                    # print(job[i],max(cosine_similarity([sen_embeddings[i]],sen_embeddings[len(job):])[0]),cosine_similarity([sen_embeddings[i]],sen_embeddings[len(job):])[0])
        score = score / len(job)
        return round(score, 2)

    def skills_semantic_matching(self, resumes, job_index,job_skills):
        """calculate the skills semantic matching scores between resumes and job description"""
        resumes['Skills job ' + str(job_index) + ' semantic matching'] = 0
        for i, row in resumes.iterrows():
            resumes.loc[i, 'Skills job ' + str(job_index) + ' semantic matching'] = \
                self.semantic_similarity(job_skills, resumes['skills'][i])
        return resumes

    # calculate matching scores
    def matching_score(self, resumes, jobs, job_index):
        # matching degrees
        resumes = self.degree_matching(resumes, jobs, job_index)
        # matching majors
        resumes = self.major_matching(resumes, jobs, job_index)
        # matching skills
        num_unique_job_skills, job_skills = self.unique_job_skills(jobs, job_index)
        # matching skills semantically
        resumes = self.skills_semantic_matching(resumes, job_index, job_skills)
        resumes["matching score job " + str(job_index)] = 0
        resumes["job index"] = job_index
        for i, row in self.resumes.iterrows():
            skills_score = resumes['Skills job ' + str(job_index) + ' semantic matching'][i]
            degree_score = resumes['Degree job ' + str(job_index) + ' matching'][i]
            major_score = resumes['Major job ' + str(job_index) + ' matching'][i]
            final_score = (skills_score + degree_score + major_score) / 3
            resumes.loc[i, "matching score job " + str(job_index)] = round(final_score, 3)
        return resumes
