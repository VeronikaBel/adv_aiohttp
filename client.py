#примеры запросов

import requests

# response = requests.post(
#     "http://localhost:8080/ads",
# json = {"title": "adv_1", "description": "new test advertisment", "owner_id": "1"}
# )

# print(response.status_code)
# print(response.text)


# response = requests.get(
#     "http://localhost:8080/ads/1",
    
# )

# print(response.status_code)
# print(response.text)

# response = requests.delete(
#     "http://localhost:8080/ads/1")

# print(response.status_code)
# print(response.text)


response = requests.patch(
    "http://localhost:8080/ads/1", json={"title": "Updated title"})

print(response.status_code)
print(response.text)
