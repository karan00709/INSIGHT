
import streamlit as st
import sqlite3
import json
import io
import html
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak
)

# =========================================================
# INSIGHT 1.0
# Educational self-reflection and personal development app
# =========================================================

st.set_page_config(
    page_title="INSIGHT | Self Development",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PREMIUM DARK DESIGN ----------------

NAVY = "#101C2B"
TEAL = "#62D6C5"
LIGHT = "#E8EEF7"
MUTED = "#9AABC0"
PANEL = "#17283B"
BORDER = "#2A4058"

st.markdown("""
<style>
:root {
    color-scheme: dark;
    --bg: #0B1421;
    --panel: #142337;
    --panel-2: #1A2D43;
    --border: #2A4058;
    --text: #E8EEF7;
    --muted: #9AABC0;
    --accent: #62D6C5;
}
.stApp, [data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 12% 0%, #182D43 0%, #0B1421 48%, #0B1421 100%);
    color: var(--text);
}
[data-testid="stHeader"] { background: rgba(11,20,33,.88); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14263A 0%, #101C2B 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text); }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: .48rem .65rem; border-radius: 10px; margin: 2px 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: #20364D; }
h1, h2, h3, h4, p, label, .stMarkdown, [data-testid="stCaptionContainer"] {
    color: var(--text);
}
h1 { letter-spacing: -.035em; font-weight: 750; }
h2, h3 { letter-spacing: -.02em; }
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1A3047, #142337);
    border: 1px solid var(--border); border-radius: 16px;
    padding: 18px 20px; box-shadow: 0 10px 28px rgba(0,0,0,.16);
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-weight: 750; }
.hero {
    background: linear-gradient(115deg, #17334A 0%, #1B4A5A 58%, #17665F 100%);
    border: 1px solid rgba(126,220,207,.2); padding: 30px 34px;
    border-radius: 22px; color: white; margin: 6px 0 28px;
    box-shadow: 0 18px 50px rgba(0,0,0,.22); position: relative; overflow: hidden;
}
.hero:after { content: ""; position: absolute; width: 220px; height: 220px; right: -55px; top: -100px; border-radius: 50%; background: rgba(255,255,255,.06); }
.hero h1 { color: #FFFFFF !important; font-size: clamp(36px, 5vw, 52px); margin: 0 0 8px; }
.hero p { color: #D3E4EC !important; font-size: 16px; margin: 5px 0; }
.eyebrow { color: #80DCCD; font-size: 11px; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; margin-bottom: 10px; }
.section-intro { color: var(--muted); font-size: 15px; margin-top: -8px; margin-bottom: 20px; }
.insight-card {
    background: linear-gradient(145deg, #192D43, #132337);
    border: 1px solid var(--border); border-radius: 17px;
    padding: 20px 21px; min-height: 150px;
    box-shadow: 0 10px 26px rgba(0,0,0,.13); margin-bottom: 12px;
}
.insight-card h3 { color: #F4F8FC; margin: 4px 0 8px; font-size: 19px; }
.insight-card p { color: #AFC0D2; font-size: 14px; margin: 0; }
.card-kicker { color: #72D8C8; text-transform: uppercase; font-size: 10px; font-weight: 800; letter-spacing: .13em; }
div.stButton > button, div.stDownloadButton > button, button[kind="primary"] {
    border-radius: 11px; min-height: 43px; font-weight: 650;
    border: 1px solid #3A5872; background: #1B344B; color: #EDF6FC;
    transition: all .16s ease;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    border-color: var(--accent); color: #FFFFFF; background: #24465A;
}
div.stButton > button[kind="primary"], button[kind="primary"] {
    background: linear-gradient(100deg, #2C9F96, #47BFAE); color: #071B22;
    border: 0; font-weight: 800;
}
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input, [data-baseweb="select"] > div {
    background: #102033 !important; color: #E8EEF7 !important;
    border-color: #38516B !important; border-radius: 10px !important;
}
[data-testid="stRadio"] label, [data-testid="stCheckbox"] label { color: #DCE6F1 !important; }
/* Premium dark expanders */
[data-testid="stExpander"] {
    background: #142337 !important;
    border: 1px solid #38516B !important;
    border-radius: 13px !important;
    overflow: hidden;
}

[data-testid="stExpander"] details,
[data-testid="stExpander"] details summary {
    background: #1B3047 !important;
    color: #F1F5F9 !important;
}

[data-testid="stExpander"] details summary:hover {
    background: #243E57 !important;
}

[data-testid="stExpander"] details summary p,
[data-testid="stExpander"] details summary span {
    color: #F1F5F9 !important;
}

[data-testid="stExpander"] details summary svg {
    fill: #72D8C8 !important;
    color: #72D8C8 !important;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #142337 !important;
    color: #DCE6F1 !important;
}
/* Dark notification and validation messages */
[data-testid="stAlert"],
[data-testid="stAlert"] > div,
div[role="alert"] {
    background-color: #1B2D42 !important;
    border: 1px solid #45617D !important;
    border-radius: 12px !important;
    color: #F1F5F9 !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] label,
div[role="alert"] p {
    color: #F1F5F9 !important;
}

[data-testid="stAlert"] svg {
    fill: #72D8C8 !important;
    color: #72D8C8 !important;
}
[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #36A99D, #7AE0CF); }
hr { border-color: #2A4058 !important; }
[data-testid="stDataFrame"] { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
.small-muted { color: var(--muted); font-size: 13px; }
.question-panel { background: #142337; border: 1px solid #2A4058; padding: 24px; border-radius: 18px; margin: 12px 0 18px; }
.result-panel { background: linear-gradient(145deg, #17384A, #142337); border: 1px solid #326174; border-radius: 18px; padding: 22px; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ---------------- DATABASE ----------------

DB_PATH = Path(__file__).parent / "insight_history.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            assessment_type TEXT NOT NULL,
            summary TEXT NOT NULL
        )
    """)
    connection.commit()
    return connection


def save_history(assessment_type, summary):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO history (created_at, assessment_type, summary)
        VALUES (?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            assessment_type,
            json.dumps(summary)
        )
    )
    connection.commit()
    connection.close()


