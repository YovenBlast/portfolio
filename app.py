"""
Single-file Flask portfolio app for Maheswaren CHINNASAMY.
- Uses Bootstrap 5 via CDN
- Includes animations and simple interactivity (AOS, lightbox)
- Data is prefilled from available user context; missing items are marked TODO

How to run:
1. Install dependencies: pip install Flask
2. python portfolio_app.py
3. Open http://127.0.0.1:5000

You can edit the DATA dict to fill missing info (photo paths, links, email, project repo/demo links).
"""
from flask import Flask, render_template_string, send_file, request, redirect, url_for
import io

app = Flask(__name__)

# ---------------------------
# Replace or fill TODO fields below
# ---------------------------
DATA = {
    "name": "Maheswaren CHINNASAMY",
    "title": "Software Developer — Aspiring Software Tester",
    "location": "Mauritius",
    "summary": (
        "I'm Maheswaren, a software developer and aspiring software test engineer. "
        "I work with AI, IoT, mobile development (Flutter), and automation. "
        "I love building practical projects that solve real problems."
    ),
    # TODO: Update profile_image to the path of your profile photo in static/ or an external URL
    "profile_image": "/static/images/image.png",
    # Contact info - TODO: fill in your email, linkedin, github links
    "email": "ychinnasamy48@gmail.com",
    "linkedin": "https://www.linkedin.com/in/maheswaren-chinnasamy-2a5a5a296/",
    "github": "https://github.com/YovenBlast",
    # Quick skills
    "skills": {
        "languages": ["Python", "Java", "Dart (Flutter)", "JavaScript"],
        "frameworks": ["Flask", "Flutter", "React (basic)", "Node.js"],
        "tools": ["Git", "Firebase", "Postman", "Selenium", "JUnit"],
    },
    "experience": [
        {
            "role": "Software Tester Intern",
            "company": "SD Worx Mauritius",
            "date": "March 2024",
            "details": "Worked on real-world testing tasks; learned teamwork, workflows, and testing tools.",
            "technologies": ["C#", "Playwright", "Agile Methodologies"],
            "position": "",
            "tasks": []
        },
        {
            "role": "Working at CIM",
            "company": "CIM Finance Services Ltd",
            "date": "Present",
            "details": "I work in software testing and development, doing forms, AI integration, and automations.",
            "technologies": ["C#", "WSO2", "CSS", "Python"],
            "position": "Analyst Programmer",
            "tasks": [
                "Design and Implementation of forms",
                "Automation of ESB system",
                "Providing innovative solutions",
                "Files transfer"
            ]
        }
    ],
    "education": [
        {"degree": "BSc (Hons) Software Engineering", "school": "University of Technology, Mauritius", "date": "Expected Feb 2025"}
    ],
    "certifications": [
        {
            "name": "WSO2 API Manager Practitioner Certification - V4",
            "issuer": "WSO2",
            "date": "September 2025",
            "credential_url": "https://certification.wso2.com/certificate/CID-05134719"
        },
        {
            "name": "Rise In",
            "issuer": "Rise In",
            "date": "November - December 2024",
            "credential_url": "https://www.risein.com/courses/transactions-and-bitcoin"
        }
    ],
    "projects": [
        {
            "id": "smart_compost",
            "name": "Smart Composting Bin",
            "summary": "IoT smart compost bin using ESP8266, multiple sensors (temp, moisture, pH, gas) and Firebase real-time DB.",
            "stack": ["ESP8266", "MQ4/MQ8", "Firebase", "Python (data processing)"],
            "contribution": "Designed sensor system, integrated Firebase streaming and dashboard, defined composting phases.",
            "image": "/static/projects/compostBin.png",
            "repo": "https://github.com/TODO/smart-composting-bin",
            "demo": "",
            "video_url": "",  # TODO: Add GitHub video URL
            "images_url": "https://github.com/YovenBlast/Smart_Composting_Bin_Images"  # TODO: Add GitHub images folder URL
        },
        {
            "id": "smart_parking",
            "name": "IoT-Based Smart Parking System",
            "summary": "Ultrasonic sensors detect car presence in zones; data sent via ESP8266 to a cloud DB.",
            "stack": ["ESP8266", "Ultrasonic sensors", "Firebase"],
            "contribution": "Sensor interfacing, zone logic, cloud push and simple web dashboard.",
            "image": "/static/projects/parking.webp",
            "repo": "https://github.com/YovenBlast/Smart-Parking-System",
            "demo": "",
            "video_url": "https://vimeo.com/1154608349?fl=ip&fe=ec",  # TODO: Add GitHub video URL
            "images_url": "https://github.com/YovenBlast/Images/blob/main/PK1.webp"  # TODO: Add GitHub images folder URL
        },
        {
            "id": "hotel_app",
            "name": "Hotel Booking App (Flutter)",
            "summary": "A Flutter hotel booking app with booking history and room management features.",
            "stack": ["Flutter", "Dart", "Firebase"],
            "contribution": "Built UI, booking logic, and integrated database helpers for images and room numbers.",
            "image": "/static/projects/HotelBooking.png",
            "repo": "https://github.com/YovenBlast/Hotel_Booking_System",
            "demo": "",
            "video_url": "",  # TODO: Add GitHub video URL
            "images_url": "https://github.com/YovenBlast/Hotel_Booking_System_Images"  # TODO: Add GitHub images folder URL
        },
        {
            "id": "trash_tamer",
            "name": "Trash Tamer (Game)",
            "summary": "A physics-based game built with Construct 3 including AdMob and Facebook sharing integrations.",
            "stack": ["Construct 3", "AdMob", "Facebook OAuth"],
            "contribution": "Game design, ad integration, and social sharing implementation.",
            "image": "/static/projects/trash.jpg",
            "repo": "https://github.com/YovenBlast/Trash_Tamer_Homepage",
            "demo": "",
            "video_url": "",  # TODO: Add GitHub video URL
            "images_url": "https://github.com/YovenBlast/Trash_Tamer_Images"  # TODO: Add GitHub images folder URL
        },
        {
            "id": "mq4_butane",
            "name": "Butane Detection System",
            "summary": "Butane gas detection using MQ4 sensor and ESP8266 with LED alerts and Firebase logging.",
            "stack": ["ESP8266", "MQ4", "Firebase"],
            "contribution": "Wiring, threshold logic, and cloud logging. Provided code to trigger LED on detection.",
            "image": "/static/projects/mq4.jpg",
            "repo": "https://github.com/YovenBlast/app_C-",
            "demo": "",
            "video_url": "",  # TODO: Add GitHub video URL
            "images_url": ""  # TODO: Add GitHub images folder URL
        },
        {
            "id": "java_datetime",
            "name": "Java Date & Time Adjustment Program",
            "summary": "A console-based Java application that validates dates, detects leap years, and automatically adjusts time when adding hours, minutes, or seconds.",
            "stack": ["Java", "Scanner", "Algorithms"],
            "contribution": "Built full date-time logic: leap year detection, input validation, automatic rollover of time and date.",
            "image": "/static/projects/java1.jpg",
            "repo": "https://github.com/YovenBlast/app_java",
            "demo": "",
            "video_url": "",  # TODO: Add GitHub video URL
            "images_url": ""  # TODO: Add GitHub images folder URL
        }
    ]
}

