"""
Management command to seed default extraction templates
"""
from django.core.management.base import BaseCommand
from myApp.models import ExtractionTemplate
import json


class Command(BaseCommand):
    help = 'Seed default extraction templates'

    def handle(self, *args, **options):
        templates_data = [
            {
                "name": "General Contract Template v1",
                "schema": {
                    "doc_type": "contract",
                    "fields": [
                        {"key": "party_a_name", "label": "Party A", "type": "string", "required": True},
                        {"key": "party_b_name", "label": "Party B", "type": "string", "required": True},
                        {"key": "effective_date", "label": "Effective Date", "type": "date", "required": False},
                        {"key": "termination_date", "label": "Termination Date", "type": "date", "required": False},
                        {"key": "payment_terms", "label": "Payment Terms", "type": "string", "required": False},
                        {"key": "governing_law", "label": "Governing Law", "type": "string", "required": False},
                        {"key": "total_value", "label": "Total Contract Value", "type": "number", "required": False},
                        {"key": "currency", "label": "Currency", "type": "string", "required": False}
                    ]
                }
            },
            {
                "name": "NDA Template v1",
                "schema": {
                    "doc_type": "nda",
                    "fields": [
                        {"key": "disclosing_party", "label": "Disclosing Party", "type": "string", "required": True},
                        {"key": "receiving_party", "label": "Receiving Party", "type": "string", "required": True},
                        {"key": "effective_date", "label": "Effective Date", "type": "date", "required": False},
                        {"key": "expiration_date", "label": "Expiration Date", "type": "date", "required": False},
                        {"key": "term_duration", "label": "Term Duration", "type": "string", "required": False},
                        {"key": "confidential_information_scope", "label": "Confidential Information Scope", "type": "string", "required": False},
                        {"key": "exclusions", "label": "Exclusions", "type": "string", "required": False},
                        {"key": "return_of_materials", "label": "Return of Materials", "type": "string", "required": False},
                        {"key": "governing_law", "label": "Governing Law", "type": "string", "required": False},
                        {"key": "jurisdiction", "label": "Jurisdiction", "type": "string", "required": False}
                    ]
                }
            },
            {
                "name": "MSA Template v1",
                "schema": {
                    "doc_type": "msa",
                    "fields": [
                        {"key": "service_provider", "label": "Service Provider", "type": "string", "required": True},
                        {"key": "client", "label": "Client", "type": "string", "required": True},
                        {"key": "effective_date", "label": "Effective Date", "type": "date", "required": False},
                        {"key": "term_length", "label": "Term Length", "type": "string", "required": False},
                        {"key": "renewal_terms", "label": "Renewal Terms", "type": "string", "required": False},
                        {"key": "termination_notice", "label": "Termination Notice Period", "type": "string", "required": False},
                        {"key": "service_description", "label": "Service Description", "type": "string", "required": False},
                        {"key": "pricing_model", "label": "Pricing Model", "type": "string", "required": False},
                        {"key": "payment_terms", "label": "Payment Terms", "type": "string", "required": False},
                        {"key": "sla_requirements", "label": "SLA Requirements", "type": "string", "required": False},
                        {"key": "liability_cap", "label": "Liability Cap", "type": "string", "required": False},
                        {"key": "governing_law", "label": "Governing Law", "type": "string", "required": False}
                    ]
                }
            },
            {
                "name": "KPI Report Template v1",
                "schema": {
                    "doc_type": "report",
                    "fields": [
                        {"key": "report_title", "label": "Report Title", "type": "string", "required": True},
                        {"key": "report_period", "label": "Report Period", "type": "string", "required": False},
                        {"key": "report_date", "label": "Report Date", "type": "date", "required": False},
                        {"key": "revenue", "label": "Revenue", "type": "number", "required": False},
                        {"key": "revenue_growth", "label": "Revenue Growth %", "type": "number", "required": False},
                        {"key": "customer_acquisition_cost", "label": "Customer Acquisition Cost (CAC)", "type": "number", "required": False},
                        {"key": "lifetime_value", "label": "Customer Lifetime Value (LTV)", "type": "number", "required": False},
                        {"key": "ltv_cac_ratio", "label": "LTV:CAC Ratio", "type": "number", "required": False},
                        {"key": "churn_rate", "label": "Churn Rate %", "type": "number", "required": False},
                        {"key": "active_users", "label": "Active Users", "type": "number", "required": False},
                        {"key": "conversion_rate", "label": "Conversion Rate %", "type": "number", "required": False},
                        {"key": "net_promoter_score", "label": "Net Promoter Score (NPS)", "type": "number", "required": False},
                        {"key": "operating_margin", "label": "Operating Margin %", "type": "number", "required": False},
                        {"key": "currency", "label": "Currency", "type": "string", "required": False}
                    ]
                }
            }
        ]

        created_count = 0
        updated_count = 0

        for template_data in templates_data:
            template, created = ExtractionTemplate.objects.get_or_create(
                name=template_data["name"],
                defaults={"schema_json": template_data["schema"]}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created template: {template.name}'))
                created_count += 1
            else:
                # Update existing template if schema changed
                if template.schema_json != template_data["schema"]:
                    template.schema_json = template_data["schema"]
                    template.save()
                    self.stdout.write(self.style.WARNING(f'↻ Updated template: {template.name}'))
                    updated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'○ Template already exists: {template.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Template seeding completed! Created: {created_count}, Updated: {updated_count}'))

