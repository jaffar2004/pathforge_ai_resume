"""Transparent skill vocabulary and role requirements for PathForge AI."""
SKILLS = {
    "Python": ["python", "python3", "py"],
    "Java": ["java", "jdk"],
    "C": [" c programming", " c language", "c language"],
    "C++": ["c++", "cpp"],
    "JavaScript": ["javascript", "js", "ecmascript"],
    "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs"],
    "Data Structures": ["data structures", "dsa"],
    "Algorithms": ["algorithms", "algorithm design"],
    "Statistics": ["statistics", "statistical analysis", "probability"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "neural networks", "cnn", "rnn"],
    "NLP": ["natural language processing", "nlp"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow", "keras"],
    "PyTorch": ["pytorch"],
    "Git": ["git", "github", "gitlab", "version control"],
    "Linux": ["linux", "unix", "bash", "shell scripting"],
    "Docker": ["docker", "containers", "containerization", "containerisation"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["microsoft azure", "azure"],
    "Networking": ["computer networks", "networking", "tcp/ip"],
    "Cybersecurity": ["cybersecurity", "information security", "penetration testing"],
    "Databases": ["database design", "dbms", "database management"],
    "REST APIs": ["rest api", "restful api", "api development"],
}

# Values are importance weights (0.5–1.0) and target proficiency (0–100).
def _role(weights):
    return {skill: {"weight": weight, "target": target}
            for skill, weight, target in weights}

ROLES = {
    "AI Engineer": _role([
        ("Python",1,85),("Data Structures",.7,65),("Algorithms",.7,65),
        ("Statistics",.9,75),("Machine Learning",1,85),("Deep Learning",1,80),
        ("NLP",.8,70),("NumPy",.8,75),("Pandas",.8,75),
        ("Scikit-learn",.8,75),("TensorFlow",.7,65),("PyTorch",.8,70),
        ("Git",.6,60),("Linux",.5,55),("REST APIs",.6,60)
    ]),
    "Data Scientist": _role([
        ("Python",1,85),("SQL",.9,80),("Statistics",1,85),("Machine Learning",1,80),
        ("Pandas",1,85),("NumPy",.9,80),("Scikit-learn",.9,75),
        ("Data Structures",.5,55),("Algorithms",.5,55),("Deep Learning",.6,60),
        ("NLP",.6,60),("Git",.5,55),("Databases",.7,65)
    ]),
    "Data Analyst": _role([
        ("SQL",1,85),("Python",.8,70),("Statistics",.9,75),("Pandas",.9,80),
        ("NumPy",.6,60),("Databases",.8,75),("Excel",.8,70),
        ("Git",.4,45),("Networking",.3,40)
    ]),
    "Software Developer": _role([
        ("Python",.7,70),("Java",.9,80),("C++",.7,65),("Data Structures",1,85),
        ("Algorithms",1,85),("SQL",.7,65),("Git",.9,80),("Linux",.6,60),
        ("Databases",.7,65),("REST APIs",.7,65)
    ]),
    "Web Developer": _role([
        ("HTML",1,90),("CSS",1,90),("JavaScript",1,85),("React",.9,75),
        ("Node.js",.7,65),("SQL",.6,55),("Git",.8,70),("REST APIs",.8,70),
        ("Python",.4,45),("Databases",.5,55)
    ]),
    "Backend Developer": _role([
        ("Python",.8,75),("Java",.8,75),("SQL",1,85),("Databases",1,85),
        ("REST APIs",1,85),("Data Structures",.8,70),("Algorithms",.8,70),
        ("Git",.8,70),("Linux",.8,70),("Docker",.7,65),("Networking",.7,65)
    ]),
    "Cybersecurity Analyst": _role([
        ("Networking",1,85),("Linux",.9,80),("Cybersecurity",1,85),
        ("Python",.7,65),("C",.5,55),("SQL",.5,55),("Git",.5,50),
        ("Databases",.5,55)
    ]),
    "Cloud/DevOps Engineer": _role([
        ("Linux",1,85),("Networking",.9,80),("Docker",1,85),
        ("Kubernetes",.9,75),("AWS",.9,75),("Azure",.7,65),
        ("Python",.7,65),("Git",.9,80),("REST APIs",.5,55),
        ("Databases",.5,55)
    ]),
}

RESOURCE_GUIDE = {
    "Python": ("Beginner-to-intermediate Python course", "Build a command-line student record manager"),
    "SQL": ("SQL fundamentals and query practice", "Design a small college database and write 15 queries"),
    "Statistics": ("Descriptive statistics and probability lessons", "Analyse a small dataset and explain its distributions"),
    "Machine Learning": ("Supervised learning course", "Train and compare two classifiers on a public dataset"),
    "Deep Learning": ("Neural-network fundamentals", "Build a small image or text classifier"),
    "Git": ("Git and GitHub workflow tutorial", "Publish one project with branches and a README"),
    "Linux": ("Linux command-line fundamentals", "Write a shell script to automate a repetitive task"),
    "Docker": ("Docker fundamentals", "Containerise a small Python application"),
    "Kubernetes": ("Container orchestration introduction", "Deploy a sample app locally with a manifest"),
    "Networking": ("TCP/IP and networking fundamentals", "Document a client-server request flow"),
    "Cybersecurity": ("Security fundamentals and safe lab practice", "Complete a legal beginner CTF exercise"),
    "HTML": ("HTML semantic markup lessons", "Build an accessible multi-section webpage"),
    "CSS": ("CSS layout and responsive design", "Create a responsive portfolio page"),
    "JavaScript": ("Modern JavaScript fundamentals", "Build an interactive form with validation"),
    "React": ("React component and state fundamentals", "Build a small task tracker"),
    "REST APIs": ("HTTP and REST API fundamentals", "Create and test a CRUD API"),
}