# ---------------------------
# Templates
# ---------------------------
BASE_HTML = '''
<!doctype html>
<html lang="en" data-theme="dark">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ data.name }} - Portfolio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <style>
      :root {
        --bg-primary: #0f172a;
        --bg-secondary: #07132a;
        --text-primary: #e6eef8;
        --text-secondary: #94a3b8;
        --card-bg: rgba(255,255,255,0.03);
        --accent: #7dd3fc;
        --skill-badge-bg: rgba(255,255,255,0.05);
        --skill-badge-text: #ffffff;
        --border-color: rgba(255,255,255,0.1);
      }

      [data-theme="light"] {
        --bg-primary: #f8fafc;
        --bg-secondary: #e2e8f0;
        --text-primary: #1e293b;
        --text-secondary: #475569;
        --card-bg: #ffffff;
        --accent: #0284c7;
        --skill-badge-bg: #e0f2fe;
        --skill-badge-text: #0c4a6e;
        --border-color: #cbd5e1;
      }

      body { 
        background: linear-gradient(180deg, var(--bg-primary) 0%, var(--bg-secondary) 100%); 
        color: var(--text-primary);
        transition: background 0.3s ease, color 0.3s ease;
        min-height: 100vh;
      }

      .card { 
        background: var(--card-bg); 
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
      }

      .accent { color: var(--accent); }

      .skill-badge { 
        background: var(--skill-badge-bg); 
        color: var(--skill-badge-text);
        padding: 6px 12px; 
        border-radius: 999px; 
        margin: 4px; 
        display: inline-block;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid transparent;
      }

      .skill-badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 4px 12px rgba(125, 211, 252, 0.3);
        border-color: var(--accent);
        background: var(--accent);
        color: #ffffff;
      }

      .hero { padding: 60px 0; }

      .profile-img { 
        width: 160px; 
        height: 160px; 
        object-fit: cover; 
        border-radius: 50%; 
        box-shadow: 0 8px 30px rgba(0,0,0,0.6); 
        border: 4px solid var(--border-color);
        transition: border-color 0.3s ease;
      }

      .project-img { 
        width: 100%; 
        height: 180px; 
        object-fit: cover; 
        border-radius: 8px;
        filter: brightness(1.1);
      }

      a.glow { 
        text-decoration: none; 
        border-bottom: 1px dashed rgba(125,211,252,0.4); 
      }

      footer { 
        opacity: 0.7; 
        padding: 30px 0; 
      }

      .card h4,
      .card h5, 
      .card h6,
      .card p, 
      .card strong {
        color: var(--text-primary) !important;
        opacity: 1 !important;
      }

      .form-label {
        color: var(--text-primary) !important;
      }

      h3 {
        color: var(--text-primary) !important;
      }

      .card-body h5 {
        color: var(--text-primary) !important;
      }

      .cert-item {
        padding: 12px 0;
        border-bottom: 1px solid var(--border-color);
      }

      .cert-item:last-child {
        border-bottom: none;
      }

      .task-item {
        padding: 4px 0;
        padding-left: 20px;
        position: relative;
        color: var(--text-primary) !important;
      }

      .task-item:before {
        content: "•";
        position: absolute;
        left: 8px;
        color: var(--accent);
      }

      /* Theme Toggle Button */
      .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      }

      .theme-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(125, 211, 252, 0.3);
      }

      .theme-toggle svg {
        width: 24px;
        height: 24px;
        fill: var(--text-primary);
      }

      .navbar {
        background: var(--card-bg) !important;
        border-bottom: 1px solid var(--border-color);
      }

      .nav-link {
        color: var(--text-secondary) !important;
      }

      .nav-link:hover {
        color: var(--accent) !important;
      }

      .btn-outline-light {
        border-color: var(--border-color);
        color: var(--text-primary);
      }

      .btn-outline-light:hover {
        background: var(--accent);
        border-color: var(--accent);
        color: #ffffff;
      }

      .form-control {
        background: var(--card-bg);
        border-color: var(--border-color);
        color: var(--text-primary);
      }

      .form-control:focus {
        background: var(--card-bg);
        border-color: var(--accent);
        color: var(--text-primary);
      }

      [data-theme="light"] .text-muted {
        color: var(--text-secondary) !important;
      }

      .media-section {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid var(--border-color);
      }

      .video-container {
        position: relative;
        padding-bottom: 56.25%; /* 16:9 aspect ratio */
        height: 0;
        overflow: hidden;
        border-radius: 8px;
        margin-bottom: 15px;
      }

      .video-container video {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 8px;
      }
    </style>
  </head>
  <body>
    <!-- Theme Toggle Button -->
    <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
      <svg id="theme-icon-sun" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="display: none;">
        <path d="M12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12C18 15.3137 15.3137 18 12 18ZM12 16C14.2091 16 16 14.2091 16 12C16 9.79086 14.2091 8 12 8C9.79086 8 8 9.79086 8 12C8 14.2091 9.79086 16 12 16ZM11 1H13V4H11V1ZM11 20H13V23H11V20ZM3.51472 4.92893L4.92893 3.51472L7.05025 5.63604L5.63604 7.05025L3.51472 4.92893ZM16.9497 18.364L18.364 16.9497L20.4853 19.0711L19.0711 20.4853L16.9497 18.364ZM19.0711 3.51472L20.4853 4.92893L18.364 7.05025L16.9497 5.63604L19.0711 3.51472ZM5.63604 16.9497L7.05025 18.364L4.92893 20.4853L3.51472 19.0711L5.63604 16.9497ZM23 11V13H20V11H23ZM4 11V13H1V11H4Z"/>
      </svg>
      <svg id="theme-icon-moon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path d="M10 7C10 10.866 13.134 14 17 14C18.9584 14 20.729 13.1957 21.9995 11.8995C22 11.933 22 11.9665 22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C12.0335 2 12.067 2 12.1005 2.00049C10.8043 3.27098 10 5.04157 10 7ZM4 12C4 16.4183 7.58172 20 12 20C15.0583 20 17.7158 18.2839 19.062 15.7621C18.3945 15.9187 17.7035 16 17 16C12.0294 16 8 11.9706 8 7C8 6.29648 8.08133 5.60547 8.2379 4.938C5.71611 6.28423 4 8.9417 4 12Z"/>
      </svg>
    </button>

    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container">
        <a class="navbar-brand accent" href="#">{{ data.name }}</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav" aria-controls="nav" aria-expanded="false">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="nav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="#about">About</a></li>
            <li class="nav-item"><a class="nav-link" href="#projects">Projects</a></li>
            <li class="nav-item"><a class="nav-link" href="#experience">Experience</a></li>
            <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container">
      {% block content %}{% endblock %}
    </main>

    <footer class="text-center">
      <div class="container">Maheswaren Chinnasamy + Portfolio • {{ data.location }} • <a class="glow" href="{{ data.github }}">GitHub</a></div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
      AOS.init();

      // Theme Toggle Functionality
      function toggleTheme() {
        const html = document.documentElement;
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Toggle icons
        const sunIcon = document.getElementById('theme-icon-sun');
        const moonIcon = document.getElementById('theme-icon-moon');

        if (newTheme === 'light') {
          sunIcon.style.display = 'none';
          moonIcon.style.display = 'block';
        } else {
          sunIcon.style.display = 'block';
          moonIcon.style.display = 'none';
        }
      }

      // Load saved theme on page load
      document.addEventListener('DOMContentLoaded', function() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);

        const sunIcon = document.getElementById('theme-icon-sun');
        const moonIcon = document.getElementById('theme-icon-moon');

        if (savedTheme === 'light') {
          sunIcon.style.display = 'none';
          moonIcon.style.display = 'block';
        } else {
          sunIcon.style.display = 'block';
          moonIcon.style.display = 'none';
        }
      });
    </script>
  </body>
</html>
'''

