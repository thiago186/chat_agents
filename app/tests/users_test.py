

@pytest.fixture(name="session", scope="function")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session 

def test_create_user(session):
    test_email = "test@example.com"
    test_username = "testuser"
    test_password = "securepassword123"
    test_plan = "basic"

    user = User(email=test_email, username=test_username, current_plan=test_plan)
    user.set_password(test_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.user_id is not None
    assert user.email == test_email
    assert user.username == test_username
    assert user.verify_password(test_password) 
    assert user.current_plan == test_plan
    assert user.active is True
    assert user.created_at is not None
