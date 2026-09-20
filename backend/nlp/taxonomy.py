"""
Curated Skill Taxonomy with canonical names, categorization, and alias mapping.
"""

SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", 
        "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R", "SQL", "Bash", "Dart"
    ],
    "Frontend Development": [
        "React", "Next.js", "Vue.js", "Angular", "Svelte", "HTML5", "CSS3", 
        "Tailwind CSS", "Redux", "Bootstrap", "Webpack", "Vite", "Responsive Design"
    ],
    "Backend Development": [
        "FastAPI", "Django", "Flask", "Node.js", "Express.js", "Spring Boot", 
        "ASP.NET", "Ruby on Rails", "NestJS", "REST APIs", "GraphQL", "Microservices", 
        "gRPC", "WebSockets"
    ],
    "Databases & Storage": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Cassandra", 
        "DynamoDB", "Elasticsearch", "Snowflake", "Oracle", "Firebase", "Neo4j"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", 
        "Jenkins", "GitHub Actions", "GitLab CI", "Ansible", "Linux", "Nginx", "Prometheus", "Grafana"
    ],
    "AI, ML & Data Science": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "LLMs", 
        "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "Hugging Face", 
        "LangChain", "Generative AI", "RAG", "Data Analysis", "Data Modeling"
    ],
    "Tools & Engineering": [
        "Git", "GitHub", "GitLab", "Jira", "Agile", "Scrum", "Unit Testing", 
        "PyTest", "Postman", "Kafka", "RabbitMQ", "Celery", "Object-Oriented Programming", "Design Patterns"
    ]
}

# Mapping all canonical skills to their category for easy lookup
SKILL_TO_CATEGORY = {}
for category, skills in SKILL_CATEGORIES.items():
    for skill in skills:
        SKILL_TO_CATEGORY[skill.lower()] = category

# Mapping variations / synonyms to canonical names
SKILL_ALIASES = {
    # Python
    "python": "Python",
    "python 3": "Python",
    "python3": "Python",
    "python programming": "Python",
    
    # JavaScript / TypeScript
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    
    # React
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "react native": "React Native",
    
    # Next.js
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    
    # Vue
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    
    # Angular
    "angular": "Angular",
    "angularjs": "Angular",
    
    # Node
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    
    # Express
    "express": "Express.js",
    "expressjs": "Express.js",
    "express.js": "Express.js",
    
    # FastAPI
    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    
    # Spring Boot
    "spring": "Spring Boot",
    "springboot": "Spring Boot",
    "spring boot": "Spring Boot",
    
    # Cloud
    "aws": "AWS",
    "amazon web services": "AWS",
    "amazon ec2": "AWS",
    "aws lambda": "AWS",
    "s3": "AWS",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "ms azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    
    # DevOps / Containers
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "kube": "Kubernetes",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "jenkins": "Jenkins",
    "github actions": "GitHub Actions",
    "gitlab ci": "GitLab CI",
    "ci/cd": "CI/CD",
    "ci-cd": "CI/CD",
    "continuous integration": "CI/CD",
    
    # Databases
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "psql": "PostgreSQL",
    "mysql": "MySQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "sqlite": "SQLite",
    "dynamodb": "DynamoDB",
    "elasticsearch": "Elasticsearch",
    "snowflake": "Snowflake",
    "sql": "SQL",
    
    # AI / ML
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "dl": "Deep Learning",
    "nlp": "NLP",
    "natural language processing": "NLP",
    "computer vision": "Computer Vision",
    "cv": "Computer Vision",
    "llm": "LLMs",
    "llms": "LLMs",
    "large language model": "LLMs",
    "large language models": "LLMs",
    "generative ai": "Generative AI",
    "genai": "Generative AI",
    "rag": "RAG",
    "retrieval augmented generation": "RAG",
    "pytorch": "PyTorch",
    "torch": "PyTorch",
    "tensorflow": "TensorFlow",
    "tf": "TensorFlow",
    "scikit-learn": "Scikit-Learn",
    "scikit learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "huggingface": "Hugging Face",
    "hugging face": "Hugging Face",
    "langchain": "LangChain",
    
    # Tools & APIs
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "rest": "REST APIs",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "restful": "REST APIs",
    "restful apis": "REST APIs",
    "graphql": "GraphQL",
    "kafka": "Kafka",
    "apache kafka": "Kafka",
    "rabbitmq": "RabbitMQ",
    "celery": "Celery",
    "pytest": "PyTest",
    "unit testing": "Unit Testing",
    "postman": "Postman",
    "agile": "Agile",
    "scrum": "Scrum",
    "jira": "Jira",
    "linux": "Linux",
    "nginx": "Nginx"
}
