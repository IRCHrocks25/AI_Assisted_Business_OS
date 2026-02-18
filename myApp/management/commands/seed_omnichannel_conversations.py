from django.core.management.base import BaseCommand
from myApp.models import DemoConversation, DemoMessage
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed demo conversations for the Omnichannel AI Support demo'

    def handle(self, *args, **options):
        # Clear existing conversations
        DemoConversation.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared existing conversations'))
        
        # Sample conversations
        conversations = [
            {
                'channel': 'instagram',
                'customer_name': 'Sarah Chen',
                'initial_message': 'Hi, I haven\'t received my invoice yet. Can you help?',
                'created_at': timezone.now() - timedelta(minutes=15)
            },
            {
                'channel': 'web',
                'customer_name': 'Michael Rodriguez',
                'initial_message': 'I\'m having trouble logging into my account. It says invalid credentials but I\'m using the correct password.',
                'created_at': timezone.now() - timedelta(hours=1)
            },
            {
                'channel': 'facebook',
                'customer_name': 'Jennifer Park',
                'initial_message': 'Love your product! Quick question - do you offer bulk discounts for enterprise customers?',
                'created_at': timezone.now() - timedelta(hours=2)
            },
            {
                'channel': 'email',
                'customer_name': 'David Kim',
                'initial_message': 'I was charged twice this month. This is unacceptable. I need a refund immediately.',
                'created_at': timezone.now() - timedelta(hours=3)
            },
            {
                'channel': 'whatsapp',
                'customer_name': 'Emma Wilson',
                'initial_message': 'Hi! I need to update my billing address. How do I do that?',
                'created_at': timezone.now() - timedelta(hours=4)
            },
            {
                'channel': 'web',
                'customer_name': 'Alex Thompson',
                'initial_message': 'The feature I requested last month - is it available yet?',
                'created_at': timezone.now() - timedelta(hours=5)
            },
            {
                'channel': 'instagram',
                'customer_name': 'Lisa Wang',
                'initial_message': 'Your service is amazing! Just wanted to say thank you for the great support.',
                'created_at': timezone.now() - timedelta(hours=6)
            },
            {
                'channel': 'facebook',
                'customer_name': 'Robert Chen',
                'initial_message': 'URGENT: Our entire system is down. None of our team can access the platform. Please help ASAP!',
                'created_at': timezone.now() - timedelta(minutes=30),
                'status': 'escalated'
            },
            {
                'channel': 'email',
                'customer_name': 'Ryan Miller',
                'initial_message': 'I\'m interested in your API integration. Can someone from your technical team contact me?',
                'created_at': timezone.now() - timedelta(hours=7)
            },
            {
                'channel': 'whatsapp',
                'customer_name': 'Olivia Brown',
                'initial_message': 'I need to cancel my subscription. How do I do that?',
                'created_at': timezone.now() - timedelta(hours=8)
            }
        ]
        
        # Create conversations
        for conv_data in conversations:
            status = conv_data.pop('status', 'open')
            conversation = DemoConversation.objects.create(
                status=status,
                **conv_data
            )
            
            # Add some follow-up messages for some conversations
            if conversation.channel == 'web' and conversation.customer_name == 'Michael Rodriguez':
                DemoMessage.objects.create(
                    conversation=conversation,
                    sender='customer',
                    content='I\'ve tried resetting my password multiple times but still can\'t get in.'
                )
            elif conversation.channel == 'facebook' and conversation.customer_name == 'Robert Chen':
                DemoMessage.objects.create(
                    conversation=conversation,
                    sender='customer',
                    content='This is affecting our production environment. We have customers waiting!'
                )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(conversations)} demo conversations'))

