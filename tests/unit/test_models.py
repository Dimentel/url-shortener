# from datetime import datetime, timedelta
# from src.models import User, Link
# import uuid
#
#
# def test_user_model():
#     user = User(
#         email="test@user.com",
#         hashed_password="hashed123",
#         is_active=True,
#         is_superuser=False,
#         is_verified=False,
#     )
#     assert user.email == "test@user.com"
#     assert user.hashed_password == "hashed123"
#     assert user.is_active is True
#     assert user.is_superuser is False
#     assert user.is_verified is False
#
#
# def test_link_model():
#     user_id = uuid.uuid4()
#     link = Link(
#         original_url="https://example.com",
#         short_code="ex1234",
#         user_id=user_id,
#         created_at=datetime.now(),
#         expires_at=datetime.now() + timedelta(days=7),
#         clicks=0,
#     )
#     assert link.original_url == "https://example.com"
#     assert link.clicks == 0
#     assert link.short_code == "ex1234"
#     assert link.user_id == user_id
#     assert isinstance(link.created_at, datetime)
#     assert isinstance(link.expires_at, datetime)
