import piheaan as heaan
from piheaan.math import approx  # for piheaan math function
import os
import math

# set parameter
params = heaan.ParameterPreset.FGb
context = heaan.make_context(params)  # context has paramter information
heaan.make_bootstrappable(context)  # make parameter bootstrapable

# create and save keys
key_file_path = "./keys"
sk = heaan.SecretKey(context)  # create secret key
os.makedirs(key_file_path, mode=0o775, exist_ok=True)
sk.save(key_file_path + "/secretkey.bin")  # save secret key

key_generator = heaan.KeyGenerator(context, sk)  # create public key
key_generator.gen_common_keys()
key_generator.save(key_file_path + "/")  # save public key

log_slots = 12
num_slots = 2 ** log_slots

# load secret key and public key
# When a key is created, it can be used again to save a new key without creating a new one
key_file_path = "./keys"

sk = heaan.SecretKey(context, key_file_path + "/secretkey.bin")  # load secret key
pk = heaan.KeyPack(context, key_file_path + "/")  # load public key
pk.load_enc_key()
pk.load_mult_key()

eval = heaan.HomEvaluator(context, pk)  # to load piheaan basic function
dec = heaan.Decryptor(context)  # for decrypt
enc = heaan.Encryptor(context)  # for encrypt

from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("beomi/kcbert-base")
model = AutoModel.from_pretrained("beomi/kcbert-base")

happy_words = ['기쁘다', '즐겁다', '행복하다', '환희', '기쁨']
sad_words = ['슬프다', '우울하다', '서글프다', '애처롭다', '비통', '슬픔']
angry_words = ['짜증', '화나다', '분노', '분해하다', '격노', '노여움', '분노', '화']

happy_embeddings = []
sad_embeddings = []
angry_embeddings = []

sentiment_embedding = [0] * 4096

