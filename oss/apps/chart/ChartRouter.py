class ChartRouter(object):
    """
    A router to control all database operations on models in the
        chart application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read chart models go to chart_db.
        """
        if model._meta.app_label == 'chart':
            return 'chart_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write chart models go to chart_db.
        """ 
        if model._meta.app_label == 'chart':
            return 'chart_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the chart app is involved.
        """ 
        if obj1._meta.app_label == 'chart' or \
            obj2._meta.app_label == 'chart':
            return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the chart app only appears in the 'chart_db'
        database.
        """
         
        if db == 'chart_db':
            return model._meta.app_label == 'chart'
        elif model._meta.app_label == 'chart':
            return False
        return None
