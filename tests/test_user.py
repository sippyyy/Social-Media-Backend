import pytest
from app import schemas
from jose import jwt
from app.oauth2 import SECRET_KEY,ALGORITHM


@pytest.mark.parametrize("email,password,expected",[
    ("thuy@gmail.com","nguyenthuy0308",True),
    ("thuy2@gmail.com","nguyenthuy0308",True)
])
def test_create_user(client,email, password, expected):

    res = client.post("/users/",json={"email":email,"password":password})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email ==  email
    assert res.status_code == 201

def test_login(client,test_user):
    res = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    res_login =schemas.Token(**res.json())
    payload = jwt.decode(res_login.token,SECRET_KEY,algorithms=ALGORITHM)
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert res_login.token_type == 'bearer'
    assert res.status_code == 200
    
@pytest.mark.parametrize("email,password,status_code",[
    ("kaka","wrong",403),
    ("thuy@gmail.com","sadasdasd",403),
    (None, "asdasd",422),
    ("thuy@gmail.com",None,422)
])
def test_incorrect_password_login(client,email,password,status_code):
    res = client.post("/login",data={"username":email,"password":password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'wrong password'or res.json().get('detail') == f'No user found with email {email}'
