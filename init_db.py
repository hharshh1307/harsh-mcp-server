"""
Initialize SQLite database with Harsh Agarwal's resume data
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "resume.db")

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
    -- Personal Info
    CREATE TABLE IF NOT EXISTS personal_info (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        location TEXT,
        current_company TEXT,
        current_role TEXT,
        bio TEXT
    );

    -- Education
    CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY,
        institution TEXT,
        degree TEXT,
        field TEXT,
        gpa REAL,
        start_date TEXT,
        end_date TEXT,
        location TEXT
    );

    -- Courses
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT
    );

    -- Skills
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        proficiency INTEGER
    );

    -- Work Experience
    CREATE TABLE IF NOT EXISTS work_experience (
        id INTEGER PRIMARY KEY,
        company TEXT,
        role TEXT,
        location TEXT,
        start_date TEXT,
        end_date TEXT,
        is_current INTEGER
    );

    -- Projects
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        work_experience_id INTEGER,
        name TEXT,
        description TEXT,
        impact TEXT,
        technologies TEXT,
        FOREIGN KEY (work_experience_id) REFERENCES work_experience(id)
    );

    -- Achievements
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        year TEXT
    );
    """)

    # Insert Personal Info
    cursor.execute("""
    INSERT OR REPLACE INTO personal_info (id, name, email, phone, location, current_company, current_role, bio)
    VALUES (1, 'Harsh Agarwal', 'harshh1307@gmail.com', '+91-7414890202', 'Bengaluru, India', 'Newme', 'Data Scientist',
    'Data Scientist with 2.5+ years of experience building ML systems at scale. IIT Delhi graduate passionate about recommendation systems, deep learning, and solving real-world problems with data.')
    """)

    # Insert Education
    cursor.execute("""
    INSERT OR REPLACE INTO education (id, institution, degree, field, gpa, start_date, end_date, location)
    VALUES (1, 'Indian Institute of Technology Delhi', 'Bachelor of Technology', 'Electrical Engineering', 8.326, 'Jul 2018', 'Jun 2022', 'Delhi, India')
    """)

    # Insert Courses
    courses = [
        ('Machine Intelligence and Learning', 'ML/AI'),
        ('Data Structures And Algorithms', 'CS Fundamentals'),
        ('Probability and Stochastic Processes', 'Mathematics'),
        ('Digital Electronics', 'Electronics'),
        ('Digital Signal Processing', 'Signal Processing'),
        ('Communication Engineering', 'Electronics')
    ]
    cursor.executemany("INSERT INTO courses (name, category) VALUES (?, ?)", courses)

    # Insert Skills
    skills = [
        ('Python', 'Languages', 95),
        ('C++', 'Languages', 75),
        ('MySQL', 'Languages', 85),
        ('GoLang', 'Languages', 70),
        ('VS Code', 'Tools', 90),
        ('Docker', 'Tools', 80),
        ('Airflow', 'Tools', 75),
        ('GIT', 'Tools', 90),
        ('Scikit-learn', 'ML/Deep Learning', 90),
        ('PyTorch', 'ML/Deep Learning', 85),
        ('TensorFlow', 'ML/Deep Learning', 80),
        ('Hugging Face', 'ML/Deep Learning', 85),
        ('SBERT', 'ML/Deep Learning', 85),
        ('CLIP / FashionCLIP', 'ML/Deep Learning', 80),
        ('FAISS', 'ML/Deep Learning', 85),
        ('XGBoost', 'ML/Deep Learning', 90),
        ('LambdaMART', 'ML/Deep Learning', 90)
    ]
    cursor.executemany("INSERT INTO skills (name, category, proficiency) VALUES (?, ?, ?)", skills)

    # Insert Work Experience
    work_experiences = [
        (1, 'Newme', 'Data Scientist', 'Bengaluru, India', 'Sep 2024', 'Present', 1),
        (2, 'Zomato', 'Data Scientist', 'Gurugram, India', 'Jun 2022', 'Aug 2024', 0),
        (3, 'Axis Bank', 'Intern - DBAT Team', 'Remote', 'May 2021', 'Jul 2021', 0)
    ]
    cursor.executemany("""
    INSERT OR REPLACE INTO work_experience (id, company, role, location, start_date, end_date, is_current)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, work_experiences)

    # Insert Projects
    projects = [
        # Newme projects
        (1, 'Shop Page Recommendation System',
         'Implemented a LambdaMART-based ranking system using LambdaRank optimization and NDCG evaluation to personalize apparel recommendations for 200K daily active app users',
         '+7% lift in conversion rate',
         'LambdaMART, LambdaRank, NDCG, Python'),
        (1, 'Similar Products Module',
         'Engineered a Similar Products module on the PDP by combining deep product-image embeddings with key product features',
         '50% boost in click-through rate, comparable uplift in conversions',
         'Deep Embeddings, FashionCLIP, FAISS'),
        (1, 'Order Return Risk (RTO)',
         'Built a checkout-time RTO risk prediction model to identify high-risk COD orders and mitigate fraud',
         'Currently in experimentation phase',
         'XGBoost, Risk Modeling'),

        # Zomato projects
        (2, 'Restaurant Recommendation Model',
         'Engineered a real-time, learn-to-rank model for Zomato dining homepage, optimizing recommendations for 7L+ daily app users. Integrated cuisine preferences, ambiance, popularity, customer affordability, and geographic proximity',
         '3.4% increase in customer interaction, 1.3% uplift in ad-revenue',
         'Learn-to-Rank, Real-time ML, Python'),
        (2, 'Customer Churn Prediction',
         'Developed a predictive tree-based XGBoost model to forecast customer churn with approximately 70% precision',
         'Reduced churn rate by 1.2%',
         'XGBoost, Classification'),
        (2, 'New User Promo Segmentation',
         'Created a tree-based model to analyze new users first-order features for personalized promo distribution',
         'Enhanced first-order retention by 2.3%',
         'Decision Trees, Segmentation'),
        (2, 'User Community Detection',
         'Implemented the Leiden algorithm to cluster platform users into communities based on address links to identify high-value customers early',
         'Reduced acquisition costs by 4%, increased conversions by 0.8%',
         'Leiden Algorithm, Graph Clustering'),

        # Axis Bank projects
        (3, 'VCIP Automation',
         'Automated the Video-Based Customer Identification Protocol (VCIP) recon file for co-origination journeys',
         '40% reduction in workflow time',
         'Python, Automation')
    ]
    cursor.executemany("""
    INSERT INTO projects (work_experience_id, name, description, impact, technologies)
    VALUES (?, ?, ?, ?, ?)
    """, projects)

    # Insert Achievements
    achievements = [
        ('JEE Advanced 2018', 'All India Rank 304 among 155K candidates (99.79 percentile)', '2018'),
        ('KVPY Fellowship 2018', 'AIR 973 - Kishore Vaigyanik Protsahan Yojna by DST, Govt. of India', '2018'),
        ('IITD Semester Merit', 'Scholarship for being among top 7% students in Sem I 2018-19', '2018'),
        ('Inter Hostel Ad Making 2020', 'Awarded first position unanimously by judges, out of 13 teams', '2020'),
        ('Inter-Hostel Football', 'First Runners-up in Inter-Hostel Games', '2019')
    ]
    cursor.executemany("""
    INSERT INTO achievements (title, description, year)
    VALUES (?, ?, ?)
    """, achievements)

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_database()
