"""Generate synthetic LinkedIn job postings dataset for AU analyst roles."""
import pandas as pd, numpy as np, os
np.random.seed(99)
n = 2000
titles = ['Data Analyst','Business Analyst','BI Analyst','Reporting Analyst','Systems Analyst',
          'Senior Data Analyst','Senior Business Analyst','Junior Data Analyst','Associate BA','Insights Analyst']
title_w=[0.18,0.20,0.12,0.10,0.08,0.10,0.09,0.07,0.04,0.02]
companies=['Deloitte','PwC','KPMG','ANZ Bank','Commonwealth Bank','Woolworths','Telstra',
           'NAB','Amazon','Department of Health','AGL','Optus','REA Group','Seek','Coles']
cities=['Melbourne','Sydney','Brisbane','Perth','Adelaide','Canberra','Remote']
city_w=[0.32,0.28,0.16,0.10,0.06,0.04,0.04]
industries=['Finance','Technology','Government','Consulting','Retail','Healthcare','Energy','Property']
skills_pool=['Power BI','SQL','Python','Excel','Tableau','Agile','Jira','Azure','AWS',
             'Stakeholder Management','R','Machine Learning','Looker','BPMN','DAX']
exp_levels=['Graduate/<1yr','1-3 years','3-5 years','5+ years']
exp_w=[0.12,0.35,0.35,0.18]

records=[]
for i in range(n):
    title=np.random.choice(titles,p=title_w)
    exp=np.random.choice(exp_levels,p=exp_w)
    base=75000 if 'Junior' in title or 'Graduate' in exp else (95000 if 'Senior' in title else 82000)
    salary=int(np.random.normal(base,12000)/1000)*1000
    salary=max(55000,min(145000,salary))
    n_skills=np.random.randint(3,9)
    job_skills=list(np.random.choice(skills_pool,n_skills,replace=False))
    # Make Power BI and SQL more common
    if np.random.rand()<0.67 and 'Power BI' not in job_skills: job_skills[0]='Power BI'
    if np.random.rand()<0.82 and 'SQL' not in job_skills: job_skills[1 % len(job_skills)]='SQL'
    records.append({
        'job_id':f'J{i:04d}','title':title,'company':np.random.choice(companies),
        'city':np.random.choice(cities,p=city_w),'industry':np.random.choice(industries),
        'experience_required':exp,'salary_aud':salary,
        'skills':','.join(job_skills),
        'remote_ok':np.random.choice([0,1],p=[0.55,0.45]),
        'visa_sponsor':np.random.choice([0,1],p=[0.78,0.22]),
        'posted_year':np.random.choice([2024,2025,2026],p=[0.25,0.40,0.35])
    })

df=pd.DataFrame(records)
os.makedirs(os.path.dirname(__file__),exist_ok=True)
df.to_csv(os.path.join(os.path.dirname(__file__),'linkedin_jobs_sample.csv'),index=False)
print(f"Generated {len(df)} job records")
