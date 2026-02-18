from django.db import models
import uuid
import json

class ExtractionTemplate(models.Model):
    """Template defining what fields to extract from documents"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    schema_json = models.JSONField()  # Stores field definitions + rules
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_fields(self):
        """Get fields from schema_json"""
        return self.schema_json.get('fields', [])


class Document(models.Model):
    """Uploaded PDF document"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file_url = models.URLField(max_length=500)  # Cloudinary URL
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title


class ExtractionRun(models.Model):
    """One extraction run per document per template"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('DONE', 'Done'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='extraction_runs')
    template = models.ForeignKey(ExtractionTemplate, on_delete=models.CASCADE, related_name='runs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    extracted_json = models.JSONField(null=True, blank=True)  # The extracted data
    validation_json = models.JSONField(null=True, blank=True)  # Validation errors/warnings
    pushed_at = models.DateTimeField(null=True, blank=True)  # When pushed to CRM
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [['document', 'template']]
    
    def __str__(self):
        return f"{self.document.title} - {self.template.name}"


class CRMRecord(models.Model):
    """Mini CRM - stores extracted data pushed from extraction runs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_id = models.CharField(max_length=255)
    document_title = models.CharField(max_length=255)
    template_id = models.CharField(max_length=255)
    template_name = models.CharField(max_length=255)
    extracted_data = models.JSONField()  # The actual extracted fields
    validation_data = models.JSONField(null=True, blank=True)  # Validation info
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document_title} - {self.template_name}"


class DemoEmail(models.Model):
    """Sample emails for the AI Email Automation demo"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=500)
    body = models.TextField()
    from_email = models.EmailField()
    from_name = models.CharField(max_length=255)
    received_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-received_at']
    
    def __str__(self):
        return self.subject


class DemoEmailResult(models.Model):
    """AI processing results for demo emails"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.OneToOneField(DemoEmail, on_delete=models.CASCADE, related_name='ai_result')
    intent = models.CharField(max_length=100)
    urgency = models.CharField(max_length=20)  # Low, Medium, High
    sentiment = models.CharField(max_length=20)  # Positive, Neutral, Negative
    suggested_owner = models.CharField(max_length=255)
    crm_action = models.CharField(max_length=255)
    draft_reply = models.TextField()
    follow_up_hours = models.IntegerField(default=48)
    confidence_score = models.IntegerField(default=0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Result for {self.email.subject}"


class EmailCRMRecord(models.Model):
    """CRM records created from email automation"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_id = models.CharField(max_length=255)
    email_subject = models.CharField(max_length=500)
    email_from = models.CharField(max_length=255)
    email_from_name = models.CharField(max_length=255)
    intent = models.CharField(max_length=100)
    urgency = models.CharField(max_length=20)
    sentiment = models.CharField(max_length=20)
    assigned_team = models.CharField(max_length=255)
    crm_action = models.CharField(max_length=255)
    task_id = models.CharField(max_length=255, null=True, blank=True)
    ticket_id = models.CharField(max_length=255, null=True, blank=True)
    crm_record_id = models.CharField(max_length=255, null=True, blank=True)
    follow_up_hours = models.IntegerField(default=48)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email_subject} - {self.assigned_team}"


class DemoConversation(models.Model):
    """Sample conversations for Omnichannel AI Support demo"""
    CHANNEL_CHOICES = [
        ('web', 'Web Chat'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    customer_name = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    initial_message = models.TextField()
    status = models.CharField(max_length=20, default='open')  # open, escalated, resolved
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_channel_display()} - {self.customer_name}"


class DemoMessage(models.Model):
    """Messages within a conversation"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(DemoConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20)  # 'customer' or 'ai' or 'human'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender} - {self.conversation}"


class DemoTicket(models.Model):
    """Support tickets created from conversations"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('escalated', 'Escalated'),
        ('resolved', 'Resolved'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.OneToOneField(DemoConversation, on_delete=models.CASCADE, related_name='ticket')
    ticket_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_team = models.CharField(max_length=255)
    intent = models.CharField(max_length=100)
    urgency = models.CharField(max_length=20)
    sentiment = models.CharField(max_length=20)
    summary = models.TextField()
    ai_confidence = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Ticket #{self.ticket_number} - {self.conversation.customer_name}"


class DemoLead(models.Model):
    """Demo lead for qualification"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    company = models.CharField(max_length=255)
    budget_range = models.CharField(max_length=100)
    service_interest = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company}"


class DemoQualification(models.Model):
    """AI qualification result for a lead"""
    INTENT_CHOICES = [
        ('strong', 'Strong'),
        ('moderate', 'Moderate'),
        ('weak', 'Weak'),
    ]
    
    FIT_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lead = models.OneToOneField(DemoLead, on_delete=models.CASCADE, related_name='qualification')
    answers = models.JSONField(default=dict)  # Store Q&A pairs
    score = models.IntegerField(default=0)
    intent = models.CharField(max_length=20, choices=INTENT_CHOICES, default='moderate')
    fit_level = models.CharField(max_length=20, choices=FIT_CHOICES, default='medium')
    budget_match = models.BooleanField(default=False)
    urgency_days = models.IntegerField(null=True, blank=True)
    assigned_team = models.CharField(max_length=255, blank=True)
    recommended_action = models.CharField(max_length=255, blank=True)
    demo_booked = models.BooleanField(default=False)
    demo_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Qualification for {self.lead.name} - Score: {self.score}"


