from pymongo import MongoClient

client = MongoClient('3.10.213.78', 7077)
mongo_base = client.instagram
collection = mongo_base['instapars']



print('В базе находются данные по следующем пользователям')
for key, val in enumerate(collection.distinct('username')):
    print(key, val)
username = collection.distinct('username')[int(input('Введите номер нужного пользователя:'))]
print(f"У пользователя {username}: {collection.count_documents({'username': username, 'follow_by': True})} подписчиков, Подписан на {collection.count_documents({'username': username, 'follow_by': False})} ")
choose = input(f"1.Подписчики\n2.Подписан\n(1,2):")

if choose == '1':
    for follower in collection.find({"username": username, "follow_by":True}):
        print(f"{follower['follower_username']} | {follower['follower_full_name']}")
else:
    for follow in collection.find({"username": username, "follow_by":False}):
        print(f"{follow['follower_username']} | {follow['follower_full_name']}")
