# 🧠 INSIGHT
### Understand Yourself. Improve Yourself.

**INSIGHT** is an interactive personal development and self-reflection application built with Python and Streamlit. It helps users explore their personality, practise everyday social situations, identify areas for improvement, and track their personal development over time.

The project was developed as a final project for **Stanford Code in Place**.

---

## 🎯 Project Purpose

Self-awareness and interpersonal skills play an important role in personal, academic and professional development. However, people do not always have structured ways to reflect on their behaviour and practise better responses to everyday situations.

INSIGHT aims to provide a structured environment for this process through personality exploration, scenario-based learning, self-assessment and progress tracking.

The goal is not to label people, but to encourage reflection, learning and continuous improvement.

## ✨ Features

### 1. Know Your Personality
- A 20-item personality questionnaire based on the Mini-IPIP.
- Explores the Big Five personality dimensions:
  - Extraversion
  - Agreeableness
  - Conscientiousness
  - Neuroticism
  - Openness
- Calculates dimension scores.
- Provides educational interpretations, possible strengths, challenges and reflections related to studying and relationships.
- Generates a downloadable PDF report.

### 2. Get Better
- Eight realistic social and interpersonal scenarios.
- Multiple-choice response options.
- Written reflection exercises.
- Feedback explaining possible consequences of different responses.
- Learning principles, alternative approaches and practical exercises.
- An educational response-alignment scoring system.
- Downloadable PDF report.

### 3. Know Your Weak Areas
- A 24-question self-reflection assessment.
- Evaluates eight practical development domains:
  - Emotional regulation
  - Empathy
  - Communication
  - Conflict resolution
  - Self-awareness
  - Decision-making
  - Assertiveness
  - Resilience
- Calculates domain-wise reflection scores.
- Identifies three development priorities.
- Recommends practical exercises.

### 4. My Progress
- Stores assessment summaries in an SQLite database.
- Displays previous assessment records.
- Helps users review their development over time.

### 5. Psychology Library
Provides educational explanations of concepts including:
- The Big Five personality model
- Emotional regulation
- Empathy
- Active listening
- Assertive communication
- Cognitive reframing
- Self-compassion
- Growth mindset
- Decision-making
- Resilience

### 6. PDF Reports
Users can generate downloadable reports containing assessment results, interpretations and development recommendations.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Pandas | Data handling |
| Plotly | Data visualisation |
| SQLite | Persistent assessment history |
| ReportLab | PDF report generation |
| Git and GitHub | Version control and project hosting |

---

## 🚀 Getting Started

### Prerequisites
- Python installed
- Git (optional, for cloning the repository)

### Installation

Clone the repository:

```bash
git clone https://github.com/karan00709/INSIGHT.git
```

Navigate to the project directory:

```bash
cd INSIGHT
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

## 📁 Project Structure

```text
INSIGHT/
│
├── streamlit_app.py       # Main application
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Excluded files
└── insight_history.db     # Local assessment history (generated at runtime)
```

---

## 🔒 Privacy and Data Handling

- Assessment summaries are stored in a local SQLite database.
- Written scenario reflections are not saved in assessment history.
- The database is excluded from Git using `.gitignore`.
- The application does not require users to create an account.
- The current version is designed for individual use in a Codespaces workspace.

**Important:** This version does not implement user authentication or separate databases for multiple users. It should not be deployed as a public multi-user application with shared assessment history.

---

## ⚠️ Limitations

INSIGHT is an educational self-reflection application, not a clinical or psychological diagnostic tool.

- Personality results are based on self-reported answers.
- Skill scores represent reported behaviour frequency, not objectively measured ability.
- Scenario scores reflect an educational response-alignment rubric.
- Written reflection feedback uses basic keyword-based analysis, not an AI model.
- The application has not undergone independent psychometric validation.
- Results should not be used for diagnosis, hiring, selection or other high-stakes decisions.

---

## 📚 Research References

1. Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E. (2006). *The Mini-IPIP Scales: Tiny-yet-effective measures of the Big Five factors of personality.* Psychological Assessment, 18(2), 192–203.

2. Gross, J. J. (1998). *The emerging field of emotion regulation: An integrative review.* Review of General Psychology, 2(3), 271–299.

3. Beck, J. S. (2020). *Cognitive Behavior Therapy: Basics and Beyond.*

4. Neff, K. D. (2023). *Self-Compassion: Theory, Method, Research, and Intervention.*

---

## 🎓 Project Information

**Project:** INSIGHT – Personal Development and Self-Reflection Platform  
**Course:** Stanford Code in Place  
**Language:** Python  
**Framework:** Streamlit  
**Repository:** https://github.com/karan00709/INSIGHT

Built to explore how programming can be used to create practical tools for self-awareness, reflection and personal growth.

---

*Understand Yourself. Improve Yourself.*
