from django.core.management.base import BaseCommand
from myApp.models import DemoEmail
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed demo emails for the AI Email Automation demo'

    def handle(self, *args, **options):
        # Clear existing demo emails
        DemoEmail.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing demo emails'))
        
        # Sample emails
        emails = [
            {
                'subject': 'Need pricing for 50 licenses ASAP',
                'body': '''Hi there,

We're looking to scale our team and need pricing information for 50 user licenses. We need this information by end of week as we're making a decision soon.

Could you please provide:
- Per-user pricing
- Annual vs monthly options
- Any volume discounts
- Implementation timeline

Thanks!
Sarah Chen
CTO, TechStart Inc.''',
                'from_email': 'sarah.chen@techstart.com',
                'from_name': 'Sarah Chen',
                'received_at': timezone.now() - timedelta(hours=2)
            },
            {
                'subject': 'Bug Report - Login not working',
                'body': '''Hello Support Team,

I'm experiencing an issue where I cannot log into my account. I've tried resetting my password multiple times but still cannot access the system.

Error message: "Invalid credentials" even though I'm using the correct password.

This is urgent as I have a deadline tomorrow and need access to my account.

Please help ASAP.

Thanks,
Michael Rodriguez
mrodriguez@example.com''',
                'from_email': 'mrodriguez@example.com',
                'from_name': 'Michael Rodriguez',
                'received_at': timezone.now() - timedelta(hours=5)
            },
            {
                'subject': 'Partnership Opportunity - Integration Request',
                'body': '''Dear Team,

I'm reaching out from InnovateCorp to explore a potential partnership opportunity. We're interested in integrating your platform with our existing CRM system.

We have over 500 enterprise clients who could benefit from this integration. We'd like to discuss:
- Technical feasibility
- Partnership terms
- Revenue sharing model
- Timeline for integration

Would you be available for a call this week to discuss further?

Best regards,
Jennifer Park
VP of Partnerships, InnovateCorp
jpark@innovatecorp.com''',
                'from_email': 'jpark@innovatecorp.com',
                'from_name': 'Jennifer Park',
                'received_at': timezone.now() - timedelta(hours=8)
            },
            {
                'subject': 'Feature Request - Export Functionality',
                'body': '''Hi,

I've been using your platform for a few months now and it's been great! I have a feature request that would make my workflow much easier.

Could you add the ability to export reports in Excel format? Currently, I can only export as PDF, but I need to manipulate the data in Excel for my analysis.

This would be a huge time-saver for me and my team.

Thanks for considering!
Alex Thompson
alex.thompson@company.com''',
                'from_email': 'alex.thompson@company.com',
                'from_name': 'Alex Thompson',
                'received_at': timezone.now() - timedelta(hours=12)
            },
            {
                'subject': 'Complaint - Billing Issue',
                'body': '''To Whom It May Concern,

I'm very frustrated with a billing issue I've been experiencing. I was charged twice for my subscription this month, and despite multiple emails, I haven't received a response or refund.

This is unacceptable customer service. I've been a loyal customer for 2 years and this is the first time I've had such a poor experience.

I need this resolved immediately or I will be forced to cancel my subscription and file a complaint with my credit card company.

Regards,
David Kim
david.kim@business.com''',
                'from_email': 'david.kim@business.com',
                'from_name': 'David Kim',
                'received_at': timezone.now() - timedelta(hours=1)
            },
            {
                'subject': 'General Question - API Documentation',
                'body': '''Hello,

I'm a developer working on integrating your API into our application. I've reviewed the documentation but have a few questions:

1. What's the rate limit for API calls?
2. Do you support webhooks for real-time updates?
3. Is there a sandbox environment for testing?

Thanks for your help!
Ryan Miller
ryan.miller@devstudio.io''',
                'from_email': 'ryan.miller@devstudio.io',
                'from_name': 'Ryan Miller',
                'received_at': timezone.now() - timedelta(hours=3)
            },
            {
                'subject': 'Thank you - Great product!',
                'body': '''Hi Team,

I just wanted to reach out and say thank you for such an amazing product! We've been using it for 6 months now and it's transformed how we work.

The automation features have saved us countless hours, and the support team has been incredibly helpful whenever we had questions.

Keep up the great work!

Best,
Lisa Wang
lisa.wang@startup.com''',
                'from_email': 'lisa.wang@startup.com',
                'from_name': 'Lisa Wang',
                'received_at': timezone.now() - timedelta(hours=6)
            },
            {
                'subject': 'Urgent - System Down',
                'body': '''URGENT: Our entire system appears to be down. None of our team members can access the platform.

We're getting error 500 on all endpoints. This is affecting our production environment and we have customers waiting.

Please investigate immediately.

Emergency contact: +1-555-0123

Thanks,
Emergency Response Team
emergency@criticalsystems.com''',
                'from_email': 'emergency@criticalsystems.com',
                'from_name': 'Emergency Team',
                'received_at': timezone.now() - timedelta(minutes=15)
            },
            {
                'subject': 'Follow-up: Contract Renewal Discussion',
                'body': '''Hi,

Following up on our conversation last week about renewing our annual contract. We'd like to discuss:
- Updated pricing for 2024
- New features included
- Migration timeline
- Support package options

Can we schedule a call this week?

Best,
Robert Chen
robert.chen@enterprise.com''',
                'from_email': 'robert.chen@enterprise.com',
                'from_name': 'Robert Chen',
                'received_at': timezone.now() - timedelta(hours=4)
            },
            {
                'subject': 'Question about API Rate Limits',
                'body': '''Hello Support,

I'm building an integration and need to understand the API rate limits. The documentation mentions limits but doesn't specify:
- Requests per minute
- Requests per hour
- Burst capacity
- How to handle rate limit errors

Could you clarify these details?

Thanks,
Emma Wilson
Developer
emma.wilson@devteam.io''',
                'from_email': 'emma.wilson@devteam.io',
                'from_name': 'Emma Wilson',
                'received_at': timezone.now() - timedelta(hours=7)
            }
        ]
        
        # Create emails
        for email_data in emails:
            DemoEmail.objects.create(**email_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(emails)} demo emails'))

