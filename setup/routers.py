class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'rl':
            return 'db_ipbregiaoleste'
        elif model._meta.app_label == 'hom':
            return 'db_homol'
        elif model._meta.app_label == 'ch':
            return 'db_casarohr'
        # elif model._meta.app_label == 'proacos':
        #     return 'db_proacos'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'rl':
            return 'db_ipbregiaoleste'
        elif model._meta.app_label == 'hom':
            return 'db_homol'
        elif model._meta.app_label == 'ch':
            return 'db_casarohr'
        # elif model._meta.app_label == 'proacos':
        #     return 'db_proacos'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        db_obj1 = obj1._state.db
        db_obj2 = obj2._state.db
        # # Allow relations if both models are from the same database
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'rl':
            return db == 'db_ipbregiaoleste'
        elif app_label == 'hom':
            return db == 'db_homol'
        elif app_label == 'ch':
            return db == 'db_casarohr'
        # elif app_label == 'proacos':
        #     return 'db_proacos'
        return db == 'default'
