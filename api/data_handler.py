from hashlib import md5
from base64 import b64encode
from datetime import datetime

from storage import MySQL
from settings import USERNAME, PASSWORD

class DataHandler(object):

    # Get Authorized Admin
    Q_ADMIN_GET = """SELECT user_id, token FROM auth_admin"""
    Q_ADMIN_INSERT = """INSERT INTO auth_admin (username, password, user_id, token) VALUES ('%s', '%s', '%s', '%s')"""

    # Get Queries
    Q_ARTICLE_LIST_DISPLAY = """SELECT id, title FROM articles_title LIMIT %s, %s"""

    Q_ARTICLE_DISPLAY = """SELECT id, title FROM articles_title WHERE id=%s"""
    Q_PARAGRAPH_DISPLAY = """SELECT id, paragraph_number, text FROM articles_content WHERE article_id=%s ORDER BY paragraph_number"""
    Q_COMMENT_DISPLAY = """SELECT id, paragraph_id, text FROM articles_comment WHERE paragraph_id IN (%s)"""

    # Create Queries
    Q_ARTICLE_CREATE = """INSERT INTO articles_title (title) VALUES ('%s')"""
    Q_PARAGRAPH_CREATE = """INSERT INTO articles_content (article_id, paragraph_number, text) VALUES (%s, %s, '%s')
                            ON DUPLICATE KEY UPDATE text=VALUES(text)"""
    Q_COMMENT_CREATE = """INSERT INTO articles_comment (paragraph_id, text) VALUES (%s, '%s')"""

    # Delete Queries
    Q_ARTICLE_DELETE = """DELETE FROM articles_title WHERE id=%s"""
    Q_PARAGRAPH_DELETE = """DELETE FROM articles_content WHERE article_id=%s"""
    Q_COMMENT_DELETE = """DELETE FROM articles_comment WHERE paragraph_id IN (SELECT id FROM articles_content WHERE article_id=%s)"""

    Q_COMMENT_ID_DELETE = """DELETE FROM articles_comment WHERE id=%s"""


    def __init__(self):
        self.sql = MySQL()
        self.admin_dict = {}

        self._get_admin_tokens()

    def _get_identifier(self, user_name, password):
        to_hash = '::'.join([str(user_name), str(password)])
        return md5(to_hash).hexdigest()

    def _get_admin_tokens(self):
        admin_list = self.sql._get_query_result_as_list(self.Q_ADMIN_GET)

        # Create Admin dict
        for each in admin_list:
            admin_name = each.get('user_id')
            token = each.get('token')

            self.admin_dict[admin_name] = token

        first_admin_token = b64encode('%s:%s' % (USERNAME, PASSWORD))
        first_admin_identifier = self._get_identifier(USERNAME, PASSWORD)

        if first_admin_token not in self.admin_dict.values():
            q_admin_insert = self.Q_ADMIN_INSERT % (USERNAME, PASSWORD, first_admin_identifier, first_admin_token)

            self.sql.execute_query(q_admin_insert)
            self.sql.conn.commit()

    def _paragraphs_display(self, article_id):
        # Display all paragraphs in article
        q_para_display = self.Q_PARAGRAPH_DISPLAY % (article_id, )
        
        return self.sql._get_query_result_as_list(q_para_display)

    def _comments_display(self, paragraph_list):
        para_str = ','.join([str(paragraph) for paragraph in paragraph_list])

        q_comment_display = self.Q_COMMENT_DISPLAY % (para_str, )
        
        comments_list = self.sql._get_query_result_as_list(q_comment_display)
        comments_dict = {}
        for each in comments_list:
            para_id = each.pop('paragraph_id')

            if para_id not in comments_dict:
                comments_dict[para_id] = []

            comments_dict[para_id].append(each)

        return comments_dict

    def _paragraph_create(self, article_id, content):
        # Segregate paragraphs
        paragraphs = content.split('\n\n')

        # Create paragraphs list withr respective content
        count = 1
        for para in paragraphs:
            q_para_create = self.Q_PARAGRAPH_CREATE % (article_id, count, para)
            self.sql.execute_query(q_para_create)

            count += 1

    def article_list_display(self, start=[], count=[]):
        if start:
            start = start[0]
        else:
            start = 0
        if count:
            count = count[0]
        else:
            count = 5

        # Display articles with given start and count
        q_articles_display = self.Q_ARTICLE_LIST_DISPLAY % (start, count)
        
        return self.sql._get_query_result_as_list(q_articles_display)

    def article_content_display(self, article_id):
        # Get article's title
        q_article_title = self.Q_ARTICLE_DISPLAY % (article_id, )
        title = self.sql._get_query_result_as_list(q_article_title)[0]['title']

        # Get paragraphs
        paragraphs = self._paragraphs_display(article_id)
        paragraph_list = [para.get('id') for para in paragraphs]
        
        # Get Comments
        comments_dict = self._comments_display(paragraph_list)

        # Merge comments with paragraphs
        for i in range(len(paragraphs)):
            para_id = paragraphs[i].get('id')
            paragraphs[i].update({"comments": comments_dict.get(para_id, [])})

        return [{
                "id": article_id,
                "title": title,
                "paragraphs": paragraphs
        }]

    def admin_create(self, username, password, is_admin=False):
        if not is_admin:
            return {"admin_error": "Admin access required to make another admin!"}

        token = b64encode('%s:%s' % (username, password))
        identifier = self._get_identifier(username, password)

        q_admin_insert = self.Q_ADMIN_INSERT % (username, password, identifier, token)
        
        self.sql.execute_query(q_admin_insert)
        self.sql.conn.commit()

        return {"detail": "OK"}

    def article_create(self, title, content, is_admin=False):
        if not is_admin:
            return {"admin_error": "Admin access required to create an article!"}

        q_article_create = self.Q_ARTICLE_CREATE % (title, )
        self.sql.execute_query(q_article_create)

        article_id = self.sql.cursor.lastrowid

        # Create paragraphs in database
        self._paragraph_create(article_id, content)

        self.sql.conn.commit()

        return {"detail": "OK"}

    def comment_create(self, paragraph_id, text, **kwargs):
        q_comment_create = self.Q_COMMENT_CREATE % (paragraph_id, text)
        
        self.sql.execute_query(q_comment_create)
        self.sql.conn.commit()

        return {"detail": "OK"}

    def article_delete(self, article_id, is_admin=False):
        # Delete the article's content in following flow:
        # 1. Delete all the comments related to given article
        # 2. Delete all paragraphs of given article
        # 3. Delete article's title
        if not is_admin:
            return {"admin_error": "Admin access required to delete an article!"}

        q_comment_delete = self.Q_COMMENT_DELETE % (article_id, )
        q_para_delete = self.Q_PARAGRAPH_DELETE % (article_id, )
        q_article_delete = self.Q_ARTICLE_DELETE % (article_id, )

        self.sql.execute_query(q_comment_delete)
        self.sql.execute_query(q_para_delete)
        self.sql.execute_query(q_article_delete)

        self.sql.conn.commit()

        return {"detail": "OK"}

    def comment_delete(self, comment_id, is_admin=False):
        if not is_admin:
            return {"error": "Admin access required to delete a comment!"}

        q_comment_delete = self.Q_COMMENT_ID_DELETE % (comment_id, )

        self.sql.execute_query(q_comment_delete)
        self.sql.conn.commit()

        return {"detail": "OK"}