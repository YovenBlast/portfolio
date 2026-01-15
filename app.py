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
    "title": "Software Developer \u2014 Aspiring Software Tester",
    "location": "Mauritius",
    "summary": (
        "I\'m Maheswaren, a software developer and aspiring software test engineer. "
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
            "details": "Worked on real-world testing tasks; learned teamwork, workflows, and testing tools."
        },
        {
            "role": "Working at CIM Finance Services Ltd",
            "company": "CIM Finance Services Ltd",
            "date": "Present",
            "details": "I work in software testing and development, doing forms, AI integration, and automations."
        }
    ],
    "education": [
        {"degree": "BSc (Hons) Software Engineering", "school": "University of Technology, Mauritius", "date": "Expected Feb 2025"}
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
            "demo": ""
        },
        {
            "id": "smart_parking",
            "name": "IoT-Based Smart Parking System",
            "summary": "Ultrasonic sensors detect car presence in zones; data sent via ESP8266 to a cloud DB.",
            "stack": ["ESP8266", "Ultrasonic sensors", "Firebase"],
            "contribution": "Sensor interfacing, zone logic, cloud push and simple web dashboard.",
            "image": "/static/projects/parking.webp",
            "repo": "https://github.com/YovenBlast/Smart-Parking-System",
            "demo": ""
        },
        {
            "id": "hotel_app",
            "name": "Hotel Booking App (Flutter)",
            "summary": "A Flutter hotel booking app with booking history and room management features.",
            "stack": ["Flutter", "Dart", "Firebase"],
            "contribution": "Built UI, booking logic, and integrated database helpers for images and room numbers.",
            "image": "/static/projects/HotelBooking.png",
            "repo": "https://github.com/TODO/hotel-booking-app",
            "demo": ""
        },
        {
            "id": "trash_tamer",
            "name": "Trash Tamer (Game)",
            "summary": "A physics-based game built with Construct 3 including AdMob and Facebook sharing integrations.",
            "stack": ["Construct 3", "AdMob", "Facebook OAuth"],
            "contribution": "Game design, ad integration, and social sharing implementation.",
            "image": "/static/projects/trash.jpg",
            "repo": "https://github.com/YovenBlast/Trash_Tamer_Homepage",
            "demo": ""
        },
        {
            "id": "mq4_butane",
            "name": "Butane Detection System",
            "summary": "Butane gas detection using MQ4 sensor and ESP8266 with LED alerts and Firebase logging.",
            "stack": ["ESP8266", "MQ4", "Firebase"],
            "contribution": "Wiring, threshold logic, and cloud logging. Provided code to trigger LED on detection.",
            "image": "/static/projects/mq4.jpg",
            "repo": "https://github.com/TODO/butane-detection",
            "demo": ""
        },
        {
            "id": "java_datetime",
            "name": "Java Date & Time Adjustment Program",
            "summary": "A console-based Java application that validates dates, detects leap years, and automatically adjusts time when adding hours, minutes, or seconds.",
            "stack": ["Java", "Scanner", "Algorithms"],
            "contribution": "Built full date-time logic: leap year detection, input validation, automatic rollover of time and date.",
            "image": "/static/projects/java1.jpg",
            "repo": "",
            "demo": ""
        }
]

}

# ---------------------------
# Templates
# ---------------------------
BASE_HTML = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ data.name }} - Portfolio</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <style>
      body { background: linear-gradient(180deg,#0f172a 0%, #07132a 100%); color: #e6eef8; }
      .card { background: rgba(255,255,255,0.03); border: none; }
      .accent { color: #7dd3fc; }
      .skill-badge{ background: rgba(255,255,255,0.05); padding:6px 8px; border-radius:999px; margin:4px; display:inline-block;}
      .hero { padding: 60px 0; }
      .profile-img { width:160px; height:160px; object-fit:cover; border-radius:50%; box-shadow: 0 8px 30px rgba(0,0,0,0.6); border:4px solid rgba(255,255,255,0.06); }
      .project-img { width:100%; height:180px; object-fit:cover; border-radius:8px; }
      a.glow { text-decoration:none; border-bottom:1px dashed rgba(125,211,252,0.4); }
      footer { opacity:0.7; padding:30px 0; }

       .card h5, 
  .card p, 
  .card .skill-badge {
      color: #ffffff !important;
      opacity: 1 !important;
  }

  .project-img {
      filter: brightness(1.1);
  }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-transparent">
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

    <footer class="text-center text-muted">
      <div class="container">Built with Python + Flask • {{ data.location }} • <a class="glow" href="{{ data.github }}">GitHub</a></div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script> AOS.init(); </script>
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
        {% for edu in data.education %}
          <p><strong>{{ edu.degree }}</strong><br>{{ edu.school }} — <small>{{ edu.date }}</small></p>
        {% endfor %}
        <hr>
        {% for exp in data.experience %}
          <p><strong>{{ exp.role }}</strong> — {{ exp.company }} <br><small>{{ exp.date }}</small><br>{{ exp.details }}</p>
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
          <h5>{{ exp.role }} <small class="text-muted">@ {{ exp.company }}</small></h5>
          <p>{{ exp.details }}</p>
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
        <p><a class="btn btn-outline-light" href="/download-cv">Download CV (sample)</a></p>
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
          <button class="btn btn-primary">Send</button>
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

@app.route('/download-cv')
def download_cv():
    # Create a tiny sample CV on the fly. You can replace this with a static file.
    sample = f"""
    {DATA['name']} - Resume\n\n{DATA['title']}\nLocation: {DATA['location']}\n\nSummary:\n{DATA['summary']}\n\nEducation:\n"""
    for e in DATA['education']:
        sample += f"- {e['degree']}, {e['school']} ({e['date']})\n"
    sample += "\nExperience:\n"
    for ex in DATA['experience']:
        sample += f"- {ex['role']} @ {ex['company']} ({ex['date']})\n  {ex['details']}\n"
    bio = io.BytesIO(sample.encode('utf-8'))
    bio.seek(0)
    return send_file(bio, as_attachment=True, download_name='Maheswaren_CV.txt', mimetype='text/plain')

# ---------------------------
# Static files note
# ---------------------------
# For the images to show, create a folder named 'static' next to this file and add:
# - profile.jpg (your photo)
# - projects/compost.jpg, parking.jpg, hotel.jpg, trash.jpg, mq4.jpg
# If you don't have images, point DATA['profile_image'] and project['image'] to external URLs.

if __name__ == '__main__':
    app.run(debug=True)