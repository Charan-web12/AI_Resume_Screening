import os
from pathlib import Path
import docx
from docx.shared import Pt, Inches, RGBColor
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_resumes"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

CANDIDATES = [
    {
        "filename_base": "Rahul_Sharma_Senior_ML_Engineer",
        "name": "Rahul Sharma",
        "title": "Senior AI & Machine Learning Engineer",
        "email": "rahul.sharma@example.com",
        "phone": "+1 (555) 234-5678",
        "location": "San Francisco, CA",
        "education": "M.S. in Computer Science, Stanford University (2018)\nB.Tech in Computer Engineering, IIT Delhi (2016)",
        "summary": "Innovative Senior AI/ML Engineer with 6.5+ years of experience designing and deploying scalable deep learning pipelines, generative AI solutions, and NLP applications. Proven track record deploying models to AWS using Docker, FastAPI, and Kubernetes.",
        "experience": [
            {
                "role": "Senior Machine Learning Engineer",
                "company": "NeuralScale Inc.",
                "period": "2021 - Present (3+ years)",
                "bullets": [
                    "Architected NLP and LLM fine-tuning pipelines using PyTorch, Hugging Face, and Scikit-Learn for document comprehension.",
                    "Built asynchronous microservices with FastAPI and Docker, handling 15M+ daily inference queries on AWS.",
                    "Implemented CI/CD pipelines with GitHub Actions for automated model evaluation and container deployments.",
                    "Mentored team of 5 ML engineers in best practices for model tracking, Pandas, and NumPy optimization."
                ]
            },
            {
                "role": "Data Scientist & ML Developer",
                "company": "Cognitive Insights",
                "period": "2018 - 2021 (3 years)",
                "bullets": [
                    "Engineered predictive machine learning models using Scikit-Learn, XGBoost, and Python.",
                    "Automated ETL pipelines with SQL, PostgreSQL, and Pandas to clean terabyte-scale datasets.",
                    "Collaborated via Git with backend teams to integrate REST APIs for real-time risk scoring."
                ]
            }
        ],
        "skills": "Python, Machine Learning, Deep Learning, NLP, LLMs, Generative AI, PyTorch, Scikit-Learn, TensorFlow, Pandas, NumPy, FastAPI, Docker, Kubernetes, AWS, SQL, PostgreSQL, Git, CI/CD, REST APIs, Linux",
        "projects": "Enterprise RAG Assistant: Built retrieval-augmented generation search over 200k documents using PyTorch, LangChain, and FastAPI.\nAutomated Document Parser: Developed OCR and NLP classification model achieving 96% accuracy."
    },
    {
        "filename_base": "Priya_Patel_FullStack_Engineer",
        "name": "Priya Patel",
        "title": "Senior Full-Stack & Cloud Developer",
        "email": "priya.patel@example.com",
        "phone": "+1 (555) 345-6789",
        "location": "New York, NY",
        "education": "B.S. in Computer Science, UC Berkeley (2020)",
        "summary": "Results-oriented Full Stack Developer with 4.5+ years of experience building high-performance web applications using React, TypeScript, Node.js, and Python. Passionate about clean architecture, microservices, and database performance.",
        "experience": [
            {
                "role": "Lead Full Stack Developer",
                "company": "Apex Cloud Systems",
                "period": "2022 - Present (2.5 years)",
                "bullets": [
                    "Led development of modern React & TypeScript web platform with Tailwind CSS, improving page speed by 45%.",
                    "Built resilient backend microservices in Python (FastAPI) and Node.js (Express.js) backed by PostgreSQL and Redis.",
                    "Configured Docker containers and automated deployments via GitHub Actions and AWS ECS.",
                    "Authored comprehensive unit testing suites with Jest and PyTest ensuring 90%+ test coverage."
                ]
            },
            {
                "role": "Software Engineer",
                "company": "DataStream Solutions",
                "period": "2020 - 2022 (2 years)",
                "bullets": [
                    "Developed interactive dashboards using React, Redux, and REST APIs for enterprise analytics.",
                    "Designed relational database schemas and optimized complex SQL queries in PostgreSQL and MySQL.",
                    "Participated in Agile/Scrum sprints, daily standups, and code reviews using Git and Jira."
                ]
            }
        ],
        "skills": "React, TypeScript, JavaScript, Python, FastAPI, Node.js, Express.js, PostgreSQL, MongoDB, Redis, Docker, Git, REST APIs, Tailwind CSS, HTML5, CSS3, AWS, Unit Testing, Agile, Vite",
        "projects": "Collaborative Cloud Workspace: Built real-time canvas application using React, WebSockets, and Node.js.\nE-Commerce Microservices: Created order management service with Python FastAPI and PostgreSQL."
    },
    {
        "filename_base": "Amit_Verma_Backend_Developer",
        "name": "Amit Verma",
        "title": "Senior Backend Systems Engineer",
        "email": "amit.verma@example.com",
        "phone": "+1 (555) 456-7890",
        "location": "Austin, TX",
        "education": "B.Tech in Information Technology, NIT Trichy (2019)",
        "summary": "Dedicated Backend Engineer with 5.0 years of experience building enterprise-scale distributed systems, microservices, and database architectures. Strong expertise in Java, Spring Boot, Python, and SQL.",
        "experience": [
            {
                "role": "Senior Backend Engineer",
                "company": "Vortex Financial Tech",
                "period": "2021 - Present (3+ years)",
                "bullets": [
                    "Engineered transaction processing microservices using Java, Spring Boot, and Python with sub-50ms latency.",
                    "Implemented distributed caching with Redis and message queuing with RabbitMQ and Kafka.",
                    "Managed MySQL and PostgreSQL database migrations, indexing, and high-availability clustering.",
                    "Maintained containerized services using Docker and Linux server administration."
                ]
            },
            {
                "role": "Software Developer",
                "company": "InnoSoft Global",
                "period": "2019 - 2021 (2 years)",
                "bullets": [
                    "Developed RESTful APIs in Java and Python for enterprise resource planning software.",
                    "Wrote automated unit tests with JUnit and PyTest to prevent regression bugs.",
                    "Collaborated in Agile environment using Git, GitLab, and Jira."
                ]
            }
        ],
        "skills": "Java, Spring Boot, Python, MySQL, PostgreSQL, Redis, REST APIs, Microservices, Docker, Git, Linux, Unit Testing, Kafka, RabbitMQ, Agile, Object-Oriented Programming",
        "projects": "High-Throughput Payment Gateway: Processed $20M+ monthly transactions in Java Spring Boot and Redis.\nInventory Sync Daemon: Multi-threaded Python service syncing warehouse catalogs with MySQL."
    },
    {
        "filename_base": "Michael_Chang_DevOps_Cloud_Architect",
        "name": "Michael Chang",
        "title": "Lead DevOps & Cloud Infrastructure Engineer",
        "email": "michael.chang@example.com",
        "phone": "+1 (555) 567-8901",
        "location": "Seattle, WA",
        "education": "B.S. in Software Engineering, University of Washington (2017)",
        "summary": "Seasoned Cloud & DevOps Architect with 7.0 years of experience implementing Infrastructure as Code, CI/CD automation, and Kubernetes orchestration across enterprise AWS and multi-cloud environments.",
        "experience": [
            {
                "role": "Principal DevOps Engineer",
                "company": "CloudForge Systems",
                "period": "2020 - Present (4+ years)",
                "bullets": [
                    "Architected production Kubernetes (EKS) clusters hosting 200+ containerized microservices.",
                    "Authored automated Infrastructure as Code using Terraform and Ansible on AWS.",
                    "Constructed zero-downtime CI/CD deployment pipelines using GitHub Actions and Jenkins.",
                    "Set up monitoring, alerting, and observability stacks with Prometheus, Grafana, and Linux tooling."
                ]
            },
            {
                "role": "Systems & Cloud Administrator",
                "company": "Cascade Networks",
                "period": "2017 - 2020 (3 years)",
                "bullets": [
                    "Wrote Python and Bash automation scripts for server provisioning and security patching.",
                    "Administered Linux (Ubuntu/RHEL) systems, Nginx reverse proxies, and SSL certificates.",
                    "Managed AWS VPC, EC2, S3, IAM, and CloudWatch infrastructure."
                ]
            }
        ],
        "skills": "AWS, Kubernetes, Docker, Terraform, CI/CD, GitHub Actions, Jenkins, Linux, Python, Bash, Ansible, Prometheus, Grafana, Git, Nginx, Microservices, Agile",
        "projects": "Multi-Region Cloud Migration: Migrated 50+ on-prem services to AWS EKS with Terraform.\nGitOps Automation Pipeline: Implemented automated branch preview environments using Docker and Kubernetes."
    },
    {
        "filename_base": "Sneha_Rao_Junior_Frontend_Developer",
        "name": "Sneha Rao",
        "title": "Frontend UI/UX Developer",
        "email": "sneha.rao@example.com",
        "phone": "+1 (555) 678-9012",
        "location": "Chicago, IL",
        "education": "B.S. in Web Development & Digital Design, University of Texas (2023)",
        "summary": "Creative and enthusiastic Frontend Developer with 1.5 years of experience crafting intuitive, mobile-responsive web interfaces with React, JavaScript, HTML5, and modern CSS frameworks.",
        "experience": [
            {
                "role": "Junior Frontend Developer",
                "company": "PixelCraft Studios",
                "period": "2023 - Present (1.5 years)",
                "bullets": [
                    "Developed modern user interfaces using React, JavaScript (ES6+), and Tailwind CSS.",
                    "Converted Figma design mockups into pixel-perfect, accessible, and responsive web pages.",
                    "Integrated frontend components with backend REST APIs.",
                    "Maintained code repositories and branch workflows using Git and GitHub."
                ]
            }
        ],
        "skills": "React, JavaScript, HTML5, CSS3, Tailwind CSS, Responsive Design, Git, GitHub, Vite, Redux, Bootstrap",
        "projects": "Portfolio Showcase Platform: Responsive single-page application built with React and Vite.\nTask Management Board: Interactive drag-and-drop kanban board using React hooks and HTML5 drag APIs."
    }
]