def load_history():
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT id, created_at, assessment_type, summary
        FROM history
        ORDER BY id DESC
        """
    ).fetchall()
    connection.close()

    records = []
    for row in rows:
        records.append({
            "id": row[0],
            "date": row[1],
            "type": row[2],
            "summary": json.loads(row[3])
        })
    return records


# ---------------- PERSONALITY QUESTIONNAIRE ----------------
# Mini-IPIP, Donnellan et al. (2006)
# 11 reverse-scored items

personality_questions = [
    ("I am the life of the party.", "Extraversion", False),
    ("I sympathize with others' feelings.", "Agreeableness", False),
    ("I get chores done right away.", "Conscientiousness", False),
    ("I have frequent mood swings.", "Neuroticism", False),
    ("I have a vivid imagination.", "Openness", False),

    ("I don't talk a lot.", "Extraversion", True),
    ("I am not interested in other people's problems.", "Agreeableness", True),
    ("I often forget to put things back in their proper place.", "Conscientiousness", True),
    ("I am relaxed most of the time.", "Neuroticism", True),
    ("I am not interested in abstract ideas.", "Openness", True),

    ("I talk to a lot of different people at parties.", "Extraversion", False),
    ("I feel others' emotions.", "Agreeableness", False),
    ("I like order.", "Conscientiousness", False),
    ("I get upset easily.", "Neuroticism", False),
    ("I have difficulty understanding abstract ideas.", "Openness", True),

    ("I keep in the background.", "Extraversion", True),
    ("I am not really interested in others.", "Agreeableness", True),
    ("I make a mess of things.", "Conscientiousness", True),
    ("I seldom feel blue.", "Neuroticism", True),
    ("I do not have a good imagination.", "Openness", True)
]

personality_options = {
    "Very inaccurate": 1,
    "Moderately inaccurate": 2,
    "Neither inaccurate nor accurate": 3,
    "Moderately accurate": 4,
    "Very accurate": 5
}

personality_info = {
    "Extraversion": {
        "meaning": "Social engagement, talkativeness and energy in social situations.",
        "high_strength": "You may feel comfortable initiating conversations, participating in groups and seeking social engagement.",
        "low_strength": "You may prefer focused interaction, independent work and time to think before speaking.",
        "challenge": "A higher score can sometimes mean taking on too many social commitments. A lower score may make it harder to speak up in some group settings.",
        "study": "Consider whether collaborative study, discussions or independent study suit your energy and concentration patterns.",
        "relationships": "Notice how you balance social activity, conversation and personal space."
    },
    "Agreeableness": {
        "meaning": "Consideration for others, sympathy and interpersonal interest.",
        "high_strength": "You may be attentive to other people's feelings and motivated to cooperate.",
        "low_strength": "You may be more comfortable challenging ideas, questioning assumptions and prioritising directness.",
        "challenge": "A higher score can sometimes make boundary-setting difficult. A lower score can sometimes make cooperation or tact more demanding.",
        "study": "You may benefit from balancing teamwork with independent critical thinking.",
        "relationships": "Consider how empathy, honesty and boundaries work together in your interactions."
    },
    "Conscientiousness": {
        "meaning": "Organisation, order, reliability and completing tasks.",
        "high_strength": "You may find it easier to organise tasks, follow plans and maintain routines.",
        "low_strength": "You may be more flexible and comfortable adapting when plans change.",
        "challenge": "A higher score can sometimes lead to perfectionism. A lower score may make deadlines and consistent routines harder to maintain.",
        "study": "Experiment with realistic schedules, task breakdowns and review routines.",
        "relationships": "Consider how reliability, planning and flexibility affect shared responsibilities."
    },
    "Neuroticism": {
        "meaning": "Tendency to experience negative emotional states and emotional sensitivity.",
        "high_strength": "Greater sensitivity may help you notice emotional changes and stressful situations early.",
        "low_strength": "You may report fewer frequent negative emotional reactions in everyday situations.",
        "challenge": "A higher score may be associated with stronger or more frequent distress. A lower score does not mean you never experience difficult emotions.",
        "study": "Notice whether stress affects concentration and experiment with breaks, preparation and healthy coping strategies.",
        "relationships": "Pay attention to how you communicate when upset and what helps you regulate emotional reactions."
    },
    "Openness": {
        "meaning": "Imagination, interest in abstract ideas and intellectual curiosity.",
        "high_strength": "You may enjoy exploring ideas, experimenting and considering unfamiliar perspectives.",
        "low_strength": "You may prefer practical examples, familiar methods and concrete information.",
        "challenge": "A higher score may sometimes lead to too many competing interests. A lower score may make unfamiliar approaches less appealing.",
        "study": "Try combining conceptual exploration with practical examples and structured learning.",
        "relationships": "Consider how curiosity and openness to different perspectives influence conversations."
    }
}


def score_personality(answers):
    dimensions = {name: [] for name in personality_info}

    for index, (_, dimension, reverse) in enumerate(personality_questions):
        value = answers[index]
        if reverse:
            value = 6 - value
        dimensions[dimension].append(value)

    return {
        name: round(sum(values) / len(values), 2)
        for name, values in dimensions.items()
    }


def level_label(score):
    if score < 2.5:
        return "Relatively lower on this dimension"
    if score < 3.6:
        return "Around the middle of this scale"
    return "Relatively higher on this dimension"


# ---------------- GET BETTER SCENARIOS ----------------

scenarios = [
    {
        "title": "Public embarrassment",
        "situation": "A friend makes fun of you in front of several people. Everyone laughs, and you feel embarrassed.",
        "options": [
            ("A", "Insult them back immediately.", 1,
             "This may express anger, but it can escalate the conflict and shift attention away from the original behaviour."),
            ("B", "Laugh along, even though the comment hurt you.", 2,
             "This may help you avoid immediate confrontation, but your friend may not realise that the comment hurt you."),
            ("C", "Calmly tell them that the comment bothered you.", 4,
             "This communicates a boundary directly while reducing the chance of unnecessary escalation."),
            ("D", "Discuss it privately later.", 3,
             "A private conversation can protect your dignity and allow a calmer discussion. It may not address the immediate public moment.")
        ],
        "principle": "Assertive communication and emotional regulation",
        "alternative": "You could say: 'I know you may have meant it as a joke, but I didn't find that funny. Please don't do that again.'",
        "exercise": "Practise stating one boundary in a calm, specific sentence without insulting the other person."
    },
    {
        "title": "Receiving criticism",
        "situation": "A teacher or colleague criticises your work in front of others. You believe part of the criticism is unfair.",
        "options": [
            ("A", "Argue immediately and defend every decision.", 1,
             "You may communicate disagreement, but reacting immediately can make it harder to understand the feedback."),
            ("B", "Ignore the feedback completely.", 1,
             "You avoid an uncomfortable exchange, but may miss useful information or leave a misunderstanding unresolved."),
            ("C", "Listen, identify useful points and ask for clarification.", 4,
             "This allows you to evaluate the feedback without automatically accepting every claim."),
            ("D", "Accept everything without questioning it.", 2,
             "This may reduce conflict, but it does not help you distinguish fair criticism from inaccurate feedback.")
        ],
        "principle": "Growth mindset and constructive communication",
        "alternative": "Ask for a specific example, then explain respectfully where you see the situation differently.",
        "exercise": "Take one piece of feedback and separate it into: what is useful, what needs clarification and what you disagree with."
    },
    {
        "title": "Repeatedly cancelled plans",
        "situation": "A close friend repeatedly cancels plans at the last minute. You feel that your time is not being respected.",
        "options": [
            ("A", "Stop speaking to them without explaining why.", 1,
             "Distance may protect your time, but the other person may not understand the reason."),
            ("B", "Keep accepting cancellations without saying anything.", 1,
             "This avoids immediate disagreement but may allow frustration to build."),
            ("C", "Explain how the repeated cancellations affect you.", 4,
             "Direct communication gives your friend an opportunity to understand the impact and change their behaviour."),
            ("D", "Cancel their plans next time to teach them a lesson.", 1,
             "Retaliation may create more resentment without resolving the underlying issue.")
        ],
        "principle": "Boundary-setting and direct communication",
        "alternative": "Explain the pattern and agree on a practical arrangement, such as confirming plans in advance.",
        "exercise": "Write a boundary that describes the behaviour, its impact and what you will do next time."
    },
    {
        "title": "Someone takes credit",
        "situation": "A group member presents work you contributed to as if they completed it alone.",
        "options": [
            ("A", "Publicly accuse them of stealing your work.", 2,
             "You address the issue, but an accusation without a clear explanation can escalate the disagreement."),
            ("B", "Remain silent and hope someone notices.", 1,
             "This avoids confrontation but may leave your contribution unrecognised."),
            ("C", "Calmly clarify your contribution using specific evidence.", 4,
             "Factual clarification helps protect your contribution without relying on personal attacks."),
            ("D", "Take credit for their work in return.", 1,
             "Retaliation creates another unfair situation and weakens trust.")
        ],
        "principle": "Assertiveness and professional conflict resolution",
        "alternative": "State which parts you completed and refer to drafts, messages or agreed responsibilities.",
        "exercise": "Practise describing your contribution using facts rather than accusations."
    },
    {
        "title": "Supporting a friend",
        "situation": "A friend tells you about a personal problem. You are unsure what advice to give.",
        "options": [
            ("A", "Immediately tell them what they should do.", 2,
             "Advice can be useful, but giving it before understanding the problem may make the friend feel unheard."),
            ("B", "Change the subject because the conversation is uncomfortable.", 1,
             "This may avoid discomfort but can leave the friend feeling unsupported."),
            ("C", "Listen carefully and ask what kind of support they need.", 4,
             "This gives the friend room to explain their needs before you offer help."),
            ("D", "Compare their problem with your own experiences.", 2,
             "Sharing experience can build connection, but it can also shift attention away from the person seeking support.")
        ],
        "principle": "Active listening and empathy",
        "alternative": "Ask: 'Would you like advice, practical help, or would you prefer that I just listen?'",
        "exercise": "In your next conversation, summarise what the other person said before offering your opinion."
    },
    {
        "title": "Jealousy and comparison",
        "situation": "A classmate achieves something you have been working towards. You feel jealous and disappointed.",
        "options": [
            ("A", "Minimise their achievement.", 1,
             "This may temporarily protect your self-image, but it does not help you understand your own feelings."),
            ("B", "Compare yourself with them repeatedly.", 1,
             "Repeated comparison can increase frustration without giving you a useful plan."),
            ("C", "Recognise your feelings and identify what you can learn.", 4,
             "This acknowledges the emotion while directing attention towards constructive action."),
            ("D", "Give up because they are ahead of you.", 1,
             "Another person's progress does not establish what you can achieve.")
        ],
        "principle": "Emotional awareness and constructive self-reflection",
        "alternative": "Recognise the feeling, congratulate them if appropriate, and identify one action that supports your own goal.",
        "exercise": "Write down one thing you admire about their progress and one realistic action you can take."
    },
    {
        "title": "Taking responsibility",
        "situation": "You make a mistake that creates extra work for another person. Nobody has realised yet that you caused it.",
        "options": [
            ("A", "Hide the mistake and hope nobody discovers it.", 1,
             "This may delay discomfort but can increase the consequences if the problem continues."),
            ("B", "Blame someone else.", 1,
             "This avoids responsibility and may damage trust."),
            ("C", "Acknowledge the mistake and help correct it.", 4,
             "Taking responsibility early can help limit harm and rebuild confidence."),
            ("D", "Wait until someone directly confronts you.", 2,
             "Waiting may allow the problem to grow and delay a solution.")
        ],
        "principle": "Accountability and problem-solving",
        "alternative": "Explain what happened, apologise where appropriate and suggest a concrete correction.",
        "exercise": "Practise a short accountability statement: what happened, your responsibility and your next corrective action."
    },
    {
        "title": "Too many commitments",
        "situation": "Several deadlines are approaching. A friend asks you to take on another responsibility.",
        "options": [
            ("A", "Agree even though you know you cannot manage it.", 1,
             "This may please the friend immediately but can create missed commitments later."),
            ("B", "Respond angrily because you feel overwhelmed.", 1,
             "Your frustration may be understandable, but anger may make the conversation less productive."),
            ("C", "Explain your commitments and set a boundary.", 4,
             "Honesty about your capacity helps you protect existing responsibilities."),
            ("D", "Ignore the request completely.", 2,
             "This avoids a difficult conversation but leaves the other person without a clear answer.")
        ],
        "principle": "Assertiveness and prioritisation",
        "alternative": "Decline respectfully or suggest a realistic time when you may be available.",
        "exercise": "List your commitments, identify your priorities and practise saying no to one non-essential request."
    }
]


def reflection_feedback(text):
    text = text.strip()
    if len(text) < 15:
        return (
            "Your explanation is quite brief. Try adding what you were "
            "feeling, what outcome you wanted and how you considered "
            "the other person's perspective."
        )

    lower = text.lower()
    indicators = {
        "emotion awareness": ["feel", "angry", "upset", "nervous", "jealous", "embarrass", "frustrat"],
        "communication": ["explain", "tell", "ask", "talk", "discuss", "communicat"],
        "boundary-setting": ["boundary", "limit", "no ", "respect", "time"],
        "perspective-taking": ["understand", "perspective", "their side", "listen", "empathy"],
        "problem-solving": ["solution", "solve", "fix", "next step", "plan", "evidence"]
    }

    detected = [
        label for label, words in indicators.items()
        if any(word in lower for word in words)
    ]

    if detected:
        return (
            "Your explanation mentions: " + ", ".join(detected) +
            ". These are useful reflection themes. Consider whether your "
            "response also accounts for possible consequences and "
            "the other person's perspective."
        )

    return (
        "You have explained your reasoning. To deepen your reflection, "
        "consider the emotion involved, the outcome you want and the "
        "possible effect on the other person."
    )


# ---------------- WEAK AREAS: 24 QUESTIONS ----------------

skill_questions = {
    "Emotional regulation": [
        "I can pause before reacting when I feel angry.",
        "I can identify what emotion I am experiencing.",
        "I can use a healthy strategy to manage stress."
    ],
    "Empathy": [
        "I try to understand how another person might feel.",
        "I listen without immediately judging someone's experience.",
        "I consider perspectives different from my own."
    ],
    "Communication": [
        "I express my thoughts clearly.",
        "I ask questions when I do not understand something.",
        "I listen carefully instead of preparing my reply while someone speaks."
    ],
    "Conflict resolution": [
        "I can discuss disagreements without personal attacks.",
        "I try to understand the actual cause of a disagreement.",
        "I look for solutions that address the problem fairly."
    ],
    "Self-awareness": [
        "I can identify my personal strengths and limitations.",
        "I recognise situations that trigger strong reactions in me.",
        "I reflect on my behaviour and its effects on others."
    ],
    "Decision-making": [
        "I consider the consequences before making important decisions.",
        "I compare relevant information before choosing.",
        "I can make a decision without endlessly delaying it."
    ],
    "Assertiveness": [
        "I can express disagreement respectfully.",
        "I can say no when a request exceeds my capacity.",
        "I can communicate my needs without being aggressive."
    ],
    "Resilience": [
        "I can return to a task after experiencing a setback.",
        "I look for lessons after an unsuccessful attempt.",
        "I can continue working towards a goal when progress is slow."
    ]
}

skill_exercises = {
    "Emotional regulation": "Use a pause-and-name exercise: stop, identify the emotion, rate its intensity and choose your next action.",
    "Empathy": "In one conversation, summarise the other person's point of view before sharing your own.",
    "Communication": "Practise explaining one idea in three parts: main point, reason and example.",
    "Conflict resolution": "Write down the issue, each person's needs and one fair solution.",
    "Self-awareness": "At the end of the day, record one reaction, its trigger and what you might do differently.",
    "Decision-making": "Use a decision table listing options, benefits, costs and likely consequences.",
    "Assertiveness": "Practise an 'I' statement: 'I feel..., when..., and I would prefer...'.",
    "Resilience": "Break one difficult goal into a small action that can be completed within 20 minutes."
}


def calculate_skill_scores(answers):
    scores = {}
    for skill, items in skill_questions.items():
        values = [answers[f"{skill}_{i}"] for i in range(3)]
        mean = sum(values) / 3
        scores[skill] = round(1 + ((mean - 1) / 4) * 9, 1)
    return scores


# ---------------- SESSION STATE ----------------

defaults = {
    "page": "Dashboard",
    "personality_answers": {},
    "personality_index": 0,
    "personality_result": None,
    "scenario_index": 0,
    "scenario_answers": {},
    "scenario_text": {},
    "scenario_results": None,
    "skill_answers": {},
    "skill_index": 0,
    "skill_result": None,
    "latest_report": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- PDF REPORT ----------------

def create_pdf(title, sections):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="MainTitle",
        parent=styles["Title"],
        textColor=colors.HexColor(NAVY),
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        textColor=colors.HexColor(TEAL),
        spaceBefore=12,
        spaceAfter=7
    ))
    styles.add(ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        leading=15,
        spaceAfter=7
    ))

    story = [
        Paragraph(html.escape(title), styles["MainTitle"]),
        Paragraph(
            "INSIGHT | Understand Yourself. Improve Yourself.",
            styles["BodyCustom"]
        ),
        Paragraph(
            "Generated: " + datetime.now().strftime("%d %B %Y, %H:%M"),
            styles["BodyCustom"]
        ),
        Spacer(1, 12)
    ]

    for heading, lines in sections:
        story.append(Paragraph(html.escape(heading), styles["SectionTitle"]))
        for line in lines:
            safe_line = html.escape(str(line)).replace("\n", "<br/>")
            story.append(Paragraph(safe_line, styles["BodyCustom"]))

    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Important: INSIGHT is an educational self-reflection tool. "
        "Its scores are not clinical diagnoses, medical advice or "
        "validated measures of overall ability. Interpret results "
        "in context.",
        styles["BodyCustom"]
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def report_download_button(label, sections, filename, key):
    pdf = create_pdf("INSIGHT Report", sections)
    st.download_button(
        label=label,
        data=pdf,
        file_name=filename,
        mime="application/pdf",
        key=key
    )


# ---------------- SHARED HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">YOUR PERSONAL DEVELOPMENT SPACE</div>
    <h1>INSIGHT</h1>
    <p><strong>Understand yourself. Become better.</strong></p>
    <p>Build self-awareness through reflection, deliberate practice and measurable growth.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("# 🧠 INSIGHT")
st.sidebar.caption("YOUR PERSONAL DEVELOPMENT SPACE")

pages = [
    "Dashboard",
    "Know Your Personality",
    "Get Better",
    "Know Your Weak Areas",
    "My Progress",
    "Psychology Library",
    "About & Privacy"
]

page = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page)
    if st.session_state.page in pages else 0
)
st.session_state.page = page

st.sidebar.divider()
st.sidebar.caption("INSIGHT 1.0 | Educational project")
st.sidebar.caption("Not a diagnostic or medical tool.")


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown('<div class="eyebrow">YOUR OVERVIEW</div>', unsafe_allow_html=True)
    st.title("Welcome back.")
    st.markdown('<div class="section-intro">A structured space to understand your patterns, strengthen everyday responses and track your development.</div>', unsafe_allow_html=True)

    history = load_history()

    personality_done = any(
        item["type"] == "Personality" for item in history
    )
    scenario_done = any(
        item["type"] == "Get Better" for item in history
    )
    skills_done = any(
        item["type"] == "Weak Areas" for item in history
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Assessments completed", len(history))
    with c2:
        st.metric("Modules explored", sum([
            personality_done, scenario_done, skills_done
        ]))
    with c3:
        st.metric("Skill domains", 8)

    st.divider()
    st.subheader("Your development modules")

    columns = st.columns(3)

    module_data = [
        ("🧠 Know Your Personality",
         "Explore five broad personality dimensions.",
         "Know Your Personality", personality_done),
        ("🎯 Get Better",
         "Practise responses to realistic social situations.",
         "Get Better", scenario_done),
        ("📊 Know Your Weak Areas",
         "Reflect on eight practical development domains.",
         "Know Your Weak Areas", skills_done)
    ]

    for column, item in zip(columns, module_data):
        title, description, destination, completed = item
        with column:
            st.markdown(
                f'<div class="insight-card"><div class="card-kicker">{"COMPLETED" if completed else "START HERE"}</div><h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True
            )
            st.caption("✓ Completed before" if completed else "Not completed yet")
            if st.button(
                "Open module",
                key=f"dashboard_{destination}",
                use_container_width=True
            ):
                st.session_state.page = destination
                st.rerun()

    st.divider()
    st.subheader("A note about self-development")

    st.write(
        "INSIGHT is designed to encourage reflection, not to label "
        "people. Your results are snapshots of your responses and "
        "may change with experience, circumstances and time."
    )


# =========================================================
# PERSONALITY
# =========================================================

elif page == "Know Your Personality":

    st.markdown('<div class="eyebrow">SELF-DISCOVERY · 20 QUESTIONS</div>', unsafe_allow_html=True)
    st.title("Know Your Personality")

    st.write(
        "Explore five broad dimensions of personality through "
        "the 20-item Mini-IPIP questionnaire."
    )

    st.info(
        "Answer based on how you generally behave, not how you "
        "wish to behave. There are no right or wrong answers."
    )

    if st.session_state.personality_result is None:

        index = st.session_state.personality_index
        question, dimension, reverse = personality_questions[index]

        st.progress((index + 1) / 20)
        st.caption(f"QUESTION {index + 1:02d} / 20  ·  {dimension.upper()}")
        st.markdown('<div class="question-panel">', unsafe_allow_html=True)
        st.subheader(question)
        st.markdown('</div>', unsafe_allow_html=True)

        old_value = st.session_state.personality_answers.get(index)
        labels = list(personality_options.keys())
        old_label = next(
            (label for label, value in personality_options.items()
             if value == old_value),
            None
        )

        selected = st.radio(
            "How accurately does this describe you?",
            labels,
            index=labels.index(old_label) if old_label else None,
            key=f"personality_radio_{index}"
        )

        left, right = st.columns(2)

        with left:
            if index > 0 and st.button(
                "← Previous", key=f"personality_prev_{index}"
            ):
                if selected:
                    st.session_state.personality_answers[index] = personality_options[selected]
                st.session_state.personality_index -= 1
                st.rerun()

        with right:
            label = "Calculate my results" if index == 19 else "Next →"

            if st.button(
                label,
                type="primary",
                key=f"personality_next_{index}"
            ):
                if selected is None:
                    st.warning("Please select an answer.")
                else:
                    st.session_state.personality_answers[index] = personality_options[selected]

                    if index < 19:
                        st.session_state.personality_index += 1
                    else:
                        scores = score_personality(
                            st.session_state.personality_answers
                        )
                        st.session_state.personality_result = scores
                        save_history("Personality", scores)
                        st.session_state.latest_report = {
                            "type": "Personality",
                            "scores": scores
                        }
                    st.rerun()

        if st.button(
            "Restart assessment",
            key="restart_personality"
        ):
            st.session_state.personality_answers = {}
            st.session_state.personality_index = 0
            st.session_state.personality_result = None
            st.rerun()

    else:
        scores = st.session_state.personality_result

        st.success("Your personality profile is ready.")

        df = pd.DataFrame({
            "Dimension": list(scores.keys()),
            "Score": list(scores.values())
        })

        fig = px.bar(
            df,
            x="Dimension",
            y="Score",
            range_y=[0, 5],
            text="Score",
            color_discrete_sequence=[TEAL]
        )
        fig.update_layout(
            plot_bgcolor="#142337",
            paper_bgcolor="#142337",
            font=dict(color="#E8EEF7"),
            xaxis=dict(gridcolor="#2A4058"),
            yaxis=dict(gridcolor="#2A4058"),
            yaxis_title="Average score (1–5)",
            xaxis_title=""
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Your detailed profile")

        for dimension, score in scores.items():
            info = personality_info[dimension]

            with st.expander(
                f"{dimension} — {score}/5 | {level_label(score)}",
                expanded=True
            ):
                st.write("**What this dimension reflects**")
                st.write(info["meaning"])

                if score >= 3.6:
                    st.write("**Possible strengths**")
                    st.write(info["high_strength"])
                elif score < 2.5:
                    st.write("**Possible strengths**")
                    st.write(info["low_strength"])
                else:
                    st.write("**Possible pattern**")
                    st.write(
                        "Your responses fall around the middle of this "
                        "scale. Your behaviour may depend strongly on context."
                    )

                st.write("**Possible challenges to reflect on**")
                st.write(info["challenge"])

                st.write("**Study implications to consider**")
                st.write(info["study"])

                st.write("**Relationship implications to consider**")
                st.write(info["relationships"])

        st.warning(
            "These are possible patterns, not predictions. A four-item "
            "dimension score cannot explain your entire personality, "
            "relationship behaviour or academic potential."
        )

        sections = [
            ("Personality scores", [
                f"{name}: {score}/5 — {level_label(score)}"
                for name, score in scores.items()
            ])
        ]

        for dimension, score in scores.items():
            info = personality_info[dimension]
            sections.append((dimension, [
                info["meaning"],
                "Possible strength: " + (
                    info["high_strength"] if score >= 3.6
                    else info["low_strength"] if score < 2.5
                    else "Your responses are around the middle of this scale."
                ),
                "Possible challenge: " + info["challenge"],
                "Study reflection: " + info["study"],
                "Relationship reflection: " + info["relationships"]
            ]))

        report_download_button(
            "Download personality report (PDF)",
            sections,
            "INSIGHT_Personality_Report.pdf",
            "personality_pdf"
        )

        if st.button(
            "Take assessment again",
            key="retake_personality"
        ):
            st.session_state.personality_answers = {}
            st.session_state.personality_index = 0
            st.session_state.personality_result = None
            st.rerun()


# =========================================================
# GET BETTER
# =========================================================

elif page == "Get Better":

    st.markdown('<div class="eyebrow">PRACTICE LAB · 8 SCENARIOS</div>', unsafe_allow_html=True)
    st.title("Get Better")

    st.write(
        "Practise handling everyday challenges. Choose a response, "
        "explain your reasoning and reflect on the feedback."
    )

    st.info(
        "This is a learning exercise. There is rarely one perfect "
        "response in real life; context, safety and individual needs matter."
    )

    if st.session_state.scenario_results is None:

        index = st.session_state.scenario_index
        scenario = scenarios[index]

        st.progress((index + 1) / len(scenarios))
        st.caption(f"SCENARIO {index + 1:02d} / {len(scenarios)}")

        st.markdown(
            f'<div class="question-panel"><div class="card-kicker">THE SITUATION</div><h2>{html.escape(scenario["title"])}</h2><p>{html.escape(scenario["situation"])}</p></div>',
            unsafe_allow_html=True
        )
        st.markdown("**Choose the response closest to what you would do.**")

        option_labels = [
            f"{key}. {text}"
            for key, text, score, explanation in scenario["options"]
        ]

        previous = st.session_state.scenario_answers.get(index)

        chosen = st.radio(
            "Choose the response closest to what you would do:",
            option_labels,
            index=option_labels.index(previous) if previous in option_labels else None,
            key=f"scenario_choice_{index}"
        )

        written = st.text_area(
            "Explain why you would respond this way:",
            value=st.session_state.scenario_text.get(index, ""),
            placeholder="Describe your reasoning, feelings and intended outcome...",
            key=f"scenario_text_{index}",
            height=120
        )

        col1, col2 = st.columns(2)

        with col1:
            if index > 0 and st.button(
                "← Previous",
                key=f"scenario_prev_{index}"
            ):
                if chosen:
                    st.session_state.scenario_answers[index] = chosen
                st.session_state.scenario_text[index] = written
                st.session_state.scenario_index -= 1
                st.rerun()

        with col2:
            button_text = "Finish scenarios" if index == 7 else "Next scenario →"

            if st.button(
                button_text,
                type="primary",
                key=f"scenario_next_{index}"
            ):
                if not chosen:
                    st.warning("Please choose a response.")
                elif len(written.strip()) < 10:
                    st.markdown("""
