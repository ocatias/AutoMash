def url_to_id(url):
    """
        Transforms the url of a youtube video to its id
    """
    return url.split("watch?v=")[1]
