 How to Run
------------

1. Open "api/settings.py" and configure MySQL settings.
2. Go to "api" folder and run the following command:
```
python runner.py
```


 HTTP API Documentation
-----------------------------

##**Creation APIs**

###  **Post Article**
```
http://<ip>:<port>/article/add
```
##### **POST**

*Request*

```
curl -i -H "Content-Type: application/json" -X POST -d '{"title": "test", "content": "Hey there\n\nHow are you?"}' "http://<ip>:<port>/article/add"
```

*Response*

```
{
    "admin_error": "Admin access required to post an article!"
}
```

*Request*

```
curl -i -H "Content-Type: application/json" -H "Authorization: Token dGVzdGVyOnZvaWxh" -X POST -d '{"title": "test", "content": "Hey there\n\nHow are you?"}' "http://<ip>:<port>/article/add"
```

*Response*
```
{
    "detail": "OK"
}
```

###  **Post Comment**

```    
http://<ip>:<port>/article/paragraph/<paragraph_id>/comment
```

##### **POST with User**
    
*Request*

```    
curl -i -H "Content-Type: application/json" -X POST  -d '{"text": "Hello!"}' "http://<ip>:<port>/article/paragraph/1/comment"
```

*Response*
```
{
    "detail": "OK"
}
```

##### **POST with Admin**
    
*Request*

```    
curl -i -H "Content-Type: application/json" -H "Authorization: Token dGVzdGVyOnZvaWxh"  -X POST  -d '{"text": "Hello!"}' "http://<ip>:<port>/article/paragraph/1/comment"
```

*Response*
```
{
    "detail": "OK"
}
```


##**Display APIs**

###  **Display Article List**
```
http://<ip>:<port>/article/list?start=<start_point_for_display>&count=<count_of_articles_to_show>
```
##### **GET**

*Request*

```    
curl -i -H "Content-Type: application/json" -X GET "http://<ip>:<port>/article/list?start=0&count=10"
```

*Response*
```
{
    "results": [
                {
                    "id": 1,
                    "title": "test"
                },
                ...
                ]
}
```

###  **Display Article Content**
```
http://<ip>:<port>/article/<article_id>
```
##### **GET**

*Request*

```    
curl -i -H "Content-Type: application/json" -X GET "http://<ip>:<port>/article/1"
```

*Response*
```
{
    "results": [
                {
                    "id": "4",
                    "title": "test"
                    "paragraphs": [
                                    {
                                        "text": "Hey there",
                                        "id": 6,
                                        "paragraph_number": 1,
                                        "comments": [
                                                    {
                                                        "text": "Hello!",
                                                        "id": 1
                                                    }
                                                ]
                                    },
                                    {
                                        "text": "How are you?",
                                        "id": 7,
                                        "paragraph_number": 2,
                                        "comments": [
                                                    {
                                                        "text": "abc!",
                                                        "id": 4
                                                    }
                                                ]
                                    }
                                ]
                }
        ]
}
```


##**Deletion APIs**

###  **Delete Comment**
```
http://<ip>:<port>/article/comment/<comment_id>
```
##### **DELETE**

*Request*

```    
curl -i -H "Content-Type: application/json" -X DELETE "http://<ip>:<port>/article/comment/1"
```

*Response*
```
{
    "admin_error": "Admin access required to delete an article!"
}
```

*Request*

```    
curl -i -H "Content-Type: application/json" -H "Authorization: Token dGVzdGVyOnZvaWxh" -X DELETE "http://<ip>:<port>/article/comment/1"
```

*Response*
```
{
    "detail": "OK"
}
```

###  **Delete Article**
```
http://<ip>:<port>/article/1
```
##### **DELETE**

*Request*

```    
curl -i -H "Content-Type: application/json" -H "Authorization: Token dGVzdGVyOnZvaWxh" -X DELETE "http://<ip>:<port>/article/1"
```

*Response*
```
{
    "detail": "OK"
}
```


##**Admin APIs**

###  **Create Admin**
```
http://<ip>:<port>/admin/add
```
##### **POST**

*Request*

```    
curl -i -H "Content-Type: application/json" -X POST -d '{"username": "abc", "password": "def"}' "http://<ip>:<port>/admin/add"
```

*Response*
```
{
    "admin_error": "Admin access required to make another admin!"
}
```

*Request*

```    
curl -i -H "Content-Type: application/json" -H "Authorization: Token dGVzdGVyOnZvaWxh" -X POST -d '{"username": "abc", "password": "def"}' "http://<ip>:<port>/admin/add"
```

*Response*
```
{
    "detail": "OK"
}
```