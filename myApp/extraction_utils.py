"""
Utilities for structured data extraction from PDFs
"""
import fitz  # PyMuPDF
import openai
from django.conf import settings
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file using PyMuPDF.
    Returns concatenated text from all pages.
    """
    doc = fitz.open(pdf_path)
    text_parts = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        text_parts.append(text)
    
    doc.close()
    return "\n\n".join(text_parts)


def extract_with_llm(document_text: str, template_schema: Dict) -> Dict[str, Any]:
    """
    Use LLM to extract structured data from document text based on template schema.
    Returns extracted JSON with values and evidence snippets.
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OpenAI API key not configured")
    
    # Build field descriptions for the prompt
    fields_desc = []
    for field in template_schema.get('fields', []):
        field_info = f"- {field['label']} ({field['key']}): {field['type']}"
        if field.get('required'):
            field_info += " [REQUIRED]"
        fields_desc.append(field_info)
    
    fields_text = "\n".join(fields_desc)
    
    # Limit text length to avoid token limits (keep first 8000 chars)
    text_preview = document_text[:8000] if len(document_text) > 8000 else document_text
    if len(document_text) > 8000:
        text_preview += "\n\n[... document continues ...]"
    
    system_prompt = """You are a data extraction assistant. Extract structured data from documents and return ONLY valid JSON.

For each field, provide:
- value: the extracted value (null if not found)
- source_snippet: a short quote from the document showing where you found it
- page_number: page number if available (null if not)

Return a JSON object with this structure:
{
  "fields": {
    "field_key": {
      "value": "extracted value or null",
      "source_snippet": "quote from document",
      "page_number": 1 or null
    }
  }
}

IMPORTANT:
- Output ONLY valid JSON, no markdown, no explanations
- Use null for missing values
- Dates should be in YYYY-MM-DD format
- Numbers should be numeric (no currency symbols in the number)
- Extract exactly what is in the document, don't infer"""
    
    user_prompt = f"""Extract the following fields from this document:

{fields_text}

Document text:
{text_preview}

Return ONLY the JSON object with extracted fields."""
    
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Low temperature for consistent extraction
            response_format={"type": "json_object"}  # Force JSON output
        )
        
        result_text = response.choices[0].message.content
        extracted_data = json.loads(result_text)
        
        # Transform to flat structure: {field_key: value, ...}
        # Also store evidence in a separate structure
        flat_data = {}
        evidence = {}
        
        if 'fields' in extracted_data:
            for field_key, field_data in extracted_data['fields'].items():
                flat_data[field_key] = field_data.get('value')
                evidence[field_key] = {
                    'source_snippet': field_data.get('source_snippet'),
                    'page_number': field_data.get('page_number')
                }
        
        return {
            'extracted': flat_data,
            'evidence': evidence
        }
    
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}")
    except Exception as e:
        raise ValueError(f"LLM extraction failed: {str(e)}")


def validate_extraction(extracted_data: Dict[str, Any], template_schema: Dict) -> Dict[str, Any]:
    """
    Validate extracted data against template schema.
    Returns validation results with errors, warnings, and field status.
    """
    errors = []
    warnings = []
    field_status = {}
    
    fields = template_schema.get('fields', [])
    
    for field in fields:
        field_key = field['key']
        field_label = field['label']
        field_type = field['type']
        is_required = field.get('required', False)
        
        value = extracted_data.get(field_key)
        
        # Check required fields
        if is_required and (value is None or value == ''):
            errors.append(f"{field_label} is required but not found")
            field_status[field_key] = 'error'
            continue
        
        if value is None or value == '':
            field_status[field_key] = 'ok'  # Optional field, missing is OK
            continue
        
        # Type validation
        if field_type == 'date':
            try:
                # Try to parse date
                datetime.strptime(str(value), '%Y-%m-%d')
                field_status[field_key] = 'ok'
            except (ValueError, TypeError):
                # Try other common date formats
                try:
                    datetime.strptime(str(value), '%m/%d/%Y')
                    warnings.append(f"{field_label} date format may need conversion")
                    field_status[field_key] = 'warning'
                except (ValueError, TypeError):
                    errors.append(f"{field_label} is not a valid date (expected YYYY-MM-DD)")
                    field_status[field_key] = 'error'
        
        elif field_type == 'number':
            try:
                # Remove currency symbols and commas
                clean_value = str(value).replace('$', '').replace(',', '').strip()
                float(clean_value)
                field_status[field_key] = 'ok'
            except (ValueError, TypeError):
                errors.append(f"{field_label} is not a valid number")
                field_status[field_key] = 'error'
        
        elif field_type == 'string':
            if not isinstance(value, str):
                errors.append(f"{field_label} should be text")
                field_status[field_key] = 'error'
            else:
                field_status[field_key] = 'ok'
        
        else:
            field_status[field_key] = 'ok'  # Unknown type, assume OK
    
    # Cross-field validation
    # Check: if currency exists, total_value should be numeric
    currency_key = None
    total_value_key = None
    
    for field in fields:
        if 'currency' in field['key'].lower():
            currency_key = field['key']
        if 'value' in field['key'].lower() or 'amount' in field['key'].lower():
            total_value_key = field['key']
    
    if currency_key and total_value_key:
        currency = extracted_data.get(currency_key)
        total_value = extracted_data.get(total_value_key)
        
        if currency and total_value:
            try:
                float(str(total_value).replace('$', '').replace(',', '').strip())
            except (ValueError, TypeError):
                warnings.append(f"Total value should be numeric when currency is present")
    
    # Check: effective_date should not be after termination_date
    effective_date_key = None
    termination_date_key = None
    
    for field in fields:
        if 'effective' in field['key'].lower() and 'date' in field['key'].lower():
            effective_date_key = field['key']
        if 'termination' in field['key'].lower() and 'date' in field['key'].lower():
            termination_date_key = field['key']
    
    if effective_date_key and termination_date_key:
        effective_date = extracted_data.get(effective_date_key)
        termination_date = extracted_data.get(termination_date_key)
        
        if effective_date and termination_date:
            try:
                eff_dt = datetime.strptime(str(effective_date), '%Y-%m-%d')
                term_dt = datetime.strptime(str(termination_date), '%Y-%m-%d')
                
                if eff_dt > term_dt:
                    warnings.append("Effective date is after termination date")
            except (ValueError, TypeError):
                pass  # Date parsing already handled above
    
    return {
        'errors': errors,
        'warnings': warnings,
        'field_status': field_status,
        'is_valid': len(errors) == 0
    }

