from django.db import models

# Create your models here.
class Adj(models.Model):
    adjString=models.CharField(max_length=10000)
    def __str__(self):
        return self.adjString

class Node(models.Model):
    nodeString = models.CharField(max_length=10000)
    def __str__(self):
        return self.nodeString

class RawData(models.Model):
    rawdata=models.CharField(max_length=5000)
    def __str__(self):
        return self.rawdata