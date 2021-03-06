from django.db import models
from edit.models import Protocol, Action, Event

class Experiment(models.Model):
    time_start = models.DateTimeField()
    time_complete = models.DateTimeField(null=True, blank=True)
    trials_completed = models.IntegerField(default=0)
    total_duration = models.DecimalField(max_digits=8, decimal_places=3,null=True, blank=True)
    name = models.CharField(max_length=255)
    protocol = models.ForeignKey(Protocol)

    def set_trials_completed(self):
        self.trials_completed = Trial.objects.filter(experiment=self,completed=True).count()
    
    def current_trial(self):
        try:
            return Trial.objects.filter(experiment=self,completed=False).order_by('-time_start')[0]
        except IndexError:
            return None

class Trial(models.Model):
    experiment = models.ForeignKey(Experiment)
    time_start = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=8, decimal_places=3,null=True, blank=True)
    completed = models.BooleanField(default=False)

class Happening(models.Model):
    experiment = models.ForeignKey(Experiment)
    time_occurred = models.DecimalField(max_digits=8, decimal_places=3,null=True, blank=True)
    type = models.CharField(max_length=3, choices=(('ACT','Action Occurred'),('EVT','Event Occurred'),('ITL','Interval Start'),('TRL','Trial Start'),('MRK','Mark Point')) )
    description = models.TextField(default='',blank=True)
    broadcast = models.BooleanField(default=False)
    write_on = models.DateTimeField(auto_now=True)
    keyname = models.CharField(max_length=100, default='',blank=True)
    
class RuntimeCache(models.Model):
    experiment = models.OneToOneField(Experiment,null=True,blank=True)
    experiment_terminate = models.BooleanField(default=False)
    happening_ids = models.TextField(blank=True,default='')
    interval_start = models.DateTimeField(null=True, blank=True)
    
class EmulateAction(models.Model):
    experiment = models.ForeignKey(Experiment)
    time_occurred = models.DecimalField(max_digits=8, decimal_places=3,null=True, blank=True)
    action = models.ForeignKey(Action)
    
class SimEvent(models.Model):
    experiment = models.ForeignKey(Experiment)
    time_occurred = models.DecimalField(max_digits=8, decimal_places=3,null=True, blank=True)
    eventid = models.IntegerField(default=0)    