from django.core.management.base import BaseCommand
from myApp.models import QualityConversation, DemoRiskAnalysis


class Command(BaseCommand):
    help = 'Seed sample conversations for Quality Control & Monitoring demo'

    def handle(self, *args, **options):
        # Clear existing data
        DemoRiskAnalysis.objects.all().delete()
        QualityConversation.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Clearing existing quality conversations...'))
        
        # Sample conversations with expected analysis results
        conversations_data = [
            {
                'channel': 'chat',
                'message': 'Thanks for the quick response! Really appreciate your help.',
                'sender_type': 'customer',
                'sender_name': 'Sarah Johnson',
                'expected_severity': 1.0,
                'expected_churn': 'low',
                'expected_compliance': False,
            },
            {
                'channel': 'email',
                'message': 'This is the third time I\'ve contacted you about this issue. If it\'s not resolved today, I\'m canceling my subscription.',
                'sender_type': 'customer',
                'sender_name': 'Mike Chen',
                'expected_severity': 8.5,
                'expected_churn': 'high',
                'expected_compliance': False,
            },
            {
                'channel': 'support',
                'message': 'Yes, we guarantee 200% ROI within the first 90 days. Our clients typically see returns of 250-300%.',
                'sender_type': 'agent',
                'sender_name': 'Sales Rep',
                'expected_severity': 7.0,
                'expected_churn': 'low',
                'expected_compliance': True,
                'compliance_type': 'ROI_Claim',
            },
            {
                'channel': 'email',
                'message': 'If this billing issue isn\'t resolved today, I\'ll dispute the charge with my credit card company and file a complaint.',
                'sender_type': 'customer',
                'sender_name': 'Emily Rodriguez',
                'expected_severity': 9.0,
                'expected_churn': 'high',
                'expected_compliance': True,
                'compliance_type': 'Payment_Dispute',
            },
            {
                'channel': 'chat',
                'message': 'I want to exercise my right under GDPR. Please delete all my personal data immediately and confirm deletion.',
                'sender_type': 'customer',
                'sender_name': 'David Park',
                'expected_severity': 7.5,
                'expected_churn': 'low',
                'expected_compliance': True,
                'compliance_type': 'GDPR_Request',
            },
            {
                'channel': 'social',
                'message': 'Your service has been terrible. I\'ve been waiting for a response for 5 days. This is unacceptable.',
                'sender_type': 'customer',
                'sender_name': 'Lisa Thompson',
                'expected_severity': 6.5,
                'expected_churn': 'medium',
                'expected_compliance': False,
            },
            {
                'channel': 'email',
                'message': 'Great service! The team was very helpful and resolved my issue quickly.',
                'sender_type': 'customer',
                'sender_name': 'Robert Williams',
                'expected_severity': 0.5,
                'expected_churn': 'low',
                'expected_compliance': False,
            },
            {
                'channel': 'support',
                'message': 'I\'m switching to your competitor. They offer better pricing and I\'ve heard their support is much faster.',
                'sender_type': 'customer',
                'sender_name': 'Jennifer Martinez',
                'expected_severity': 7.0,
                'expected_churn': 'high',
                'expected_compliance': False,
            },
        ]
        
        created_count = 0
        
        for conv_data in conversations_data:
            # Extract analysis data
            expected_severity = conv_data.pop('expected_severity')
            expected_churn = conv_data.pop('expected_churn')
            expected_compliance = conv_data.pop('expected_compliance')
            compliance_type = conv_data.pop('compliance_type', '')
            
            # Create conversation
            conversation = QualityConversation.objects.create(**conv_data)
            
            # Determine sentiment
            message_lower = conversation.message.lower()
            if 'thanks' in message_lower or 'great' in message_lower or 'appreciate' in message_lower:
                sentiment_score = 0.6
                sentiment_label = 'Positive'
            elif 'terrible' in message_lower or 'unacceptable' in message_lower or 'cancel' in message_lower:
                sentiment_score = -0.7
                sentiment_label = 'Very Negative'
            elif 'third time' in message_lower or 'dispute' in message_lower:
                sentiment_score = -0.7
                sentiment_label = 'Very Negative'
            else:
                sentiment_score = -0.4
                sentiment_label = 'Negative'
            
            # Determine escalation
            escalation_required = expected_severity >= 7.0 or expected_compliance
            automation_paused = escalation_required
            alert_created = escalation_required
            
            # Create risk analysis
            DemoRiskAnalysis.objects.create(
                conversation=conversation,
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
                churn_risk=expected_churn,
                compliance_flag=expected_compliance,
                compliance_type=compliance_type,
                severity_score=expected_severity,
                alert_created=alert_created,
                automation_paused=automation_paused,
                escalation_required=escalation_required
            )
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created conversation with analysis: {conv_data["sender_name"]} ({conv_data["channel"]}) - Severity: {expected_severity}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} conversations with risk analyses!')
        )

