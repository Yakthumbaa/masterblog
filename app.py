from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
DATA_FILEPATH = "blog_data.json"


def fetch_blog_data(filepath=DATA_FILEPATH, post_id=None):
    """
    Retrieves the blog data. If a post id param has argument then the post dictionary is
    returned, otherwise the whole data is returned.
    :param filepath:
    :param post_id:
    :return:
    """
    with open(filepath, "r") as handle:
        blog_data = json.loads(handle.read())
    if not post_id:
        return blog_data
    else:
        for post_dict in blog_data:
            if post_dict["id"] == post_id:
                return post_dict
        return None


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


def add_post(post_dict):
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

    # Append the new_dict to data
    data.append(new_dict)

    # Save the data to file
    save_to_file(data)


def delete_post(post_id):
    """
    Deletes a post that corresponds to the id.
    :param post_id:
    :return:
    """
    # Find the blog post with the given id and remove it from the list
    data = fetch_blog_data()
    new_data = []
    for post in data:
        if post["id"] == post_id:
            continue
        else:
            new_data.append(post)
    save_to_file(new_data)


@app.route('/')
def index():
    """
    Home page. Renders the index.html template
    :return:
    """
    blog_posts = fetch_blog_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Adds a new post by calling the add_post method.
    :return:
    """
    if request.method == 'POST':

        # Retrieve form data
        author = request.form['author'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        # Prepare data to pass to the add_post method
        post_dict = {"title": title, "author": author, "content": content}
        add_post(post_dict)

        # Redirect
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Deletes a post and updates the data file. Routes back to homepage.
    :param post_id:
    :return:
    """
    delete_post(post_id)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['POST', 'GET'])
def update(post_id):
    """
    Updates the values for the corresponding post id.
    :param post_id:
    :return:
    """
    # Fetch the blog posts from the JSON file
    post = fetch_blog_data(post_id=post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':

        # Fetch the values from the post method
        author = request.form['author'].strip()
        title = request.form['title'].strip()
        content = request.form['content'].strip()

        # Prepare post data and update
        new_post = {"id": post_id, "author": author, "title": title, "content": content}
        delete_post(post_id)
        add_post(new_post)

        # Redirect back to index
        return redirect(url_for('index'))

    # Else display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
