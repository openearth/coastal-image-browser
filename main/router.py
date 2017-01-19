from main import settings


class PrimaryReplicaRouter(object):

    def db_for_read(self, model, **hints):
        """
        Reads go to a either the database named like the app_label or to default
        """
        if model._meta.app_label in settings.DATABASES:
            return model._meta.app_label
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        """
        Writes go to a either the database named like the app_label or to default
        """
        if model._meta.app_label in settings.DATABASES:
            return model._meta.app_label
        else:
            return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Only migrations on default are allowed.
        """
        if db == 'default':
            return True
        else:
            return False