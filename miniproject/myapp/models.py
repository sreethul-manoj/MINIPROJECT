from django.db import models

class Signup(models.Model):  
    fullname = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return self.email

class Complaint(models.Model):
    
    COMPLAINT_TYPES = [
        ('waste_dumping', 'Waste Dumping'),
        ('public_nuisance', 'Public Nuisance'),
        ('traffic_violations', 'Traffic Violations'),
        ('water_leakage', 'Water Leakage'),
        ('street_light', 'Street Light Issue'),
        ('noise_pollution', 'Noise Pollution'),
        ('illegal_construction', 'Illegal Construction'),
        ('stray_animals', 'Stray Animals'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    description = models.TextField()
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_TYPES)
    location = models.CharField(max_length=255)
    proof = models.FileField(upload_to='media/image', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # ✅ Add this line:
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.complaint_type}"
    

    


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    suggestion = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"
    

class User(models.Model):
    Name=models.CharField(max_length=50)
    Email=models.CharField(max_length=50)
    Mobile_number=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.Name} - {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

