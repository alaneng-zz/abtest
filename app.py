from flask import Flask, render_template, url_for, request, make_response
from scipy.stats import beta 
import mpld3
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
app.config.from_object(__name__)



@app.route('/', methods=['GET'])
def landing():
    return render_template('index.html')

@app.route('/stats', methods=['POST'])
def create_stats():
    data = request.form
    x = np.linspace(0.1,0.6,200)
    y = beta.pdf(x, 1 + int(data['conversion_a']), 1 + int(data['allocation_a']) - int(data['conversion_a']))

    plt.plot(x,y, label='a')
    plt.savefig('mychart')

    fig=Figure()
    ax=fig.add_subplot(111)

    canvas=FigureCanvas(fig)
    png_output = StringIO.StringIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'

    return response


if __name__ == '__main__':
    app.run()