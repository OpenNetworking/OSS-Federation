class BaseIssuerRouter(object):
    """
    A router to control all database operations on models in the
    member application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read member models go to website.
        """
        if model._meta.app_label == 'baseissuer':
            return 'website'
        return None
    def db_for_write(self, model, **hints):
        """
        Attempts to write member models go to website.
        """
        if model._meta.app_label == 'baseissuer':
            return 'website'
        return None
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the member app is involved.
        """
        if (obj1._meta.app_label == 'baseissuer' or
            obj2._meta.app_label == 'baseissuer'):
                return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the member app only appears in the 'website'
        database.
        """
        if db == 'website':
             return model._meta.app_label == 'baseissuer'
        elif model._meta.app_label == 'baseissuer':
             return False
        return None

