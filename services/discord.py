import requests
import json
import os

def send_to_discord(report_data, pdf_filepath, settings):
    """Sends the report details and PDF to a Discord channel via bot token."""
    bot_token = settings.get('botToken')
    channel_id = settings.get('channelId')
    applicant_name = settings.get('applicantName', 'N/A')
    applicant_email = settings.get('applicantEmail', 'N/A')

    if not bot_token or not channel_id:
        return False, "Discord Bot Token or Channel ID missing"

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    headers = {
        "Authorization": f"Bot {bot_token}"
    }

    message_content = f"""
**New Company Research Report Generated!**

**Applicant Details:**
- **Name:** {applicant_name}
- **Email:** {applicant_email}

**Research Details:**
- **Company Name:** {report_data.get('companyName')}
- **Company Website:** {report_data.get('website')}
    """

    data = {
        "content": message_content
    }

    try:
        # Check if PDF exists
        if os.path.exists(pdf_filepath):
            with open(pdf_filepath, 'rb') as f:
                files = {
                    'file': ('report.pdf', f, 'application/pdf')
                }
                # When sending files, payload_json must be used for the message content
                response = requests.post(url, headers=headers, data={'payload_json': json.dumps(data)}, files=files, timeout=20)
        else:
            # Send without file
            response = requests.post(url, headers=headers, json=data, timeout=20)
            
        response.raise_for_status()
        return True, "Message sent successfully"
    except Exception as e:
        print(f"Discord API Error: {e}")
        return False, str(e)
