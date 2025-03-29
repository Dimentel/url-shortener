# from src.routers.links import generate_short_code
# import string
#
#
# def test_short_code_generation():
#     code = generate_short_code()
#     assert len(code) == 6
#     # Проверяем, что код состоит только из букв и цифр
#     assert all(c in string.ascii_letters + string.digits for c in code)
#
#
# def test_short_code_uniqueness():
#     codes = {generate_short_code() for _ in range(100)}
#     assert len(codes) == 100  # Все коды уникальны