<div style="
    background: #332817;
    border: 1px solid #A87935;
    border-left: 4px solid #E5A943;
    border-radius: 10px;
    padding: 13px 16px;
    color: #FFE2A8;
    font-size: 14px;
    margin-top: 10px;
">
    Please explain your reasoning in at least a few words.
</div>
""", unsafe_allow_html=True)
                else:
                    st.session_state.scenario_answers[index] = chosen
                    st.session_state.scenario_text[index] = written

                    if index < 7:
                        st.session_state.scenario_index += 1
                    else:
                        results = []
                        total = 0

                        for i, item in enumerate(scenarios):
                            answer = st.session_state.scenario_answers[i]
                            selected_key = answer.split(".")[0]

                            selected_option = next(
                                option for option in item["options"]
                                if option[0] == selected_key
                            )

                            score = selected_option[2]
                            total += score

                            results.append({
                                "title": item["title"],
                                "choice": answer,
                                "score": score,
                                "explanation": selected_option[3],
                                "reflection": reflection_feedback(
                                    st.session_state.scenario_text[i]
                                ),
                                "text": st.session_state.scenario_text[i],
                                "principle": item["principle"],
                                "alternative": item["alternative"],
                                "exercise": item["exercise"]
                            })

                        average = round(total / len(scenarios), 2)

                        st.session_state.scenario_results = {
                            "average": average,
                            "details": results
                        }

                        save_history("Get Better", {
                            "average": average,
                            "completed": len(results)
                        })

                    st.rerun()

        st.caption(
            "Your written reflections are used to generate feedback "
            "in this session but are not saved in assessment history."
        )

    else:
        result = st.session_state.scenario_results

        st.success("You completed all eight scenarios.")

        st.metric(
            "Average response-alignment score",
            f"{result['average']} / 4"
        )

        st.caption(
            "This score reflects alignment with the educational rubric "
            "used in this exercise. It is not an objective measure of "
            "social intelligence or character."
        )

        for item in result["details"]:
            with st.expander(item["title"], expanded=False):
                st.write("**Your selected response**")
                st.write(item["choice"])

                st.write("**Rubric score**")
                st.write(f"{item['score']} / 4")

                st.write("**Possible consequences**")
                st.write(item["explanation"])

                st.write("**Your written reflection**")
                st.write(item["text"])

                st.write("**Reflection feedback**")
                st.write(item["reflection"])

                st.write("**Learning principle**")
                st.write(item["principle"])

                st.write("**Alternative approach**")
                st.write(item["alternative"])

                st.write("**Practice exercise**")
                st.write(item["exercise"])

        sections = [
            ("Overall result", [
                f"Average rubric score: {result['average']} / 4",
                "This is an educational alignment score, not an objective measure of social intelligence."
            ])
        ]

        for item in result["details"]:
            sections.append((item["title"], [
                "Selected response: " + item["choice"],
                f"Rubric score: {item['score']}/4",
                "Possible consequences: " + item["explanation"],
                "Reflection feedback: " + item["reflection"],
                "Learning principle: " + item["principle"],
                "Alternative approach: " + item["alternative"],
                "Practice exercise: " + item["exercise"]
            ]))

        report_download_button(
            "Download Get Better report (PDF)",
            sections,
            "INSIGHT_Get_Better_Report.pdf",
            "scenario_pdf"
        )

        if st.button(
            "Practise again",
            key="restart_scenarios"
        ):
            st.session_state.scenario_index = 0
            st.session_state.scenario_answers = {}
            st.session_state.scenario_text = {}
            st.session_state.scenario_results = None
            st.rerun()


# =========================================================
# WEAK AREAS
# =========================================================

elif page == "Know Your Weak Areas":

    st.markdown('<div class="eyebrow">SKILL REFLECTION · 24 QUESTIONS</div>', unsafe_allow_html=True)
    st.title("Know Your Weak Areas")
    st.markdown('<div class="section-intro">Identify the behaviours you already practise and the areas where deliberate practice may help.</div>', unsafe_allow_html=True)
    st.info(
        "Think about your behaviour over approximately the last 30 days. "
        "These are self-reflection scores, not objective ability tests."
    )

    if st.session_state.skill_result is None:
        flat_questions = [
            (skill, i, statement)
            for skill, items in skill_questions.items()
            for i, statement in enumerate(items)
        ]
        index = st.session_state.skill_index
        skill, item_index, statement = flat_questions[index]
        st.progress((index + 1) / len(flat_questions))
        st.caption(f"QUESTION {index + 1:02d} / {len(flat_questions)}  ·  {skill.upper()}")
        st.markdown(
            f'<div class="question-panel"><div class="card-kicker">{html.escape(skill)}</div><h3>{html.escape(statement)}</h3><p>How often has this been true for you in the last 30 days?</p></div>',
            unsafe_allow_html=True
        )
        scale = {
            1: "Almost never",
            2: "Rarely",
            3: "Sometimes",
            4: "Often",
            5: "Almost always"
        }
        prior = st.session_state.skill_answers.get(f"{skill}_{item_index}")
        selected = st.radio(
            "Choose one response",
            options=list(scale.keys()),
            format_func=lambda value: f"{value}  ·  {scale[value]}",
            index=list(scale.keys()).index(prior) if prior in scale else None,
            horizontal=True,
            key=f"skill_step_{index}"
        )
        left, right = st.columns(2)
        with left:
            if index > 0 and st.button("← Previous", key=f"skill_prev_{index}", use_container_width=True):
                if selected is not None:
                    st.session_state.skill_answers[f"{skill}_{item_index}"] = selected
                st.session_state.skill_index -= 1
                st.rerun()
        with right:
            next_label = "Calculate my skill profile" if index == len(flat_questions) - 1 else "Continue →"
            if st.button(next_label, type="primary", key=f"skill_next_{index}", use_container_width=True):
                if selected is None:
                    st.warning("Please select a response before continuing.")
                else:
                    st.session_state.skill_answers[f"{skill}_{item_index}"] = selected
                    if index < len(flat_questions) - 1:
                        st.session_state.skill_index += 1
                    else:
                        scores = calculate_skill_scores(st.session_state.skill_answers)
                        st.session_state.skill_result = scores
                        save_history("Weak Areas", scores)
                    st.rerun()
        st.caption("Scale: 1 = Almost never · 2 = Rarely · 3 = Sometimes · 4 = Often · 5 = Almost always")

    else:
        scores = st.session_state.skill_result
        st.markdown('<div class="result-panel"><div class="card-kicker">YOUR REFLECTION PROFILE</div><h2>Patterns to build on.</h2><p>Your scores show how frequently you reported practising each behaviour. They are a starting point for reflection, not a judgement of your ability.</p></div>', unsafe_allow_html=True)
        df = pd.DataFrame({
            "Skill": list(scores.keys()),
            "Score": list(scores.values())
        }).sort_values("Score")
        fig = px.bar(
            df, x="Score", y="Skill", orientation="h", range_x=[0, 10],
            text="Score", color_discrete_sequence=[TEAL]
        )
        fig.update_layout(
            plot_bgcolor="#142337", paper_bgcolor="#142337",
            font=dict(color="#E8EEF7"),
            xaxis=dict(gridcolor="#2A4058", title="Reflection score (1–10)"),
            yaxis=dict(gridcolor="#2A4058", title=""),
            margin=dict(l=10, r=20, t=20, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("Your development priorities")
        lowest = sorted(scores.items(), key=lambda x: x[1])[:3]
        cols = st.columns(3)
        for col, (skill, score) in zip(cols, lowest):
            with col:
                st.markdown(
                    f'<div class="insight-card"><div class="card-kicker">PRIORITY · {score}/10</div><h3>{html.escape(skill)}</h3><p>{html.escape(skill_exercises[skill])}</p></div>',
                    unsafe_allow_html=True
                )
        st.subheader("All skill domains")
        for skill, score in scores.items():
            c1, c2 = st.columns([4, 1])
            c1.write(f"**{skill}**")
            c2.markdown(f"<div style='text-align:right;color:#72D8C8;font-weight:700'>{score}/10</div>", unsafe_allow_html=True)
            st.progress(score / 10)
        st.warning(
            "A lower score means you reported practising the behaviour less frequently. "
            "It does not prove that you lack the skill. Context and opportunity also influence responses."
        )
        sections = [
            ("Skill scores", [f"{skill}: {score}/10" for skill, score in scores.items()]),
            ("Suggested development priorities", [f"{skill}: {skill_exercises[skill]}" for skill, score in lowest])
        ]
        report_download_button(
            "Download skill report (PDF)", sections,
            "INSIGHT_Skill_Report.pdf", "skills_pdf"
        )
        if st.button("Retake skill assessment", key="retake_skills"):
            st.session_state.skill_result = None
            st.session_state.skill_answers = {}
            st.session_state.skill_index = 0
            st.rerun()


# =========================================================
# PROGRESS
# =========================================================

elif page == "My Progress":

    st.markdown('<div class="eyebrow">YOUR DEVELOPMENT HISTORY</div>', unsafe_allow_html=True)
    st.title("My Progress")

    history = load_history()

    if not history:
        st.info(
            "Your progress will appear here after you complete "
            "your first assessment."
        )
    else:
        st.metric("Saved assessment records", len(history))

        rows = []

        for item in history:
            summary = item["summary"]

            if item["type"] == "Personality":
                description = "Five personality dimension scores"
            elif item["type"] == "Get Better":
                description = (
                    f"Average rubric score: {summary.get('average', 0)}/4"
                )
            else:
                description = "Eight skill-domain scores"

            rows.append({
                "Date": item["date"],
                "Assessment": item["type"],
                "Summary": description
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Assessment history")

        for item in history:
            with st.expander(
                f"{item['date']} — {item['type']}"
            ):
                st.json(item["summary"])

        st.caption(
            "History is stored in the local SQLite database in this "
            "Codespaces workspace. It is not synchronised to GitHub."
        )


# =========================================================
# PSYCHOLOGY LIBRARY
# =========================================================

elif page == "Psychology Library":

    st.markdown('<div class="eyebrow">LEARN THE FOUNDATIONS</div>', unsafe_allow_html=True)
    st.title("Psychology Library")

    st.write(
        "Explore the concepts that inform INSIGHT's educational "
        "activities and self-reflection exercises."
    )

    library = {
        "The Big Five personality model": (
            "The Big Five model describes personality using five broad "
            "dimensions: Extraversion, Agreeableness, Conscientiousness, "
            "Neuroticism and Openness. These dimensions describe patterns "
            "rather than fixed categories. People are not simply one type "
            "or another."
        ),
        "Emotional regulation": (
            "Emotional regulation refers to processes through which "
            "people influence which emotions they experience, when they "
            "experience them and how they express them. It does not mean "
            "suppressing every difficult emotion."
        ),
        "Empathy": (
            "Empathy involves understanding or responding to another "
            "person's emotional experience. Perspective-taking and "
            "emotional responsiveness are related but distinct processes."
        ),
        "Active listening": (
            "Active listening involves giving attention, checking "
            "understanding, asking relevant questions and reflecting "
            "what another person has communicated."
        ),
        "Assertive communication": (
            "Assertiveness involves communicating needs, opinions and "
            "boundaries clearly while respecting other people. It differs "
            "from both aggression and passive avoidance."
        ),
        "Cognitive reframing": (
            "Cognitive reframing involves examining an interpretation "
            "of a situation and considering alternative explanations. "
            "It does not require pretending that a genuinely harmful "
            "situation is harmless."
        ),
        "Self-compassion": (
            "Self-compassion involves responding to personal difficulty "
            "with understanding rather than excessive self-criticism. "
            "It can coexist with accountability and efforts to improve."
        ),
        "Growth mindset": (
            "A growth mindset emphasises the possibility of developing "
            "abilities through learning, strategies and practice. It "
            "does not mean that effort alone guarantees success."
        ),
        "Decision-making": (
            "Decision-making involves identifying options, evaluating "
            "relevant information, considering consequences and choosing "
            "an action. Good decisions depend on context and available evidence."
        ),
        "Resilience": (
            "Resilience describes processes of adapting or recovering "
            "when facing difficulty. It is influenced by personal, social "
            "and environmental resources."
        )
    }

    for title, explanation in library.items():
        with st.expander(title):
            st.write(explanation)

    st.divider()
    st.subheader("Research references")

    st.markdown("""
    1. Donnellan, M. B., Oswald, F. L., Baird, B. M., & Lucas, R. E.
       (2006). *The Mini-IPIP Scales: Tiny-yet-effective measures of the
       Big Five factors of personality.* Psychological Assessment, 18(2),
       192–203. DOI: 10.1037/1040-3590.18.2.192.

    2. Gross, J. J. (1998). *The emerging field of emotion regulation:
       An integrative review.* Review of General Psychology, 2(3), 271–299.

    3. Beck, J. S. (2020). *Cognitive Behavior Therapy: Basics and Beyond.*
       Third edition.

    4. Neff, K. D. (2023). *Self-Compassion: Theory, Method, Research,
       and Intervention.* Annual Review of Psychology.

    5. Greenberger, D., & Padesky, C. A. (2015).
       *Mind Over Mood.* Second edition.
    """)


# =========================================================
# ABOUT & PRIVACY
# =========================================================

elif page == "About & Privacy":

    st.markdown('<div class="eyebrow">PROJECT & DATA</div>', unsafe_allow_html=True)
    st.title("About INSIGHT")

    st.write("""
    INSIGHT is an educational self-reflection and personal development
    project designed to help users explore personality, practise
    communication and reflect on practical skills.

    It is not a medical service, psychological diagnostic tool or
    substitute for professional assessment.
    """)

    st.subheader("How your data is handled")

    st.write("""
    - Assessment summaries are stored in a local SQLite database.
    - Written scenario reflections are not saved in assessment history.
    - The database is excluded from Git through `.gitignore`.
    - The app does not require an account or collect an email address.
    - Anyone with access to the Codespaces workspace may be able to
      access its local database files.
    """)

    st.warning(
        "This version is designed for individual use in your Codespaces "
        "workspace. Do not deploy it as a public multi-user app with "
        "shared SQLite history. A public deployment needs user "
        "authentication and separate data isolation."
    )

    st.subheader("Important limitations")

    st.write("""
    - Personality results are based on self-report.
    - Skill scores are informal self-reflection scores.
    - Scenario feedback uses a simple educational rubric.
    - Written reflection feedback uses basic keyword-based prompts,
      not artificial intelligence or clinical interpretation.
    - INSIGHT has not undergone independent psychometric validation.
    - Results should not be used for hiring, diagnosis, selection or
      other high-stakes decisions.
    """)

    st.subheader("Project information")
    st.write("INSIGHT 1.0")
    st.write("Built with Python and Streamlit.")
    st.write("Designed as an educational student project.")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "INSIGHT 1.0 | Understand Yourself. Become Better. "
    "| Educational self-reflection only — not medical advice."
)
