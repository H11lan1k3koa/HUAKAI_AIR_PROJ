#test create acct input
#import testing framework pytest
import pytest
from createacct import app


#set up temp testing version of app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#simulate acct creation process
def test_createacct_input(client):
    user_input = {
        "username": "testing+hewa+ersagain",
        "email": "wa+erislife123456@hawaiiangirl.com",
        "password": "Prettypineapples&Me123456",
        "first_name": "billie bobbie",
        "last_name": "joe jacobson",
        "dob": "01/01/1981",
        "mobile": "8089999999"
    }
    response = client.post('/register', json=user_input, follow_redirects=True)
    print("Error", response.get_json())
    assert response.status_code == 201