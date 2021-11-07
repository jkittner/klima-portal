def test_index(client):
    resp = client.get('/')
    data = resp.data.decode()
    assert resp.status_code == 200
    # navbar is inserted
    assert '<nav class="navbar' in data
    # navbar highlight is correct
    assert '<a class="nav-link active" href="/">Home - Overview</a>' in data
    # footer is included
    assert '<div class="footer py-2 mt-4" ' in data
    assert 'GitHub' in data
    assert 'Geographisches Institut RUB' in data


def test_compare(client):
    resp = client.get('/compare')
    data = resp.data.decode()
    assert resp.status_code == 200
    assert '<nav class="navbar' in data
    # navbar highlight is correct
    assert (
        '<a class="nav-link active" href="/compare">Stationsvergleich</a>'
    ) in data
    # footer is included
    assert '<div class="footer py-2 mt-4" ' in data
    assert 'GitHub' in data
    assert 'Geographisches Institut RUB' in data


def test_favicon(client):
    resp = client.get('/favicon.ico')
    data = resp.data.decode()
    assert resp.status_code == 200
    assert '<svg' in data


def test_robots(client):
    resp = client.get('/robots.txt')
    data = resp.data.decode()
    assert resp.status_code == 200
    assert data == 'User-agent: *\nDisallow: /\n'
