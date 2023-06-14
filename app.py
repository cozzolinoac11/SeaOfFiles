from flask import Flask, render_template, request, session, send_file
from database_connections import connected_host, file_database
import flask_configuration
import random

app = Flask(__name__)
app.secret_key = flask_configuration.flask_key


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/get_host_connected', methods=['GET', 'POST'])
def get_host_connected():
    host_list = connected_host.get_connected_host()
    return render_template('connected_host_page.html', connected_host=host_list, error="")


@app.route('/get_filename', methods=['GET', 'POST'])
def get_filename():
    selected_file = request.form['filename_selected']
    connected = connected_host.get_connected_host()
    host_list = file_database.get_containing_file(host_list=connected, filename=selected_file)
    if len(host_list) > 0:
        session['selected_file'] = selected_file
        session['host_list'] = host_list
        return render_template('select_host.html', containing_host=host_list)
    else:
        e = "ERROR! FILE NOT FOUND IN THE CONNECTED HOSTS!\nRetry to insert a correct filename!\n"
        likely_file = file_database.likely_file(connected=connected, filename=selected_file)
        if len(likely_file) > 0:
            e = e+"\nBelow is a list of files found in the system with a name similar to the one entered.\n"
        return render_template('connected_host_page.html', connected_host=connected, error=e, likely_file=likely_file)


@app.route('/get_selected_host', methods=['GET', 'POST'])
def get_selected_host():
    selected_host = request.form['selected_host']
    selected_file = session.get('selected_file', None)
    host_list = session.get('host_list', None)
    if selected_host in host_list:
        session['selected_host'] = selected_host
        return render_template('download_page.html', filename=selected_file, host_name=selected_host)
    else:
        e = "Invalid or not selected hostname!\nHost is automatically selected."
        selected_host = host_list[random.randint(0, len(host_list)-1)]
        session['selected_host'] = selected_host
        return render_template('download_page.html', filename=selected_file, host_name=selected_host, error=e)


@app.route('/download', methods=['GET', 'POST'])
def download():
    selected_host = session.get('selected_host', None)
    selected_file = session.get('selected_file', None)
    file_database.download_blob(selected_host, selected_file)
    downloaded_file = open('static/downloaded/'+selected_file, 'rb')
    return send_file(downloaded_file, download_name=selected_file, as_attachment=True)


if __name__ == '__main__':
    app.run(port=8000)
