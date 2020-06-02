from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)


@app.route("/")
def index():
    return render_template_string(
        """<video controls width=500>
            <source src="{{ url_for('stream', filename='vid.mp4') }}">
        </video>"""
    )


@app.route("/stream/<filename>")
def stream(filename):
    return send_from_directory("static", filename)

app.run(debug=True)