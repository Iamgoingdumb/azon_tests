# SENSITIVE_FIELDS = {
#     "password",
#     "api_key"
# }
#
# def mask_data(data: dict) -> dict:
#     return {
#         key: "***" if key.lower() in SENSITIVE_FIELDS else value
#         for key, value in data.items()
#     }
#
# payload = {
#     "email": "venomtxt@gmail.com",
#     "password": "123141241.1nfiuaoda"
# }
#
# mask_payload = mask_data(payload)
# print(f"Изначальный payload: {payload}")
# print(f"Замаскированный payload: {mask_payload}")