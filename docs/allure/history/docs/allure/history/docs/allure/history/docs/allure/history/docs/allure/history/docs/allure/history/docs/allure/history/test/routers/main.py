"""Test Module. Main endpoint"""


def test_read_main(client):
    """Test main endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.request.path_url == "/docs"