INDEX_HTML = '''
{% extends 'base' %}
{% block content %}
<section class="hero text-center text-light">
  <div class="row align-items-center">
    <div class="col-md-4 text-md-start text-center" data-aos="fade-right">
      <img src="{{ data.profile_image }}" alt="profile" class="profile-img mb-3">
    </div>
    <div class="col-md-8" data-aos="fade-left">
      <h1 class="display-6">{{ data.name }}</h1>
      <p class="lead accent">{{ data.title }}</p>
      <p style="max-width:760px;">{{ data.summary }}</p>
      <p>
        <a class="btn btn-outline-light me-2" href="mailto:{{ data.email }}">Email me</a>
        <a class="btn btn-primary" href="#projects">View projects</a>
      </p>
    </div>
  </div>
</section>

<section id="about" class="my-5">
  <div class="row">
    <div class="col-md-6" data-aos="fade-up">
      <div class="card p-4">
        <h4>About</h4>
        <p>{{ data.summary }}</p>
        <h6>Skills</h6>
        {% for cat, items in data.skills.items() %}
          <strong class="text-capitalize">{{ cat }}:</strong>
          <div class="mt-2 mb-3">
            {% for item in items %}
              <span class="skill-badge">{{ item }}</span>
            {% endfor %}
          </div>
        {% endfor %}
      </div>
    </div>
    <div class="col-md-6" data-aos="fade-up" data-aos-delay="100">
      <div class="card p-4">
        <h4>Education & Experience</h4>

        <!-- CIM Finance (Present - Most Recent) -->
        <p><strong>Working at CIM</strong> — CIM Finance Services Ltd <br><small>Present</small><br>I work in software testing and development, doing forms, AI integration, and automations.</p>

        <hr>

        <!-- SD Worx Internship (March 2024) -->
        <p><strong>Software Tester Intern</strong> — SD Worx Mauritius <br><small>March 2024</small><br>Worked on real-world testing tasks; learned teamwork, workflows, and testing tools.</p>

        <hr>

        <!-- Education (Expected Feb 2025 - Oldest) -->
        {% for edu in data.education %}
          <p><strong>{{ edu.degree }}</strong><br>{{ edu.school }} — <small>{{ edu.date }}</small></p>
        {% endfor %}
      </div>
    </div>
  </div>
</section>

<section id="certifications" class="my-5">
  <h3 data-aos="fade-up">Certifications</h3>
  <div class="row">
    <div class="col-12" data-aos="fade-up">
      <div class="card p-4">
        {% for cert in data.certifications %}
          <div class="cert-item">
            <h6 class="mb-1">{{ cert.name }}</h6>
            <p class="mb-1"><strong>{{ cert.issuer }}</strong> — <small>{{ cert.date }}</small></p>
            {% if cert.credential_url %}
              <a href="{{ cert.credential_url }}" target="_blank" class="btn btn-sm btn-outline-light mt-2">View Credential</a>
            {% endif %}
          </div>
        {% endfor %}
      </div>
    </div>
  </div>
</section>

<section id="projects" class="my-5">
  <h3 data-aos="fade-up">Projects</h3>
  <div class="row">
    {% for p in data.projects %}
      <div class="col-md-6 col-lg-4 mb-4" data-aos="zoom-in">
        <div class="card h-100 p-3">
          <img src="{{ p.image }}" class="project-img" alt="{{ p.name }}">
          <div class="card-body">
            <h5>{{ p.name }}</h5>
            <p>{{ p.summary }}</p>
            <div class="mb-2">
              {% for t in p.stack %}
                <span class="skill-badge">{{ t }}</span>
              {% endfor %}
            </div>
            <a href="/project/{{ p.id }}" class="btn btn-outline-light btn-sm">Read more</a>
            {% if p.repo %}<a href="{{ p.repo }}" class="btn btn-light btn-sm ms-2" target="_blank">Code</a>{% endif %}
          </div>
        </div>
      </div>
    {% endfor %}
  </div>
</section>

<section id="experience" class="my-5">
  <h3 data-aos="fade-up">Experience Highlights</h3>
  <div class="row">
    {% for exp in data.experience %}
      <div class="col-md-6" data-aos="fade-up" data-aos-delay="50">
        <div class="card p-3 mb-3">
          <h5>{{ exp.role }}@ {{ exp.company }}</small></h5>
          {% if exp.position %}
            <p class="mb-2"><strong>Position:</strong> <span class="accent">{{ exp.position }}</span></p>
          {% endif %}
          <p>{{ exp.details }}</p>
          {% if exp.tasks %}
            <p class="mb-2"><strong>Key Tasks:</strong></p>
            <div class="mb-2">
              {% for task in exp.tasks %}
                <div class="task-item">{{ task }}</div>
              {% endfor %}
            </div>
          {% endif %}
          {% if exp.technologies %}
            <p class="mb-2"><strong>Technologies used:</strong></p>
            <div class="mb-2">
              {% for tech in exp.technologies %}
                <span class="skill-badge">{{ tech }}</span>
              {% endfor %}
            </div>
          {% endif %}
          {% if exp.role == "Software Tester Intern" %}
            <div class="mt-3">
              <a class="btn btn-outline-light btn-sm" href="{{ data.github }}" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github me-2" viewBox="0 0 16 16">
                  <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                </svg>
                View My Testimonials on GitHub
              </a>
            </div>
          {% endif %}
        </div>
      </div>
    {% endfor %}
  </div>
</section>

<section id="contact" class="my-5">
  <h3 data-aos="fade-up">Get in touch</h3>
  <div class="row">
    <div class="col-md-6" data-aos="fade-right">
      <div class="card p-4">
        <h5>Contact</h5>
        <p>Email: <a href="mailto:{{ data.email }}">{{ data.email }}</a></p>
        <p>LinkedIn: <a href="{{ data.linkedin }}" target="_blank">Profile</a></p>
        <p>GitHub: <a href="{{ data.github }}" target="_blank">{{ data.github }}</a></p>
        <p><a class="btn btn-outline-light" href="https://github.com/YovenBlast/CV/blob/main/CV%20M%20Chinnasamy_2025.pdf" target="_blank">Download CV</a></p>
      </div>
    </div>
    <div class="col-md-6" data-aos="fade-left">
      <div class="card p-4">
        <h5>Quick message</h5>
        <form method="post" action="/contact">
          <div class="mb-3">
            <label class="form-label">Your name</label>
            <input class="form-control" name="name">
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input class="form-control" name="email">
          </div>
          <div class="mb-3">
            <label class="form-label">Message</label>
            <textarea class="form-control" name="message"></textarea>
          </div>
          <button class="btn btn-outline-light">Send</button>
          <small class="d-block mt-2 text-muted">(This demo form currently just shows a thank-you page.)</small>
        </form>
      </div>
    </div>
  </div>
</section>
{% endblock %}
'''

