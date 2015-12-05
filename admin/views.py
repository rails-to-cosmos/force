from flask_admin.contrib.mongoengine import ModelView
from flask_security import current_user
# from flask_admin import expose, BaseView
# from user.models import User


class UserView(ModelView):
    column_list = ['created_at',
                   'email',
                   'active',
                   'confirmed_at',
                   'last_login_at',
                   'roles']
    form_columns = ['email', 'roles']

    def is_accessible(self):
        return current_user.has_role('admin')


class RoleView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class ProductView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class MenuView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class MenuProductView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class OrderView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class CategoryView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class UserDocumentView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class ProductPositionsInXLSView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')
