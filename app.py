from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
DATA_FILEPATH = "blog_data.json"


def fetch_blog_data(filepath=DATA_FILEPATH):
    """
    Retrieves the blog data.
    :param filepath:
    :return:
    """
    with open(filepath, "r") as handle:
        blog_data = json.loads(handle.read())
    return blog_data


def save_to_file(data, filepath=DATA_FILEPATH):
    """
    Saves the new data to the filepath.
    :param data:
    :param filepath:
    :return: void
    """
    with open(filepath, "w") as handle:
        content = json.dumps(data, indent=2)
        handle.write(content)


def add_post_to_data(post_dict):
    """
    Adds a post to the list of data and saves it to the file.
    :param post_dict:
    :return:
    """
    # Retrieve old data
    data = fetch_blog_data()
    ids = [val for post in data for key, val in post.items() if key == "id"]
    # Generate a new id and a new dict with key 'id'
    new_id = max(ids) + 1
    new_dict = {"id": new_id}
    for key, val in post_dict.items():
        new_dict[key] = val
    # append the new_dict to data
    data.append(new_dict)
    # save the data to file
    save_to_file(data)


@app.route('/')
def index():
    blog_posts = fetch_blog_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        # Retrieve form data
        author = request.form['author'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        # Prepare data to pass onto the save_to_file method
        post_dict = {"title": title, "author": author, "content": content}
        add_post_to_data(post_dict)
        # Redirect
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    # Find the blog post with the given id and remove it from the list
    data = fetch_blog_data()
    new_data = []
    for post in data:
        if post["id"] == post_id:
            continue
        else:
            new_data.append(post)
    save_to_file(new_data)
    # Redirect back to the home page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
