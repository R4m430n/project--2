"""
Flask + Bootstrap 5 application that serves a very large form and opens the default
web browser automatically when you run the script.

Usage:
1. Install requirements: pip install flask
2. Run: python flask_bootstrap_large_form.py
3. The default browser will open at http://127.0.0.1:5000

Notes:
- If you want the server reachable from other devices on the network, set HOST = '0.0.0.0'
  and use the machine's LAN IP instead of 127.0.0.1 when opening the browser.
- For production use, deploy with a proper WSGI server (gunicorn/uvicorn) behind a
  reverse proxy. This script is for development/demo purposes.
"""
from flask import Flask, request, render_template_string, redirect, url_for, flash
import webbrowser
import threading
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Very large Bootstrap form template (single-file app using render_template_string for simplicity)
TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Juda katta forma - Flask + Bootstrap</title>
    <!-- Bootstrap 5 CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
    <div class="container my-4">
      <h1 class="mb-3">Juda katta forma</h1>
      <p class="text-muted">Bu demo: ko'plab maydonlar, bo'limlar va kichik JavaScript yordamida dinamik satr qo'shish.</p>

      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <div class="alert alert-success">{{ messages[0] }}</div>
        {% endif %}
      {% endwith %}

      <form method="POST" enctype="multipart/form-data" id="bigForm">
        <div class="card mb-3">
          <div class="card-header">Shaxsiy ma'lumotlar</div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Ism</label>
                <input name="first_name" class="form-control" required>
              </div>
              <div class="col-md-6">
                <label class="form-label">Familiya</label>
                <input name="last_name" class="form-control" required>
              </div>
              <div class="col-md-4">
                <label class="form-label">Elektron pochta</label>
                <input type="email" name="email" class="form-control" required>
              </div>
              <div class="col-md-4">
                <label class="form-label">Telefon</label>
                <input name="phone" class="form-control">
              </div>
              <div class="col-md-4">
                <label class="form-label">Tug'ilgan sana</label>
                <input type="date" name="birthdate" class="form-control">
              </div>
              <div class="col-12">
                <label class="form-label">Manzil</label>
                <input name="address" class="form-control">
              </div>
            </div>
          </div>
        </div>

        <div class="card mb-3">
          <div class="card-header">Ish tajribasi (dinamik qo'shish)</div>
          <div class="card-body">
            <div id="jobsContainer">
              <!-- JavaScript will clone this template -->
              <div class="job-entry row g-2 align-items-end mb-2">
                <div class="col-md-5">
                  <label class="form-label">Kompaniya</label>
                  <input name="company[]" class="form-control">
                </div>
                <div class="col-md-4">
                  <label class="form-label">Lavozim</label>
                  <input name="position[]" class="form-control">
                </div>
                <div class="col-md-2">
                  <label class="form-label">Yillar</label>
                  <input name="years[]" class="form-control" placeholder="2020-2022">
                </div>
                <div class="col-md-1 text-end">
                  <button type="button" class="btn btn-outline-danger remove-job">×</button>
                </div>
              </div>
            </div>

            <div class="mt-2">
              <button id="addJob" type="button" class="btn btn-primary">+ Ish qo'shish</button>
            </div>
          </div>
        </div>

        <div class="card mb-3">
          <div class="card-header">Ta'lim</div>
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Universitet</label>
                <input name="university" class="form-control">
              </div>
              <div class="col-md-3">
                <label class="form-label">Boshlanish yili</label>
                <input name="edu_start" class="form-control" placeholder="2016">
              </div>
              <div class="col-md-3">
                <label class="form-label">Tugash yili</label>
                <input name="edu_end" class="form-control" placeholder="2020">
              </div>
              <div class="col-12">
                <label class="form-label">Ilmiy yo'nalish</label>
                <input name="major" class="form-control">
              </div>
            </div>
          </div>
        </div>

        <div class="card mb-3">
          <div class="card-header">Qo'shimcha</div>
          <div class="card-body">
            <div class="mb-3">
              <label class="form-label">Biografiya / ma'lumot</label>
              <textarea name="bio" rows="5" class="form-control"></textarea>
            </div>
            <div class="mb-3">
              <label class="form-label">Rezyume (fayl)</label>
              <input type="file" name="resume" class="form-control">
            </div>

            <div class="row g-3">
              <div class="col-md-4">
                <label class="form-label">LinkedIn</label>
                <input name="linkedin" class="form-control" placeholder="https://...">
              </div>
              <div class="col-md-4">
                <label class="form-label">GitHub</label>
                <input name="github" class="form-control" placeholder="https://...">
              </div>
              <div class="col-md-4">
                <label class="form-label">Portfolio</label>
                <input name="portfolio" class="form-control" placeholder="https://...">
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex justify-content-between mb-4">
          <div>
            <button type="submit" class="btn btn-success">Yuborish</button>
            <button type="reset" class="btn btn-secondary">Tozalash</button>
          </div>
          <div class="text-end text-muted">Demo forma — hech qanday ma'lumot saqlanmaydi.</div>
        </div>
      </form>

      <footer class="text-muted small mt-4">Flask + Bootstrap demo — Ramazon uchun tayyorlandi</footer>
    </div>

    <script>
      // Add job entry
      document.getElementById('addJob').addEventListener('click', function () {
        const container = document.getElementById('jobsContainer');
        const template = container.querySelector('.job-entry');
        const clone = template.cloneNode(true);
        // clear inputs
        clone.querySelectorAll('input').forEach(i => i.value = '');
        container.appendChild(clone);
      });

      // Remove job entry (event delegation)
      document.getElementById('jobsContainer').addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-job')) {
          const entries = document.querySelectorAll('.job-entry');
          if (entries.length <= 1) { // keep at least one
            // clear fields instead
            entries[0].querySelectorAll('input').forEach(i => i.value = '');
            return;
          }
          e.target.closest('.job-entry').remove();
        }
      });

      // Basic client-side validation before submit (example)
      document.getElementById('bigForm').addEventListener('submit', function (e) {
        const email = document.querySelector('input[name="email"]').value;
        if (!email) {
          e.preventDefault();
          alert('Elektron pochta manzilingizni kiriting');
        }
      });
    </script>

    <!-- Bootstrap JS (Popper included) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect form fields (this demo won't save files to disk permanently)
        data = {}
        for key, val in request.form.items():
            data[key] = val

        # For array inputs like company[] Flask collects them via getlist
        data['companies'] = request.form.getlist('company[]')
        data['positions'] = request.form.getlist('position[]')
        data['years'] = request.form.getlist('years[]')

        # handle uploaded resume file temporarily
        resume = request.files.get('resume')
        if resume and resume.filename:
            # for demo only: do NOT save untrusted files in production without checks
            resume_content = resume.read()
            data['resume_filename'] = resume.filename
            data['resume_size'] = len(resume_content)
        else:
            data['resume_filename'] = None

        # Here you would normally validate and save the data to a database
        # For demo, we just flash a success message and print to console
        print('FORM SUBMITTED:')
        for k, v in data.items():
            print(k, ':', v)

        flash('Forma muvaffaqiyatli yuborildi! Konsolga chiqdi (server tomoni).')
        return redirect(url_for('index'))

    return render_template_string(TEMPLATE)


def open_browser(url):
    # Wait a moment to let the server start, then open the browser.
    # Using a thread so it doesn't block the main thread.
    webbrowser.open_new(url)


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 5000
    url = f'http://{HOST}:{PORT}/'
    # Start a timer thread to open the browser shortly after the server starts.
    threading.Timer(1.0, open_browser, args=(url,)).start()
    # Run Flask development server
    app.run(host=HOST, port=PORT, debug=True)