# 각 단어의 벡터를 계산합니다.
for word in happy_words:
    tokens = tokenizer(word, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        model_output = model(**tokens)[0]
    embedding = torch.mean(model_output, dim=1).squeeze()
    happy_embeddings.append(embedding)
happy_embedding = torch.mean(torch.stack(happy_embeddings), dim=0)

happy_embedding_list = happy_embedding.tolist()
for i in range(len(happy_embedding_list)):
    sentiment_embedding[i] = happy_embedding_list[i]
    sentiment_embedding[3072 + i] = happy_embedding_list[i]

for word in sad_words:
    tokens = tokenizer(word, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        model_output = model(**tokens)[0]
    embedding = torch.mean(model_output, dim=1).squeeze()
    sad_embeddings.append(embedding)
sad_embedding = torch.mean(torch.stack(sad_embeddings), dim=0)

sad_embedding_list = sad_embedding.tolist()
for i in range(len(sad_embedding_list)):
    sentiment_embedding[1024 + i] = sad_embedding_list[i]

for word in angry_words:
    tokens = tokenizer(word, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        model_output = model(**tokens)[0]
    embedding = torch.mean(model_output, dim=1).squeeze()
    angry_embeddings.append(embedding)
angry_embedding = torch.mean(torch.stack(angry_embeddings), dim=0)

angry_embedding_list = angry_embedding.tolist()
for i in range(len(angry_embedding_list)):
    sentiment_embedding[2048 + i] = angry_embedding_list[i]

sentiment_magnitude_message = heaan.Message(log_slots)

# happy
sentiment_magnitude_message[0] = math.sqrt(sum([sentiment_embedding[i] ** 2 for i in range(1024)]))
sentiment_magnitude_message[3072] = math.sqrt(sum([sentiment_embedding[i] ** 2 for i in range(3072, 4096)]))

# sad
sentiment_magnitude_message[1024] = math.sqrt(sum([sentiment_embedding[i] ** 2 for i in range(1024, 2048)]))

# angry
sentiment_magnitude_message[2048] = math.sqrt(sum([sentiment_embedding[i] ** 2 for i in range(2048, 3072)]))

sentiment_embedding_message = heaan.Message(log_slots)

for i in range(len(sentiment_embedding)):
    sentiment_embedding_message[i] = sentiment_embedding[i]

clear_100 = heaan.Message(log_slots)
clear_100[0] = 100
clear_100[1024] = 100
clear_100[2048] = 100
clear_100[3072] = 100

clear_1 = heaan.Message(log_slots)
clear_1[0] = 1
clear_1[1024] = 1
clear_1[2048] = 1
clear_1[3072] = 1

clear_0001 = heaan.Message(log_slots)
clear_0001[0] = 0.0001
clear_0001[1024] = 0.0001
clear_0001[2048] = 0.0001
clear_0001[3072] = 0.0001

result_check = heaan.Message(log_slots)
result_check[0] = 1
result_check[1024] = 2
result_check[2048] = 2


def cosine_similarity_with_HE(arg0):  # arg0 = enc(user_input)
    arg1, sentiment_magnitude = sentiment_embedding_message, sentiment_magnitude_message

    # copy of input message
    eval.rot_sum([arg0, arg0, arg0, arg0], [0, 1024, 2048, 3072], arg0)

    # dot product of arg0, arg1
    dot_product = heaan.Ciphertext(context)

    # multiplication each cell of arg0 and arg1
    eval.mult(arg0, arg1, dot_product)

    # sum of result of multiplication
    # left_rotate_reduce
    for i in range(log_slots - 3, -1, -1):  # 1024 가 하나의 Sentiment
        eval.rot_sum([dot_product, dot_product], [0, 2 ** i], dot_product)
    eval.mult(dot_product, clear_1, dot_product)

    # magnitude of input message
    eval.square(arg0, arg0)
    for i in range(log_slots - 3, -1, -1):
        eval.rot_sum([arg0, arg0], [0, 2 ** i], arg0)
    eval.mult(arg0, clear_0001, arg0)  # clear with 0.0001 (scailing for square root)

    approx.sqrt(eval, arg0, arg0)
    # recover value
    eval.mult(arg0, clear_100, arg0)

    # magnitude * magnitude
    cosine_similarities = heaan.Ciphertext(context)
    eval.mult(arg0, sentiment_magnitude, cosine_similarities)

    # dot_product / (magnitude1 * magnitude2)
    approx.inverse(eval, cosine_similarities, cosine_similarities)

    eval.bootstrap(cosine_similarities, cosine_similarities)

    eval.mult(dot_product, cosine_similarities, cosine_similarities)

    return cosine_similarities


def compare_and_get_result(cosine_similarities):
    test_result = heaan.Message(log_slots)
    dec.decrypt(cosine_similarities, sk, test_result)

    temp_cosine_similarities = heaan.Ciphertext(context)
    eval.left_rotate(cosine_similarities, 1024, temp_cosine_similarities)

    approx.compare(eval, cosine_similarities, temp_cosine_similarities, cosine_similarities)

    eval.mult(cosine_similarities, result_check, cosine_similarities)

    return cosine_similarities


def sentiment_classify(sentence):
    tokens = tokenizer(sentence, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        model_output = model(**tokens)[0]
    embedding = torch.mean(model_output, dim=1).squeeze().tolist()
    embedding_message = heaan.Message(log_slots)
    for i in range(len(embedding)):
        embedding_message[i] = embedding[i]

    # encrypt input message embedding
    embedding_ciphertext = heaan.Ciphertext(context)
    enc.encrypt(embedding_message, pk, embedding_ciphertext)

    result = cosine_similarity_with_HE(embedding_ciphertext)

    result = compare_and_get_result(result)

    result_message = heaan.Message(log_slots)
    dec.decrypt(result, sk, result_message)

    happy = round(result_message[0].real)
    sad = round(result_message[1024].real)
    angry = round(result_message[2048].real)

    if (happy == 1 and angry == 0):
        return "happy"
    elif (happy == 0 and sad == 2):
        return "sad"
    elif (happy == 1 and angry == 2) or (happy == 0 and sad == 0):
        return "angry"
