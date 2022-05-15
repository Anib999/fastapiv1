import pytest
from app import schemas

# def test_get_all_post(authorized_client, test_posts):
#     res = authorized_client.get('/posts/sqlalch')
#     print(res.json())
#     assert res.status_code == 200

# def test_unauthorized_post(client, test_posts):
#     res = client.get('/posts/sqlalch')
#     assert res.status_code == 401

# def test_unauthorized_post_one(client, test_posts):
#     res = client.get(f'/posts/sqlgetone/{test_posts[0].id}')
#     assert res.status_code == 200

# def test_unauthorized_post_one_not(authorized_client, test_posts):
#     res = authorized_client.get(f'/posts/sqlgetone/520')
#     assert res.status_code == 404

# def test_authorized_post_one(authorized_client, test_posts):
#     res = authorized_client.get(f'/posts/sqlgetone/{test_posts[0].id}')
#     post = schemas.PostOut(**res.json())
#     assert post.Post.id == test_posts[0].id
#     assert res.status_code == 200

# @pytest.mark.parametrize('title, content, published', [
#     ('new 1', 'con 1', True),
#     ('new 2', 'con 2', False),
#     ('new 3', 'con 3', True),
# ])
# def test_create_post(authorized_client, test_user, test_posts, title, content, published):
#     res = authorized_client.post('/posts/sqlpost', json={'title': title, 'content': content, 'published': published})
#     created_post = schemas.Post(**res.json())
#     assert res.status_code == 201
#     assert created_post.title == title

# def test_un_delete_post(client, test_user, test_posts):
#     res = client.delete(f'/posts/sqldelete/{test_posts[0].id}')
#     assert res.status_code == 401

# def test_success_delete_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f'/posts/sqldelete/{test_posts[0].id}')
#     assert res.status_code == 204

# def test_unknown_delete_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f'/posts/sqldelete/500')
#     assert res.status_code == 404

# def test_other_delete_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f'/posts/sqldelete/{test_posts[2].id}')
#     assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'helao',
        'content': 'polpo',
        'id': test_posts[0].id
    }
    res = authorized_client.put(f'/posts/sqlput/{test_posts[0].id}', json=data)
    updated_post = schemas.UpdatePost(**res.json())
    assert res.status_code == 200

def test_other_update_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        'title': 'helao',
        'content': 'polpo',
        'id': test_posts[2].id
    }
    res = authorized_client.put(f'/posts/sqlput/{test_posts[2].id}', json=data)
    updated_post = schemas.UpdatePost(**res.json())
    assert res.status_code == 403