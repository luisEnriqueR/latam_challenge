from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.exceptions.user_exceptions import (
    EmailAlreadyExists,
    NoFieldsToUpdate,
    UsernameAlreadyExists,
    UserNotFound,
)
from app.models.user import RoleEnum, User
from app.schemas.users import UserCreate, UserUpdate
from app.services.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users_paginated,
    update_user,
)


@pytest.fixture
def mock_session(monkeypatch):
    session = MagicMock()
    monkeypatch.setattr(session, "exec", MagicMock())
    monkeypatch.setattr(session, "get", MagicMock())
    monkeypatch.setattr(session, "add", MagicMock())
    monkeypatch.setattr(session, "commit", MagicMock())
    monkeypatch.setattr(session, "refresh", MagicMock())
    return session


@pytest.fixture
def sample_user_create_data():
    return UserCreate(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        role=RoleEnum.user,
    )


@pytest.fixture
def existing_user_data():
    now = datetime.now()
    return User(
        id=1,
        username="existinguser",
        email="existing@example.com",
        first_name="Existing",
        last_name="Person",
        role=RoleEnum.admin,
        active=True,
        created_at=now,
        updated_at=now,
    )


def test_create_user_success(
    mock_session, sample_user_create_data, monkeypatch
):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    monkeypatch.setattr(
        mock_session, "exec", MagicMock(return_value=mock_exec_result)
    )

    def refresh_side_effect(user_obj):
        user_obj.id = 1

    mock_session.refresh.side_effect = refresh_side_effect

    created_user = create_user(sample_user_create_data, mock_session)

    assert created_user is not None
    assert created_user.username == sample_user_create_data.username
    assert created_user.email == sample_user_create_data.email
    assert (
        created_user.first_name == sample_user_create_data.first_name
    )
    assert created_user.last_name == sample_user_create_data.last_name
    assert created_user.role == sample_user_create_data.role
    assert created_user.active is True
    assert created_user.id == 1
    assert isinstance(created_user.created_at, datetime)
    assert isinstance(created_user.updated_at, datetime)

    assert mock_session.exec.call_count == 2
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    mock_session.refresh.assert_called_once_with(created_user)


def test_create_user_username_exists(
    mock_session,
    sample_user_create_data,
    existing_user_data,
    monkeypatch,
):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_user_data
    monkeypatch.setattr(
        mock_session, "exec", MagicMock(return_value=mock_exec_result)
    )

    with pytest.raises(UsernameAlreadyExists):
        create_user(sample_user_create_data, mock_session)

    mock_session.exec.assert_called_once()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test_create_user_email_exists(
    mock_session,
    sample_user_create_data,
    existing_user_data,
):
    mock_exec_username_check = MagicMock()
    mock_exec_username_check.first.return_value = None
    mock_exec_email_check = MagicMock()
    mock_exec_email_check.first.return_value = existing_user_data
    mock_session.exec.side_effect = [
        mock_exec_username_check,
        mock_exec_email_check,
    ]

    with pytest.raises(EmailAlreadyExists):
        create_user(sample_user_create_data, mock_session)

    assert mock_session.exec.call_count == 2
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test_get_user_by_id_success(
    mock_session, existing_user_data, monkeypatch
):
    user_id = existing_user_data.id
    monkeypatch.setattr(
        mock_session,
        "get",
        MagicMock(return_value=existing_user_data),
    )

    retrieved_user = get_user_by_id(user_id, mock_session)

    assert retrieved_user is not None
    assert retrieved_user == existing_user_data
    assert retrieved_user.id == user_id
    assert retrieved_user.first_name == existing_user_data.first_name
    mock_session.get.assert_called_once_with(User, user_id)


def test_get_user_by_id_not_found(mock_session, monkeypatch):
    user_id = 999
    monkeypatch.setattr(
        mock_session, "get", MagicMock(return_value=None)
    )

    with pytest.raises(UserNotFound) as excinfo:
        get_user_by_id(user_id, mock_session)

    assert str(user_id) in str(excinfo.value)
    mock_session.get.assert_called_once_with(User, user_id)


