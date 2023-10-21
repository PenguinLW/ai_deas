from flask import Flask, render_template, request, send_file, after_this_request
from weasyprint import HTML
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', None)
        if url is None:
            return 'Missing URL', 400
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        try:
            output = tempfile.mktemp(suffix='.pdf')
            HTML(url=url).write_pdf(output)
            @after_this_request
            def remove_file(response):
                os.remove(output)
                return response
            return send_file(os.path.realpath(output), as_attachment=True)
        except Exception as e:
            return str(e), 400
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)
