from django.db import models

# ----------------------
# User Table
# ----------------------

class User(models.Model):
    user_id = models.CharField(max_length=8, primary_key=True)  # Primary key
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11, unique=True)  # Phone number is unique
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    is_admin = models.BooleanField()
    verification_status = models.CharField(max_length=20, choices=[('Verified', 'Verified'), ('Pending', 'Pending')])

    def __str__(self):
        return self.name


# ----------------------
# Service Table
# ----------------------

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)  # Primary key
    route_name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    pickup = models.CharField(max_length=100)
    dropoff = models.CharField(max_length=100)
    bus_id = models.IntegerField(null=True, blank=True)
    carpool_id = models.IntegerField(null=True, blank=True)
    vehicle_type = models.CharField(max_length=50)
    all_possible_pickup_location = models.CharField(max_length=255)
    frequency = models.CharField(max_length=50)
    stoppage = models.CharField(max_length=255)
    available_time = models.CharField(max_length=50)
    service_type = models.CharField(max_length=50, choices=[('Bus', 'Bus'), ('Carpool', 'Carpool'), ('Public Transport', 'Public Transport')])

    def __str__(self):
        return self.route_name


# ----------------------
# Driver Table
# ----------------------

class Driver(models.Model):
    license_no = models.CharField(max_length=20, primary_key=True)  # Primary key
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Foreign key to Service
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    schedule = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ----------------------
# Takes Table
# ----------------------

class Takes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Foreign key to Service
    date_taken = models.DateField()
    time_taken = models.TimeField()

    class Meta:
        unique_together = ('user', 'service')  # Composite primary key (user_id, service_id)

    def __str__(self):
        return f"{self.user.name} takes {self.service.route_name}"


# ----------------------
# Booking Table
# ----------------------

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)  # Primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Foreign key to Service
    route_id = models.IntegerField()  # Related to route in Service
    seat_no = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    seat_availability = models.CharField(max_length=20)

    def __str__(self):
        return f"Booking {self.booking_id} for {self.name}"


# ----------------------
# LostFound Table
# ----------------------

class LostFound(models.Model):
    item_id = models.AutoField(primary_key=True)  # Primary key
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Foreign key to Service
    reporter_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    found = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    lost = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    location_reported = models.CharField(max_length=100)
    date_reported = models.DateField()
    reporter_contact = models.CharField(max_length=11)
    item_details = models.CharField(max_length=255)

    def __str__(self):
        return self.item_name


# ----------------------
# Incident Table
# ----------------------

class Incident(models.Model):
    incident_id = models.AutoField(primary_key=True)  # Primary key
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Foreign key to Service
    location = models.CharField(max_length=100)
    reporter_name = models.CharField(max_length=100)
    reporter_contact = models.CharField(max_length=11)
    incident_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# ----------------------
# Feedback Table
# ----------------------

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)  # Primary key
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Foreign key to Service
    ratings = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Ratings between 1 and 5
    comment = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"Feedback {self.feedback_id}"


# ----------------------
# OTP Table
# ----------------------

class OTP(models.Model):
    otp_id = models.AutoField(primary_key=True)  # Primary key
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  # Foreign key to Booking
    code = models.CharField(max_length=6)
    status = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"OTP {self.otp_id}"


# ----------------------
# Notification Table
# ----------------------

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)  # Primary key
    send_time = models.DateTimeField()
    receive_time = models.DateTimeField()
    message = models.CharField(max_length=255)

    def __str__(self):
        return f"Notification {self.notification_id}"
