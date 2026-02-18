from django.core.management.base import BaseCommand
from myApp.models import DemoLead, DemoQualification
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Seed demo leads and qualifications for AI Sales Lead Qualification demo'

    def handle(self, *args, **options):
        # Clear existing data
        DemoQualification.objects.all().delete()
        DemoLead.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Clearing existing leads and qualifications...'))
        
        # Sample leads with varying quality
        leads_data = [
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@techcorp.com',
                'company': 'TechCorp Solutions',
                'budget_range': '$100k+',
                'service_interest': 'Custom AI Systems',
                'answers': {
                    'revenue': '$1M+ monthly revenue',
                    'crm': 'Spreadsheet',
                    'urgency': 'Immediately',
                    'bottleneck': 'We are struggling with manual data entry and losing time on repetitive tasks'
                },
                'expected_score': 85
            },
            {
                'name': 'Michael Chen',
                'email': 'mchen@startup.io',
                'company': 'StartupIO',
                'budget_range': '$50k - $100k',
                'service_interest': 'AI Automation',
                'answers': {
                    'revenue': '$500k monthly',
                    'crm': 'HubSpot',
                    'urgency': '30 days',
                    'bottleneck': 'Customer support is slow and inefficient'
                },
                'expected_score': 65
            },
            {
                'name': 'Emily Rodriguez',
                'email': 'emily@retailplus.com',
                'company': 'RetailPlus',
                'budget_range': '$25k - $50k',
                'service_interest': 'Customer Support',
                'answers': {
                    'revenue': '$250k monthly',
                    'crm': 'Salesforce',
                    'urgency': 'Next quarter',
                    'bottleneck': 'Looking to improve our processes'
                },
                'expected_score': 45
            },
            {
                'name': 'David Park',
                'email': 'david@enterprise.com',
                'company': 'Enterprise Global',
                'budget_range': '$100k+',
                'service_interest': 'Multiple Services',
                'answers': {
                    'revenue': '$2M+ monthly',
                    'crm': 'None',
                    'urgency': 'ASAP',
                    'bottleneck': 'We have major challenges with manual workflows and need automation urgently'
                },
                'expected_score': 90
            },
            {
                'name': 'Lisa Thompson',
                'email': 'lisa@smallbiz.com',
                'company': 'SmallBiz Co',
                'budget_range': 'Under $10k',
                'service_interest': 'Email Automation',
                'answers': {
                    'revenue': 'Under $100k',
                    'crm': 'Excel',
                    'urgency': '90 days',
                    'bottleneck': 'Just exploring options'
                },
                'expected_score': 25
            },
            {
                'name': 'Robert Williams',
                'email': 'rwilliams@midmarket.com',
                'company': 'MidMarket Industries',
                'budget_range': '$50k - $100k',
                'service_interest': 'Document Processing',
                'answers': {
                    'revenue': '$750k monthly',
                    'crm': 'Pipedrive',
                    'urgency': '30 days',
                    'bottleneck': 'Document processing is taking too much time and causing errors'
                },
                'expected_score': 70
            },
            {
                'name': 'Jennifer Martinez',
                'email': 'jennifer@consulting.com',
                'company': 'Martinez Consulting',
                'budget_range': '$25k - $50k',
                'service_interest': 'AI Automation',
                'answers': {
                    'revenue': '$200k monthly',
                    'crm': 'Zoho',
                    'urgency': '60 days',
                    'bottleneck': 'Need better client communication tools'
                },
                'expected_score': 50
            },
            {
                'name': 'James Anderson',
                'email': 'james@fintech.com',
                'company': 'FinTech Innovations',
                'budget_range': '$100k+',
                'service_interest': 'Custom AI Systems',
                'answers': {
                    'revenue': '$1.5M monthly',
                    'crm': 'Salesforce',
                    'urgency': 'Immediately',
                    'bottleneck': 'Critical need for AI-powered compliance and risk management systems'
                },
                'expected_score': 88
            },
            {
                'name': 'Amanda White',
                'email': 'amanda@ecommerce.com',
                'company': 'E-Commerce Pro',
                'budget_range': '$10k - $25k',
                'service_interest': 'Customer Support',
                'answers': {
                    'revenue': '$150k monthly',
                    'crm': 'Shopify',
                    'urgency': 'Next quarter',
                    'bottleneck': 'Customer service could be better'
                },
                'expected_score': 35
            },
            {
                'name': 'Christopher Lee',
                'email': 'chris@healthcare.com',
                'company': 'Healthcare Solutions',
                'budget_range': '$50k - $100k',
                'service_interest': 'Document Processing',
                'answers': {
                    'revenue': '$600k monthly',
                    'crm': 'None',
                    'urgency': '30 days',
                    'bottleneck': 'Manual patient record processing is slow and error-prone'
                },
                'expected_score': 75
            }
        ]
        
        created_count = 0
        
        for lead_data in leads_data:
            # Create lead
            lead = DemoLead.objects.create(
                name=lead_data['name'],
                email=lead_data['email'],
                company=lead_data['company'],
                budget_range=lead_data['budget_range'],
                service_interest=lead_data['service_interest']
            )
            
            # Calculate score (same logic as in views.py)
            score = 0
            answers = lead_data['answers']
            budget = lead_data['budget_range'].lower()
            
            # Budget scoring
            if '50k+' in budget or '100k+' in budget:
                score += 30
            elif '25k' in budget or '50k' in budget:
                score += 20
            elif '10k' in budget:
                score += 10
            
            # Revenue scoring
            revenue = answers.get('revenue', '').lower()
            if '500k+' in revenue or '1m+' in revenue or 'million' in revenue or '2m' in revenue or '1.5m' in revenue:
                score += 25
            elif '100k' in revenue or '250k' in revenue or '200k' in revenue or '150k' in revenue:
                score += 15
            
            # Urgency scoring
            urgency = answers.get('urgency', '').lower()
            if 'immediately' in urgency or 'asap' in urgency or 'now' in urgency:
                score += 25
            elif '30' in urgency or 'month' in urgency:
                score += 15
            elif '60' in urgency or '90' in urgency or 'quarter' in urgency:
                score += 5
            
            # CRM mismatch
            crm = answers.get('crm', '').lower()
            if 'spreadsheet' in crm or 'excel' in crm or 'none' in crm or 'nothing' in crm:
                score += 10
            
            # Pain signals
            bottleneck = answers.get('bottleneck', '').lower()
            pain_keywords = ['manual', 'time', 'inefficient', 'slow', 'error', 'difficult', 'struggling', 'challenge', 'critical', 'urgent', 'losing']
            pain_score = sum(5 for keyword in pain_keywords if keyword in bottleneck)
            if pain_score > 0:
                score += min(pain_score, 15)
            
            # Determine intent and fit
            if score >= 70:
                intent = 'strong'
                fit_level = 'high'
                recommended_action = 'Book strategy call'
                assigned_team = 'Enterprise Sales'
                assigned_to = 'Sarah (Sales)'
                demo_booked = True
                demo_date = datetime.now() - timedelta(days=random.randint(1, 7))
                demo_date = demo_date.replace(hour=random.choice([10, 11, 14, 15, 16]), minute=0)
            elif score >= 40:
                intent = 'moderate'
                fit_level = 'medium'
                recommended_action = 'Nurture campaign'
                assigned_team = 'SMB Sales'
                assigned_to = 'Mike (Sales)'
                demo_booked = False
                demo_date = None
            else:
                intent = 'weak'
                fit_level = 'low'
                recommended_action = 'Email nurture'
                assigned_team = 'Marketing'
                assigned_to = 'Marketing Team'
                demo_booked = False
                demo_date = None
            
            # Calculate urgency days
            urgency_days = None
            if 'immediately' in urgency or 'asap' in urgency:
                urgency_days = 7
            elif '30' in urgency or 'month' in urgency:
                urgency_days = 30
            elif '60' in urgency or 'quarter' in urgency:
                urgency_days = 60
            elif '90' in urgency:
                urgency_days = 90
            
            # Create qualification
            DemoQualification.objects.create(
                lead=lead,
                answers=answers,
                score=score,
                intent=intent,
                fit_level=fit_level,
                budget_match=score >= 20 and ('50k+' in budget or '100k+' in budget),
                urgency_days=urgency_days,
                assigned_team=assigned_team,
                recommended_action=recommended_action,
                demo_booked=demo_booked,
                demo_date=demo_date,
                assigned_to=assigned_to
            )
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created lead: {lead.name} ({lead.company}) - Score: {score}')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} leads with qualifications!')
        )

