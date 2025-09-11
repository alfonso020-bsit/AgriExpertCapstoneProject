from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserBase(models.Model):
    ROLE_CHOICES = [
        ('Magsasaka', 'Magsasaka'),
        ('Eksperto', 'Eksperto'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    barangay = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    profile_picture = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Magsasaka')

    class Meta:
        abstract = True  # This ensures it is inherited properly

    def __str__(self):
        return f"{self.username} ({self.role})"

class Farmer(UserBase):
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Lawak ng Sakahan (Hectares)")

    class Meta:
        db_table = "AgriExpert_farmer" 
        
class Expert(UserBase):
    proof_of_expertise = models.URLField(blank=True, null=True)
    license_number = models.CharField(max_length=50)
    position = models.CharField(max_length=255, blank=True, null=True)
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    
    class Meta:
        db_table = "AgriExpert_expert"

class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    organization = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Store hashed password

    def __str__(self):
        return f"{self.username} ({self.position})"


class Message(models.Model):
    sender_farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="sent_messages_farmer", blank=True, null=True)
    sender_expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="sent_messages_expert", blank=True, null=True)
    receiver_farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="received_messages_farmer", blank=True, null=True)
    receiver_expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name="received_messages_expert", blank=True, null=True)
    message_text = models.TextField()
    image = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, null=False)
    is_solved = models.BooleanField(default=False, null=False)
    solution_description = models.TextField(blank=True, null=True)
    
    CLASSIFICATION_CHOICES = [
        ('Sakit', 'Sakit (Disease)'),
        ('Peste', 'Peste (Pest)'),
    ]
    classification = models.CharField(max_length=10, choices=CLASSIFICATION_CHOICES, blank=True, null=True)
    
    class Meta:
        db_table = "AgriExpert_messages"

    def __str__(self):
        sender = self.sender_farmer or self.sender_expert
        receiver = self.receiver_farmer or self.receiver_expert
        return f"Message from {sender.first_name} to {receiver.first_name} at {self.timestamp}"


class ExpertPost(models.Model):
    expert = models.ForeignKey('Expert', on_delete=models.CASCADE)  # Link to the expert user
    title = models.CharField(max_length=255)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_images(self):
        return ExpertPostImage.objects.filter(post=self)

    def get_upvotes_count(self):
        return Upvote.objects.filter(post=self).count()

    def get_comments(self):
        return Comment.objects.filter(post=self).order_by('-created_at')

    def has_upvoted(self, user):
        return Upvote.objects.filter(post=self, expert=user).exists()

class ExpertPostImage(models.Model):
    post = models.ForeignKey(ExpertPost, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()  # The Supabase URL
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.post.title}"

class Upvote(models.Model):
    post = models.ForeignKey(ExpertPost, on_delete=models.CASCADE)
    expert = models.ForeignKey('Expert', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'expert']

    def __str__(self):
        return f"Upvote by {self.expert.username} on post {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(ExpertPost, on_delete=models.CASCADE)
    expert = models.ForeignKey('Expert', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_solution = models.BooleanField(default=False)  # Mark this comment as the solution
    solution_highlighted = models.BooleanField(default=False)  # Solution Highlighted

    def __str__(self):
        return f"Comment by {self.expert.username} on {self.post.title}"

    def mark_as_solution(self):
        """Marks this comment as the solution to the post."""
        self.is_solution = True
        self.solution_highlighted = True
        self.save()

    class Meta:
        ordering = ['-created_at']  # Show newest comments first

class Library(models.Model):
    paksa = models.TextField()
    deskripsyon = models.TextField()
    ano_ang_nagagawa_nito = models.TextField()
    bakit_at_saan_ito_nangyayari = models.TextField()
    paano_ito_matutukoy = models.TextField()
    bakit_ito_mahalaga = models.TextField()
    paano_ito_pangangasiwaan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.paksa

class PredictionHistory(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)  # Link to Magsasaka
    image_url = models.URLField(null=True, blank=True)
    predicted_class = models.CharField(max_length=255)
    confidence = models.FloatField()
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "AgriExpert_prediction_history"  # Explicit table name

    def __str__(self):
        return f"{self.farmer.username} - {self.predicted_class} ({self.confidence}%)"


class FarmerPost(models.Model):
    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE)  # Link to the farmer user
    title = models.CharField(max_length=255)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_images(self):
        return FarmerPostImage.objects.filter(post=self)

    def get_upvotes_count(self):
        return FarmerUpvote.objects.filter(post=self).count()

    def get_comments(self):
        return FarmerPostComment.objects.filter(post=self).order_by('-created_at')

    def has_upvoted(self, user):
        # Check if the user has upvoted based on user type
        if hasattr(user, 'farmer'):
            return FarmerUpvote.objects.filter(post=self, farmer=user.farmer).exists()
        elif hasattr(user, 'expert'):
            return FarmerUpvote.objects.filter(post=self, expert=user.expert).exists()
        return False