class DemoEvent(models.Model):
    """Simulated events that trigger workflows"""
    EVENT_TYPE_CHOICES = [
        ('form_submission', 'Form Submission'),
        ('instagram_dm', 'Instagram DM'),
        ('payment_failed', 'Payment Failed'),
        ('high_score_lead', 'High Score Lead'),
        ('support_escalation', 'Support Escalation'),
        ('email_received', 'Email Received'),
        ('chat_message', 'Chat Message'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('processed', 'Processed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_event_type_display()} - {self.created_at}"


class DemoWorkflowRun(models.Model):
    """Workflow execution result for an event"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.OneToOneField(DemoEvent, on_delete=models.CASCADE, related_name='workflow_run')
    decision_path = models.JSONField(default=list)  # List of rule nodes that were evaluated
    actions = models.JSONField(default=list)  # List of actions executed
    confidence_score = models.IntegerField(default=0)
    execution_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Workflow for {self.event.get_event_type_display()}"


class QualityConversation(models.Model):
    """Conversations for quality control monitoring"""
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('chat', 'Chat'),
        ('support', 'Support Ticket'),
        ('social', 'Social Media'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    message = models.TextField()
    sender_type = models.CharField(max_length=20)  # 'customer' or 'agent'
    sender_name = models.CharField(max_length=255, blank=True)
    conversation_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_channel_display()} - {self.message[:50]}..."


class DemoRiskAnalysis(models.Model):
    """AI risk analysis for conversations"""
    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.OneToOneField(QualityConversation, on_delete=models.CASCADE, related_name='risk_analysis')
    sentiment_score = models.FloatField(default=0.0)  # -1 to 1
    sentiment_label = models.CharField(max_length=50, default='neutral')
    churn_risk = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default='low')
    compliance_flag = models.BooleanField(default=False)
    compliance_type = models.CharField(max_length=100, blank=True)  # 'GDPR', 'ROI_Claim', etc.
    severity_score = models.FloatField(default=0.0)  # 0 to 10
    alert_created = models.BooleanField(default=False)
    automation_paused = models.BooleanField(default=False)
    escalation_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Risk Analysis for {self.conversation.get_channel_display()} - Severity: {self.severity_score}"


class DemoAnalyticsSnapshot(models.Model):
    """Analytics snapshot for AI insights"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    leads = models.IntegerField(default=0)
    conversion_rate = models.FloatField(default=0.0)
    sales_qualified_leads = models.IntegerField(default=0)
    deals_closed = models.IntegerField(default=0)
    support_tickets = models.IntegerField(default=0)
    churn_signals = models.IntegerField(default=0)
    average_response_time_minutes = models.IntegerField(default=0)
    channel_breakdown = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Analytics Snapshot - {self.period_start.date()}"


class DemoInsight(models.Model):
    """AI-generated insights from analytics"""
    IMPACT_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    INSIGHT_TYPE_CHOICES = [
        ('bottleneck', 'Bottleneck Detection'),
        ('opportunity', 'Revenue Opportunity'),
        ('risk', 'Risk Alert'),
        ('optimization', 'Optimization'),
        ('pattern', 'Pattern Detection'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    snapshot = models.ForeignKey(DemoAnalyticsSnapshot, on_delete=models.CASCADE, related_name='insights')
    insight_type = models.CharField(max_length=20, choices=INSIGHT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    what_happened = models.TextField()
    why_it_matters = models.TextField()
    recommended_action = models.TextField()
    estimated_revenue_lift = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    impact_level = models.CharField(max_length=20, choices=IMPACT_CHOICES, default='medium')
    confidence_score = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)  # Higher = more important
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_impact_level_display()} Impact"


class CRMContact(models.Model):
    """CRM Contact/Lead for workflow automation"""
    STATUS_CHOICES = [
        ('new', 'New Lead'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('closed_won', 'Closed Won'),
        ('closed_lost', 'Closed Lost'),
    ]
    
    CHANNEL_CHOICES = [
        ('website', 'Website Form'),
        ('instagram', 'Instagram DM'),
        ('email', 'Email'),
        ('referral', 'Referral'),
        ('manual', 'Manual Entry'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='website')
    source_message = models.TextField(blank=True)  # Original message/input
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    pipeline_stage = models.CharField(max_length=50, default='New Lead')
    assigned_to = models.CharField(max_length=255, blank=True)
    intent = models.CharField(max_length=50, blank=True)  # Sales, Support, Billing, Partnership
    urgency = models.CharField(max_length=20, default='medium')  # Low, Medium, High
    fit_score = models.IntegerField(default=0)  # 0-100
    recommended_route = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_channel_display()}"


class CRMTag(models.Model):
    """Tags for CRM contacts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='blue')  # For UI display
    contacts = models.ManyToManyField(CRMContact, related_name='tags', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class CRMTask(models.Model):
    """Tasks created from automation"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(CRMContact, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.CharField(max_length=255, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.contact.name}"


class CRMTicket(models.Model):
    """Support tickets created from automation"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(CRMContact, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.status}"


class CRMActivity(models.Model):
    """Activity timeline for contacts"""
    ACTIVITY_TYPE_CHOICES = [
        ('created', 'Contact Created'),
        ('tagged', 'Tagged'),
        ('stage_changed', 'Stage Changed'),
        ('assigned', 'Assigned'),
        ('task_created', 'Task Created'),
        ('followup_scheduled', 'Follow-up Scheduled'),
        ('ticket_created', 'Ticket Created'),
        ('automation_triggered', 'Automation Triggered'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(CRMContact, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)  # Store additional info
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.contact.name}"


class CRMAutomationRun(models.Model):
    """Log of automation runs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = models.ForeignKey(CRMContact, on_delete=models.CASCADE, related_name='automation_runs')
    triggered_by = models.CharField(max_length=50)  # 'form_submission', 'dm', etc.
    rules_matched = models.JSONField(default=list)  # List of rule names that matched
    actions_executed = models.JSONField(default=list)  # List of actions taken
    confidence_score = models.IntegerField(default=0)
    execution_time_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Automation Run - {self.contact.name}"