def generate_docx(candidate, output_path):
    doc = docx.Document()
    
    # Page setup
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Name Header
    h1 = doc.add_heading(candidate["name"], level=0)
    h1.runs[0].font.size = Pt(20)
    h1.runs[0].font.color.rgb = RGBColor(30, 41, 59)
    
    # Subtitle / Contact
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run(f"{candidate['title']} | {candidate['email']} | {candidate['phone']} | {candidate['location']}")
    run_sub.font.size = Pt(10)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    # Professional Summary
    doc.add_heading("Professional Summary", level=1)
    p_sum = doc.add_paragraph(candidate["summary"])
    p_sum.paragraph_format.space_after = Pt(10)
    
    # Technical Skills
    doc.add_heading("Technical Skills", level=1)
    p_skills = doc.add_paragraph(candidate["skills"])
    p_skills.paragraph_format.space_after = Pt(10)
    
    # Professional Experience
    doc.add_heading("Work Experience", level=1)
    for exp in candidate["experience"]:
        p_role = doc.add_paragraph()
        run_role = p_role.add_run(f"{exp['role']} – {exp['company']}")
        run_role.bold = True
        run_period = p_role.add_run(f" ({exp['period']})")
        run_period.italic = True
        p_role.paragraph_format.space_after = Pt(4)
        
        for bullet in exp["bullets"]:
            p_b = doc.add_paragraph(bullet, style='List Bullet')
            p_b.paragraph_format.space_after = Pt(3)
        doc.add_paragraph()
        
    # Education
    doc.add_heading("Education", level=1)
    p_edu = doc.add_paragraph(candidate["education"])
    p_edu.paragraph_format.space_after = Pt(10)
    
    # Projects
    doc.add_heading("Key Projects", level=1)
    p_proj = doc.add_paragraph(candidate["projects"])
    p_proj.paragraph_format.space_after = Pt(10)
    
    doc.save(str(output_path))
    print(f"Generated DOCX: {output_path}")

