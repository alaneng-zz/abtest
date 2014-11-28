from flask import Flask, render_template, url_for, request, make_response, Response
from scipy.stats import beta 
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def landing():
    return render_template('index.html')

@app.route('/stats', methods=['POST'])
def plot_stats():
    data = request.form
    x = np.linspace(0.1,0.6,200)
    y_a = beta.pdf(x, 1 + int(data['conversion_a']), 1 + int(data['allocation_a']) - int(data['conversion_a']))
    y_b = beta.pdf(x, 1 + int(data['conversion_b']), 1 + int(data['allocation_b']) - int(data['conversion_b']))

    plt.plot(x, y_a, label='A')
    plt.plot(x, y_b, label='B')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_data = base64.b64encode(buf.read())

    response = Response(response=image_data, status=200)
    buf.close()
    plt.close()

    return response


if __name__ == '__main__':
    app.run()