PROJECT_HTML = '''
{% extends 'base' %}
{% block content %}
<section class="my-5">
  <a href="/" class="btn btn-sm btn-outline-light mb-3">Back</a>
  <div class="card p-4">
    <div class="row">
      <div class="col-md-5">
        <img src="{{ project.image }}" class="img-fluid rounded" alt="{{ project.name }}">
      </div>
      <div class="col-md-7">
        <h2>{{ project.name }}</h2>
        <p>{{ project.summary }}</p>
        <h6>Stack</h6>
        <p>{% for s in project.stack %}<span class="skill-badge">{{ s }}</span>{% endfor %}</p>
        <h6>Contribution</h6>
        <p>{{ project.contribution }}</p>
        {% if project.repo %}<p><a class="btn btn-sm btn-outline-light" href="{{ project.repo }}" target="_blank">View code</a></p>{% endif %}
      </div>
    </div>

    <!-- Project Video Section -->
    {% if project.video_url %}
    <div class="media-section">
      <h5>Project Video</h5>
      <div class="video-container">
        <video controls>
          <source src="{{ project.video_url }}" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>
      <p class="text-center">
        <a href="{{ project.video_url }}" target="_blank" class="btn btn-sm btn-outline-light">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github me-2" viewBox="0 0 16 16">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
          </svg>
          View Video on GitHub
        </a>
      </p>
    </div>
    {% endif %}

    <!-- Project Images Section -->
    {% if project.images_url %}
    <div class="media-section">
      <h5>Project Images</h5>
      <p>View additional project screenshots and images on GitHub.</p>
      <p>
        <a href="{{ project.images_url }}" target="_blank" class="btn btn-sm btn-outline-light">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github me-2" viewBox="0 0 16 16">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
          </svg>
          View Images on GitHub
        </a>
      </p>
    </div>
    {% endif %}
  </div>
</section>
{% endblock %}
'''

