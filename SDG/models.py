from djongo import models


class Mailing(models.Model):
    id = models.ObjectIdField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    message_text = models.TextField()
    tag = models.CharField(max_length=50)



class Client(models.Model):
    id = models.ObjectIdField()
    phone_number = models.CharField(max_length=12)
    operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)


class Message(models.Model):
    id = models.ObjectIdField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    sending_status = models.CharField(max_length=50)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)


