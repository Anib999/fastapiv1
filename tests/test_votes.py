import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    newVote = models.Vote(post_id=test_posts[2].id, user_id=test_user['id'])
    session.add(newVote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post('/vote/', json={'post_id': test_posts[0].id, 'dir': 1})
    assert res.status_code == 201

def test_twice_vote_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={'post_id': test_posts[0].id, 'dir': 1})
    assert res.status_code == 201

def test_delete_vote_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post('/vote/', json={'post_id': test_posts[0].id, 'dir': 0})
    assert res.status_code == 404