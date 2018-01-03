import os
import zlib

from flask import Flask, render_template, redirect, url_for, request


class CompressedContentError(RuntimeError):
    pass


app = Flask(__name__)
# STORAGE_DIR = '/mnt/efs/'
STORAGE_DIR = '/Users/tomer/efs/'  # FOR DEBUG ONLY!


@app.route('/', methods=['GET', 'POST'])
def handle_route_index():
    if request.method == 'POST':
        message_id = request.form['message_id']
        return redirect(url_for('handle_route_message', message_id=message_id))
    else:
        return render_template('index.html')


@app.route('/<message_id>')
def handle_route_message(message_id):
    try:
        return get_message_content(message_id)
    except (CompressedContentError, FileNotFoundError) as error:
        return str(error)


def get_message_content(message_id):
    file_path = get_message_full_file_path(message_id)

    with open(file_path, 'rb') as f:
        contents = f.read()

    try:
        contents = zlib.decompress(contents)
        raise CompressedContentError('File {} is compressed'.format(file_path))

    except zlib.error as decompression_error:
        print(decompression_error)

    decoded_content = contents.decode('utf-8')
    return decoded_content


def get_message_full_file_path(message_id):
    if not isinstance(message_id, int):
        message_id = int(message_id)

    levels = list()

    # Create 4 levels

    for i in range(3):
        levels.append(str(message_id % 1000))
        message_id = int(message_id / 1000)

    levels.append(str(message_id))  # The 4th level
    levels.reverse()

    full_path = os.path.join(STORAGE_DIR, '/'.join(levels[:3]), levels[3] + '.html')
    return full_path


if __name__ == '__main__':
    app.run(debug=True)
