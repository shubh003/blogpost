import re

# URLs Regex
# Display
ARTICLE_LIST_DISPLAY = re.compile('^/article/list')
ARTICLE_CONTENT_DISPLAY = re.compile('^/article/(?P<article_id>[0-9]+)')

# Create
ADMIN_CREATE = re.compile('^/admin/add')
ARTICLE_CREATE = re.compile('^/article/add')
COMMENT_CREATE = re.compile('^/article/paragraph/(?P<paragraph_id>[0-9]+)/comment')

# Delete
ARTICLE_DELETE = re.compile('^/article/(?P<article_id>[0-9]+)')
COMMENT_DELETE = re.compile('^/article/comment/(?P<comment_id>[0-9]+)')