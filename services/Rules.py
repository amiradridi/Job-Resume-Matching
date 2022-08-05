import ast
from Resources import DEGREES_IMPORTANCE

class Rules:

    def __init__(self, labels, resumes, jobs):
        self.labels = labels
        self.resumes = resumes
        self.jobs = jobs
        self.degrees_importance = DEGREES_IMPORTANCE

    def modifying_type_resume(self, resumes):
        for i in range(len(resumes["degrees"])):
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

    # matching majors
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

    # matching skills
    @staticmethod
    def unique_job_skills(jobs, job_index):
        """calculate number of unique skills in the job description"""
        unique_job_skills = []
        for i in jobs['Skills'][job_index]:
            if i not in unique_job_skills:
                unique_job_skills.append(i)
        num_unique_job_skills = len(unique_job_skills)
        return num_unique_job_skills, unique_job_skills

    def skills_matching(self, resumes, job_index, num_unique_job_skills, unique_job_skills):
        """calculate the skills matching scores between resumes and job description"""
        resumes['Skills job ' + str(job_index) + ' matching'] = 0
        for i, row in resumes.iterrows():
            common_skills = []
            for skill in resumes['skills'][i]:
                if (skill not in common_skills) and (skill in unique_job_skills):
                    common_skills.append(skill)
            resumes.loc[i, 'Skills job ' + str(job_index) + ' matching'] = round(len(common_skills) / num_unique_job_skills,2)
        return resumes

    # calculate matching scores
    def matching_score(self, resumes, jobs, job_index):
        resumes = self.modifying_type_resume(resumes)
        #jobs = self.modifying_type_job(jobs)
        # matching degrees
        resumes = self.degree_matching(resumes, jobs, job_index)
        # matching majors
        resumes = self.major_matching(resumes, jobs, job_index)
        # matching skills
        num_unique_job_skills, job_skills = self.unique_job_skills(jobs, job_index)
        resumes = self.skills_matching(resumes, job_index, num_unique_job_skills, job_skills)
        resumes["matching score job " + str(job_index)] = 0
        for i, row in self.resumes.iterrows():
            skills_score = resumes['Skills job ' + str(job_index) + ' matching'][i]
            degree_score = resumes['Degree job ' + str(job_index) + ' matching'][i]
            major_score = resumes['Major job ' + str(job_index) + ' matching'][i]
            final_score = (skills_score + degree_score + major_score) / 3
            resumes.loc[i, "matching score job " + str(job_index)] = round(final_score,2)
        return resumes
