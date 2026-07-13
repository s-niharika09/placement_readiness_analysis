# 🎯 AI Placement Readiness Analyzer

### *Helping students understand how close they are to their dream job.*

---

## 🌟 Overview

Have you ever uploaded your resume to a job portal and wondered...

🤔 **"Will this resume get shortlisted?"**

🤔 **"Which skills am I missing?"**

🤔 **"Am I actually ready for this role?"**

This project was built to answer those questions.

The **AI Placement Readiness Analyzer** is an intelligent application that compares a student's resume with a real job description and provides personalized feedback, just like an experienced recruiter.

Instead of simply saying *"Selected"* or *"Rejected"*, it explains:

✅ What you're already good at

❌ Which skills you're missing

📈 How ready you are for the role

🛠️ What you should learn next

📅 A personalized roadmap to improve your chances

---

# 🚀 What makes this project special?

Unlike a traditional resume checker, this application combines **Artificial Intelligence**, **Machine Learning**, and **Natural Language Processing (NLP)** to evaluate a candidate from multiple perspectives.

It doesn't just count keywords—it actually understands both the resume and the job description before making recommendations.

---

# 🧠 How does it work?

Imagine a recruiter reviewing your resume.

They would typically:

📄 Read your resume

💼 Read the job description

🔍 Compare both

📊 Judge your readiness

💡 Suggest improvements

This project follows exactly the same process—but automatically.

---

## Step 1️⃣ Upload Your Resume

The user uploads a PDF resume.

📄 Example:

```
Resume.pdf
```

The application extracts all the text from the document.

---

## Step 2️⃣ Paste the Job Description

Next, the user pastes the job description of the role they want.

For example:

* Data Scientist
* AI Engineer
* Python Developer
* Software Engineer
* Data Analyst

---

## Step 3️⃣ AI Understands Your Resume 🤖

Instead of simply searching for keywords, the AI carefully reads the resume and extracts meaningful information.

It identifies:

🛠️ Technical Skills

💼 Projects

🎓 Education

🏆 Certifications

💻 Tools & Technologies

👨‍💼 Internship Experience

📂 Resume Category

It also evaluates the overall quality of the resume.

---

## Step 4️⃣ AI Understands the Job Description 💼

The application then analyzes the job description to understand what the company is actually looking for.

It extracts:

✅ Required Skills

🔥 Critical Skills

✨ Nice-to-Have Skills

🧰 Tools & Frameworks

📋 Responsibilities

🧠 Soft Skills

---

## Step 5️⃣ Resume vs Job Comparison ⚔️

Now comes the interesting part.

The application compares both documents.

It finds:

✅ Skills you already have

❌ Skills you're missing

🚨 Critical skills you should learn first

⭐ Optional skills that would strengthen your profile

---

## Step 6️⃣ Feature Engineering 📊

All of this information is converted into numerical values.

Examples include:

📈 Skill Match Percentage

🎯 Critical Skill Match

📉 Missing Skills Count

📄 Resume Completeness

🏆 Project Relevance

🎓 Certification Score

💼 Internship Score

🔑 Keyword Match

These values become the input for the Machine Learning model.

---

## Step 7️⃣ Machine Learning Prediction 🤖

A trained Machine Learning model predicts how prepared the candidate is.

The model classifies the candidate into one of four categories:

🔴 Not Ready Yet

🟠 Needs Improvement

🟡 Moderately Ready

🟢 Highly Ready

It also calculates:

📊 Placement Readiness Score

🎯 Prediction Confidence

📈 Probability of each category

---

## Step 8️⃣ Personalized AI Career Mentor 💡

Finally, another AI model acts like a career mentor.

Instead of giving generic advice, it creates personalized recommendations such as:

📝 Resume Improvement Suggestions

📅 7-Day Learning Plan

📆 30-Day Learning Roadmap

🎯 Job-Specific Preparation Tips

📚 Technologies to Learn

🎤 Interview Preparation Advice

---

# 🏗️ Project Workflow

```text
📄 Resume PDF
        │
        ▼
📝 Resume Parser
        │
        ▼
🤖 Resume Analyzer
        │
        ├──────────────┐
        ▼              ▼
💼 JD Analyzer     ⚔️ Skill Gap Analyzer
        │              │
        └──────┬───────┘
               ▼
        📊 Feature Builder
               ▼
      🤖 Machine Learning Model
               ▼
      💡 AI Feedback Generator
               ▼
      🌐 Streamlit Dashboard
```

---

# ✨ Features

✅ Resume Parsing

✅ Resume Understanding using AI

✅ Job Description Understanding

✅ Skill Gap Detection

✅ Machine Learning Prediction

✅ Placement Readiness Score

✅ AI Career Recommendations

✅ Interactive Dashboard

✅ JSON Report Download

✅ PDF Report Download

---

# 🛠️ Tech Stack

### 👨‍💻 Programming

🐍 Python

---

### 🧠 Artificial Intelligence

🤖 Groq API

🧾 Prompt Engineering

🧠 Large Language Models (LLMs)

---

### 📊 Machine Learning

📈 Scikit-learn

💾 Joblib

---

### 📚 NLP

Natural Language Processing

Structured JSON Extraction

Semantic Skill Matching

---

### 🌐 Web Application

🎨 Streamlit

---

### 📄 Resume Parsing

📑 pdfplumber

---

### 📑 Report Generation

📄 ReportLab

---

### 🗂️ Version Control

Git

GitHub

---

# 📂 Project Structure

```text
placement_readiness_analyser/

📁 analyzers/
📁 models/
📁 prompts/
📄 app.py
📄 requirements.txt
📄 README.md
📄 .gitignore
```

# 🎯 Why I Built This Project

As a Data Science learner, I wanted to build something that solves a real problem faced by students during placements.

Many students don't know:

* Why their resume gets rejected.
* Which skills they should learn next.
* Whether they are ready for a specific role.

This project aims to bridge that gap by combining AI and Machine Learning into a practical career guidance tool that provides clear, personalized feedback.

---

# 🔮 Future Improvements

✨ ATS Compatibility Score

🌍 Multi-language Resume Support

☁️ Cloud Deployment (AWS/Azure/GCP)

👥 Multi-candidate Resume Comparison

📊 Recruiter Dashboard

📈 Resume Progress Tracking

🔐 User Authentication

---

# 👩‍💻 About the Author

## Sakiley Niharika

🎓 B.Tech in Electronics & Communication Engineering

🤖 Passionate about Artificial Intelligence, Machine Learning, Data Science, and building practical AI applications.
