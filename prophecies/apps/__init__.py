from django.apps import AppConfig

class PropheciesConfig(AppConfig):
    name = 'prophecies.core'

    def ready(self):
        from actstream import registry 
        from django.contrib.auth.models import User
        self.register_action()
        registry.register(User)
        registry.register(self.get_model('Choice'))
        registry.register(self.get_model('Task'))
        registry.register(self.get_model('TaskRecord'))
        registry.register(self.get_model('TaskRecordReview'))
        registry.register(self.get_model('Tip'))
    
    def register_action(self):
        from actstream import registry 
        from actstream.models import Action
        from django.db.models import signals

        registry.register(Action)        

        signals.post_save.connect(create_aggregate_on_action_save, sender=Action)

def create_aggregate_on_action_save(sender, instance, **kwargs):
        
    if(instance.actor_content_type.model == 'user'):
        from prophecies.core.models import ActionAggregation
        action_agg, _created = ActionAggregation.objects.get_or_create(verb = instance.verb, date=instance.timestamp, actor_id = instance.actor_object_id)
        action_agg.count += 1
        action_agg.save()