class FarmerPostImage(models.Model):
    post = models.ForeignKey(FarmerPost, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()  # The Supabase URL
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.post.title}"


class FarmerUpvote(models.Model):
    post = models.ForeignKey(FarmerPost, on_delete=models.CASCADE)
    # Allow either a farmer or an expert to upvote (but not both)
    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE, null=True, blank=True)
    expert = models.ForeignKey('Expert', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Ensure that exactly one of farmer or expert is set
            models.CheckConstraint(
                check=(
                    models.Q(farmer__isnull=False, expert__isnull=True) | 
                    models.Q(farmer__isnull=True, expert__isnull=False)
                ),
                name='farmer_or_expert_upvote'
            ),
            # Ensure unique upvotes from farmers
            models.UniqueConstraint(
                fields=['post', 'farmer'],
                condition=models.Q(farmer__isnull=False),
                name='unique_farmer_upvote'
            ),
            # Ensure unique upvotes from experts
            models.UniqueConstraint(
                fields=['post', 'expert'],
                condition=models.Q(expert__isnull=False),
                name='unique_expert_upvote'
            )
        ]

    def __str__(self):
        if self.farmer:
            return f"Upvote by farmer {self.farmer} on post {self.post.title}"
        else:
            return f"Upvote by expert {self.expert} on post {self.post.title}"


class FarmerPostComment(models.Model):
    post = models.ForeignKey(FarmerPost, on_delete=models.CASCADE)
    # Allow either farmer or expert to comment
    farmer = models.ForeignKey('Farmer', on_delete=models.CASCADE, null=True, blank=True)
    expert = models.ForeignKey('Expert', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_solution = models.BooleanField(default=False)  # Mark this comment as the solution
    solution_highlighted = models.BooleanField(default=False)  # Solution Highlighted

    class Meta:
        ordering = ['-created_at']
        constraints = [
            # Ensure that exactly one of farmer or expert is set
            models.CheckConstraint(
                check=(
                    models.Q(farmer__isnull=False, expert__isnull=True) | 
                    models.Q(farmer__isnull=True, expert__isnull=False)
                ),
                name='farmer_or_expert_comment'
            )
        ]

    def __str__(self):
        if self.farmer:
            return f"Comment by farmer {self.farmer} on {self.post.title}"
        else:
            return f"Comment by expert {self.expert} on {self.post.title}"

    def mark_as_solution(self):
        """Marks this comment as the solution to the post."""
        # First, unmark any existing solutions for this post
        FarmerPostComment.objects.filter(post=self.post, is_solution=True).update(is_solution=False)
        # Now mark this comment as the solution
        self.is_solution = True
        self.solution_highlighted = True
        self.save()
    
    @property
    def commenter_name(self):
        """Returns the name of the commenter, whether farmer or expert."""
        return self.farmer.username if self.farmer else self.expert.username
    
    @property
    def commenter_type(self):
        """Returns the type of commenter ('farmer' or 'expert')."""
        return 'farmer' if self.farmer else 'expert'