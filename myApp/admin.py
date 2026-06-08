from django.contrib import admin
from .models import ExtractionTemplate, Document, ExtractionRun, CRMRecord, DemoEmail, DemoEmailResult, EmailCRMRecord, DemoConversation, DemoMessage, DemoTicket, DemoLead, DemoQualification, DemoEvent, DemoWorkflowRun, QualityConversation, DemoRiskAnalysis, DemoAnalyticsSnapshot, DemoInsight, CRMContact, CRMTag, CRMTask, CRMTicket, CRMActivity, CRMAutomationRun, BlogPost

@admin.register(ExtractionTemplate)
class ExtractionTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']
    search_fields = ['title']

@admin.register(ExtractionRun)
class ExtractionRunAdmin(admin.ModelAdmin):
    list_display = ['document', 'template', 'status', 'created_at', 'pushed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['document__title', 'template__name']

@admin.register(CRMRecord)
class CRMRecordAdmin(admin.ModelAdmin):
    list_display = ['document_title', 'template_name', 'created_at']
    list_filter = ['template_name', 'created_at']
    search_fields = ['document_title', 'template_name']

@admin.register(DemoEmail)
class DemoEmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'from_name', 'from_email', 'received_at', 'is_read', 'is_processed']
    list_filter = ['is_read', 'is_processed', 'received_at']
    search_fields = ['subject', 'from_name', 'from_email', 'body']

@admin.register(DemoEmailResult)
class DemoEmailResultAdmin(admin.ModelAdmin):
    list_display = ['email', 'intent', 'urgency', 'sentiment', 'suggested_owner', 'confidence_score', 'created_at']
    list_filter = ['intent', 'urgency', 'sentiment', 'created_at']
    search_fields = ['email__subject', 'intent', 'suggested_owner']

@admin.register(EmailCRMRecord)
class EmailCRMRecordAdmin(admin.ModelAdmin):
    list_display = ['email_subject', 'email_from_name', 'intent', 'urgency', 'assigned_team', 'crm_action', 'created_at']
    list_filter = ['intent', 'urgency', 'sentiment', 'assigned_team', 'created_at']
    search_fields = ['email_subject', 'email_from_name', 'email_from', 'assigned_team']

@admin.register(DemoConversation)
class DemoConversationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'channel', 'status', 'is_processed', 'created_at']
    list_filter = ['channel', 'status', 'is_processed', 'created_at']
    search_fields = ['customer_name', 'initial_message']

@admin.register(DemoMessage)
class DemoMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'sender', 'created_at']
    list_filter = ['sender', 'created_at']
    search_fields = ['content']

@admin.register(DemoTicket)
class DemoTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'conversation', 'status', 'assigned_team', 'urgency', 'created_at']
    list_filter = ['status', 'urgency', 'sentiment', 'assigned_team', 'created_at']
    search_fields = ['ticket_number', 'conversation__customer_name', 'summary']

@admin.register(DemoLead)
class DemoLeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'budget_range', 'service_interest', 'created_at']
    list_filter = ['budget_range', 'service_interest', 'created_at']
    search_fields = ['name', 'email', 'company']

@admin.register(DemoQualification)
class DemoQualificationAdmin(admin.ModelAdmin):
    list_display = ['lead', 'score', 'intent', 'fit_level', 'assigned_team', 'demo_booked', 'created_at']
    list_filter = ['intent', 'fit_level', 'demo_booked', 'assigned_team', 'created_at']
    search_fields = ['lead__name', 'lead__company', 'assigned_team']

@admin.register(DemoEvent)
class DemoEventAdmin(admin.ModelAdmin):
    list_display = ['event_type', 'status', 'created_at', 'processed_at']
    list_filter = ['event_type', 'status', 'created_at']
    search_fields = ['event_type', 'payload']

@admin.register(DemoWorkflowRun)
class DemoWorkflowRunAdmin(admin.ModelAdmin):
    list_display = ['event', 'confidence_score', 'execution_time_ms', 'created_at']
    list_filter = ['created_at']
    search_fields = ['event__event_type']

@admin.register(QualityConversation)
class QualityConversationAdmin(admin.ModelAdmin):
    list_display = ['channel', 'sender_type', 'sender_name', 'created_at']
    list_filter = ['channel', 'sender_type', 'created_at']
    search_fields = ['message', 'sender_name']

@admin.register(DemoRiskAnalysis)
class DemoRiskAnalysisAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'severity_score', 'churn_risk', 'compliance_flag', 'alert_created', 'created_at']
    list_filter = ['churn_risk', 'compliance_flag', 'alert_created', 'created_at']
    search_fields = ['conversation__message']

@admin.register(DemoAnalyticsSnapshot)
class DemoAnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ['period_start', 'leads', 'conversion_rate', 'deals_closed', 'created_at']
    list_filter = ['created_at']
    search_fields = []

@admin.register(DemoInsight)
class DemoInsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'insight_type', 'impact_level', 'confidence_score', 'priority', 'created_at']
    list_filter = ['insight_type', 'impact_level', 'created_at']
    search_fields = ['title', 'description']

@admin.register(CRMContact)
class CRMContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'channel', 'status', 'pipeline_stage', 'assigned_to', 'created_at']
    list_filter = ['channel', 'status', 'intent', 'urgency', 'created_at']
    search_fields = ['name', 'email', 'company']

@admin.register(CRMTag)
class CRMTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    filter_horizontal = ['contacts']

@admin.register(CRMTask)
class CRMTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact', 'priority', 'assigned_to', 'completed', 'created_at']
    list_filter = ['priority', 'completed', 'created_at']
    search_fields = ['title', 'description']

@admin.register(CRMTicket)
class CRMTicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']

@admin.register(CRMActivity)
class CRMActivityAdmin(admin.ModelAdmin):
    list_display = ['contact', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['description']

@admin.register(CRMAutomationRun)
class CRMAutomationRunAdmin(admin.ModelAdmin):
    list_display = ['contact', 'triggered_by', 'confidence_score', 'created_at']
    list_filter = ['triggered_by', 'created_at']
    search_fields = ['contact__name']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'read_minutes', 'published_at', 'is_published', 'order']
    list_filter = ['category', 'is_published', 'published_at']
    list_editable = ['is_published', 'order']
    search_fields = ['title', 'keyword', 'meta_description', 'body_html']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'category', 'accent', 'author')}),
        ('SEO', {'fields': ('keyword', 'meta_title', 'meta_description', 'excerpt')}),
        ('Content', {'fields': ('body_html', 'read_minutes')}),
        ('Publishing', {'fields': ('is_published', 'order', 'published_at')}),
    )

