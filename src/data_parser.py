from selenium import webdriver
from bs4 import BeautifulSoup


def get_text_from_url(url):
    """
    Extracts all text data from a given URL.

    Args:
        url: The URL of the website to parse.

    Returns:
        A string containing all the text data from the website.
    """

    try:
        # Send an HTTP GET request to the URL
        dr = webdriver.Chrome()
        dr.get(url)
        # response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(dr.page_source, 'html.parser')

        # Extract all text data (excluding script and style tags)
        text = soup.get_text()

        return text

    except Exception as e:
        print(f"An error occurred while fetching the URL: {e}")
        return ""


def test_urls():
    url_about = "https://www.canva.com/design/DAFmiiHpO7Q/view"
    url_hackathon = "https://www.canva.com/design/DAFmGtEKkWs/view?embed"
    text_data = get_text_from_url(url_hackathon)

    if text_data:
        print("Extracted text data:")
        print(text_data)
    else:
        print("Failed to extract text data.")


def extract_context_from_file(file_path: str) -> list[dict]:
    lines = None
    with open(file_path, 'r') as f:
        lines = f.readlines()

    return [{"role": "system", "content": line} for line in lines]


if __name__ == '__main__':
    # Example usage
    print(extract_context_from_file("../data/cold_start_data.txt"))
