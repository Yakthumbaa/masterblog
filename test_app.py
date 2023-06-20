import pytest
import json
import app

data_filepath = "test_blog_data.json"


def test_fetch_blog_data():
    """
    Test the method to fetch the blog data list. The data in the blog_data.json is a list
    of dictionaries with certain keys that relate to the blog post data.
    :return:
    """
    # Initialize...
    blog_data = app.fetch_blog_data(data_filepath)

    # Check if the data is a list
    assert type(blog_data) == list

    # Check if the keys match and that the list items are dicts
    dict_keys = blog_data[0].keys()
    valid_keys = ["id", "author", "title", "content"]
    for key in dict_keys:
        assert key in valid_keys

    # Check the values...
    dict_vals = blog_data[0].values()
    valid_values = [1, "John Doe", "First Post", "This is my first post."]
    for val in dict_vals:
        assert val in valid_values

    # Check the values...
    dict_vals = blog_data[1].values()
    valid_values = [2, "Jane Doe", "Second Post", "This is another post."]
    for val in dict_vals:
        assert val in valid_values


if __name__ == "__main__":
    pytest.main()