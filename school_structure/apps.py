from django.apps import AppConfig


class SchoolStructureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school_structure'
    
    def ready(self):
        import school_structure.signals
