def test_awards_longest_fastest_consecutive_awards(client):
    """Teste Intervalo de prêmios"""
    response = client.get("/awards/longest-fastest-consecutive-awards")
    assert response.status_code == 200
    assert response.json == {"max": [{"followingWin": 1990, "interval": 6, "previousWin": 1984, "producer": "Bo Derek"}], "min": [{"followingWin": 1990, "interval": 6, "previousWin": 1984, "producer": "Bo Derek"}]}