def generate_pdf(candidate, output_path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'SectionHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563eb'),
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    story = []
    story.append(Paragraph(candidate["name"], title_style))
    contact_line = f"{candidate['title']} &bull; {candidate['email']} &bull; {candidate['phone']} &bull; {candidate['location']}"
    story.append(Paragraph(contact_line, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    
    # Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    story.append(Paragraph(candidate["summary"], body_style))
    story.append(Spacer(1, 4))
    
    # Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    story.append(Paragraph(candidate["skills"], body_style))
    story.append(Spacer(1, 4))
    
    # Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", heading_style))
    for exp in candidate["experience"]:
        role_line = f"<b>{exp['role']}</b> – {exp['company']} <i>({exp['period']})</i>"
        story.append(Paragraph(role_line, body_style))
        for bullet in exp["bullets"]:
            story.append(Paragraph(f"&bull; {bullet}", bullet_style))
        story.append(Spacer(1, 4))
        
    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    edu_text = candidate["education"].replace("\n", "<br/>")
    story.append(Paragraph(edu_text, body_style))
    story.append(Spacer(1, 4))
    
    # Projects
    story.append(Paragraph("KEY PROJECTS", heading_style))
    proj_text = candidate["projects"].replace("\n", "<br/>")
    story.append(Paragraph(proj_text, body_style))
    
    doc.build(story)
    print(f"Generated PDF: {output_path}")

def main():
    print("Generating sample resumes...")
    # First 3 candidates as PDF, next 2 as DOCX, and also provide all 5 in both formats
    for cand in CANDIDATES:
        pdf_path = SAMPLE_DIR / f"{cand['filename_base']}.pdf"
        docx_path = SAMPLE_DIR / f"{cand['filename_base']}.docx"
        
        generate_pdf(cand, pdf_path)
        generate_docx(cand, docx_path)
        
    print("All sample resumes generated successfully!")

if __name__ == "__main__":
    main()
