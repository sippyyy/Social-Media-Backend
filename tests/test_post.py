from app import schemas
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts')
    # def validate(post):
    #     return schemas.PostOut(**post)
    
    # posts_map = map(validate, res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
   
   
def test_get_all_your_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/myposts')
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    print(list(posts_map))
    assert res.status_code == 200

def test_unauthorized(client):
    res = client.get('/posts')
    assert res.status_code == 401
    
def test_authorized_user_one_post(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/myposts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.title == test_posts[0].title
    
def test_unautorized_user_get_your_post(client,test_posts):
    res = client.get(f'/posts/myposts/{test_posts[0].id}')
    assert res.status_code == 401
    
def test_get_one_post_public(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 200
    
def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/{len(test_posts)+1}')
    assert res.status_code == 404
    
