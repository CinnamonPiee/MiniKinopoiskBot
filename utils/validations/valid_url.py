from urllib.parse import urlparse


def valid_url(url: str) -> str | None:
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
        else:
            return None
    except:
        return None
