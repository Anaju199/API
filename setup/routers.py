class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'rl':
            return 'db_ipbregiaoleste'
        # elif model._meta.app_label == 'app2':
        #     return 'tertiary'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'rl':
            return 'db_ipbregiaoleste'
        # elif model._meta.app_label == 'app2':
        #     return 'tertiary'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = self.db_for_read(obj1)
        db_obj2 = self.db_for_read(obj2)
        return db_obj1 == db_obj2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'rl':
            return db == 'db_ipbregiaoleste'
        # elif app_label == 'app2':
        #     return db == 'tertiary'
        return db == 'default'