THANK_YOU_HTML = '''
{% extends 'base' %}
{% block content %}
<section class="my-5 text-center">
  <div class="card p-4">
    <h3>Thank you, {{ name }}!</h3>
    <p>Your message has been received. I will get back to you at {{ email }} (demo behavior).</p>
    <a href="/" class="btn btn-primary">Back to portfolio</a>
  </div>
</section>
{% endblock %}
'''

# ---------------------------
# Register templates in Flask's template loader using render_template_string hack
# ---------------------------
from jinja2 import DictLoader
app.jinja_loader = DictLoader({
    'base': BASE_HTML,
    'index.html': INDEX_HTML,
    'project.html': PROJECT_HTML,
    'thankyou.html': THANK_YOU_HTML,
})

# ---------------------------
# Routes
# ---------------------------
@app.route('/')
def index():
    return render_template_string(app.jinja_loader.get_source(app.jinja_env, 'index.html')[0], data=DATA)

@app.route('/project/<pid>')
def project(pid):
    proj = next((p for p in DATA['projects'] if p['id'] == pid), None)
    if not proj:
        return redirect(url_for('index'))
    return render_template_string(app.jinja_loader.get_source(app.jinja_env, 'project.html')[0], data=DATA, project=proj)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', 'Friend')
    email = request.form.get('email', 'unknown')
    message = request.form.get('message', '')
    # Demo behaviour: show thank you page. Replace with real email sending if required.
    return render_template_string(app.jinja_loader.get_source(app.jinja_env, 'thankyou.html')[0], data=DATA, name=name, email=email)

# ---------------------------
# Static files note
# ---------------------------
# For the images to show, create a folder named 'static' next to this file and add:
# - profile.jpg (your photo)
# - projects/compost.jpg, parking.jpg, hotel.jpg, trash.jpg, mq4.jpg
# If you don't have images, point DATA['profile_image'] and project['image'] to external URLs.

if __name__ == '__main__':
    app.run(debug=True)