def test_get_users_paginated_success(mock_session, monkeypatch):
    now = datetime.now()
    user1 = User(
        id=1,
        username="user1",
        email="u1@e.com",
        first_name="U",
        last_name="One",
        role=RoleEnum.user,
        active=True,
        created_at=now,
        updated_at=now,
    )
    user2 = User(
        id=2,
        username="user2",
        email="u2@e.com",
        first_name="U",
        last_name="Two",
        role=RoleEnum.user,
        active=False,
        created_at=now,
        updated_at=now,
    )
    mock_users = [user1, user2]
    total_users = 5

    mock_exec_fetch = MagicMock()
    mock_exec_fetch.all.return_value = mock_users
    mock_exec_count = MagicMock()
    mock_exec_count.one.return_value = total_users
    monkeypatch.setattr(
        mock_session,
        "exec",
        MagicMock(side_effect=[mock_exec_fetch, mock_exec_count]),
    )

    page = 1
    limit = 2
    users, total = get_users_paginated(
        mock_session, page=page, limit=limit
    )

    assert users == mock_users
    assert total == total_users
    assert len(users) == 2
    assert mock_session.exec.call_count == 2


def test_update_user_success(
    mock_session, existing_user_data, monkeypatch
):
    user_id = existing_user_data.id
    update_payload = UserUpdate(
        first_name="UpdatedFirstName",
        last_name="UpdatedLastName",
        role=RoleEnum.user,
        active=False,
    )

    mock_user_instance = MagicMock(spec=User)
    mock_user_instance.id = existing_user_data.id
    mock_user_instance.first_name = existing_user_data.first_name
    mock_user_instance.last_name = existing_user_data.last_name
    mock_user_instance.role = existing_user_data.role
    mock_user_instance.active = existing_user_data.active

    monkeypatch.setattr(
        mock_session,
        "get",
        MagicMock(return_value=mock_user_instance),
    )

    updated_user = update_user(user_id, update_payload, mock_session)

    assert updated_user == mock_user_instance
    assert mock_user_instance.first_name == update_payload.first_name
    assert mock_user_instance.last_name == update_payload.last_name
    assert mock_user_instance.role == update_payload.role
    assert hasattr(mock_user_instance, "updated_at")
    assert isinstance(mock_user_instance.updated_at, datetime)

    mock_session.get.assert_called_once_with(User, user_id)
    mock_session.add.assert_called_once_with(mock_user_instance)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_user_instance)


def test_update_user_not_found(mock_session, monkeypatch):
    user_id = 999
    update_payload = UserUpdate(first_name="newname")
    monkeypatch.setattr(
        mock_session, "get", MagicMock(return_value=None)
    )

    with pytest.raises(UserNotFound) as excinfo:
        update_user(user_id, update_payload, mock_session)

    assert str(user_id) in str(excinfo.value)
    mock_session.get.assert_called_once_with(User, user_id)
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test_update_user_no_fields_to_update(
    mock_session, existing_user_data, monkeypatch
):
    user_id = existing_user_data.id
    update_payload = UserUpdate()

    mock_user_instance = MagicMock(
        spec=User, id=existing_user_data.id
    )
    monkeypatch.setattr(
        mock_session,
        "get",
        MagicMock(return_value=mock_user_instance),
    )

    with pytest.raises(NoFieldsToUpdate):
        update_user(user_id, update_payload, mock_session)

    mock_session.get.assert_called_once_with(User, user_id)
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()


def test_delete_user_success(
    mock_session, existing_user_data, monkeypatch
):
    user_id = existing_user_data.id

    monkeypatch.setattr(
        mock_session,
        "get",
        MagicMock(return_value=existing_user_data),
    )
    result = delete_user(user_id, mock_session)

    assert result is None

    mock_session.get.assert_called_once_with(User, user_id)
    mock_session.delete.assert_called_once_with(existing_user_data)
    mock_session.commit.assert_called_once()


def test_delete_user_not_found(mock_session, monkeypatch):
    user_id = 999  # An ID that we expect not to exist

    monkeypatch.setattr(
        mock_session, "get", MagicMock(return_value=None)
    )

    with pytest.raises(UserNotFound) as excinfo:
        delete_user(user_id, mock_session)

    assert str(user_id) in str(excinfo.value)

    mock_session.get.assert_called_once_with(User, user_id)
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
