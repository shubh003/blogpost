import urls

# Server Settings
PORT_NUMBER = 8080

# MySQL settings

MYSQL_HOST = '0.0.0.0' # host
MYSQL_USER = 'temp' # user
MYSQL_PASSWORD = 'temp123' # password
MYSQL_DB = 'test' # database

## Do not alter any variables below this
# URL Mapping
GET_URL_MAPPER = {
            urls.ARTICLE_LIST_DISPLAY : 'article_list_display',
            urls.ARTICLE_CONTENT_DISPLAY : 'article_content_display'
}

POST_URL_MAPPER = {
			urls.ADMIN_CREATE : 'admin_create',
            urls.ARTICLE_CREATE : 'article_create',
            urls.COMMENT_CREATE : 'comment_create'
}

DELETE_URL_MAPPER = {
            urls.ARTICLE_DELETE : 'article_delete',
            urls.COMMENT_DELETE : 'comment_delete'
}

# Authentication
USERNAME = 'tester'
PASSWORD = 'voila'