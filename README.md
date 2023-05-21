# Emotional Analysis of Sentences with Homomorphic Encryption

<div align="center" width="100px">
    <strong>Contributors</strong>
    <p style="height: 10px"></p>
    <p style="justify-content: space-between">
        <a href = "https://github.com/yuseogi0218">
          <img src = "https://avatars.githubusercontent.com/u/64399505?v=4" width=35px/>
        </a>
        <a href = "https://github.com/yoouung" >
          <img src = "https://avatars.githubusercontent.com/u/78146904?v=4" width=35px/>
        </a>
        <a href = "https://github.com/Younggeun97" >
          <img src = "https://avatars.githubusercontent.com/u/94732122?v=4" width=35px/>
        </a>
    </p>
</div>

## Introduction
### Idea Proposal
- A service that records a one-sentence diary on a web service and provides emotional analysis
results of its contents  
- It allows user to check user’s feelings about records for a long term by analyzing his/her own
diary posted on the web service  
### Utilization
- for personal users, users can protect their personal information and to understand and
manage their emotional state.
### [Usage of Homomorphic Encryption](https://github.com/yuseogi0218/sentiment_classification_with_HE/blob/main/sentiment_diary/diary/sentiment_classification.py)
- The service encrypts user's diary in web service using a homomorphic encryption because diaries are sensitive personal information
- It is used to protect user’s records within the emotional analysis service.

<br/>

## Environment Settings
Make sure Python is installed on your machine.   
Also, it assumes that the version of python is `3.9` 

1. Create and Activate virtual environment
```shell
% python -m venv .venv
% source .venv/bin/activate
```

2. Upgrade pip
```shell
% (.venv) pip install --upgrade pip
```
3. Install Django framework
```shell
% (.venv) pip install django
```

4. Change directory and install modules required
```shell
% (.venv) cd sentiment_diary
% (.venv) pip install pi-heaan
% (.venv) pip install transformers
% (.venv) pip install torch
```

5. Start local server
```shell
% (.venv) python manage.py runserver
```
<br/>

## How to use
1. Open Chrome and Access to `localhost:8000/common`.
2. Signup with `회원가입` button.
3. You can use diary with your account !
