from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from dotenv import load_dotenv
import resend
import os

load_dotenv(override=True)

def send_email(subject: str, html_body: str):
    resend.api_key = os.getenv("RESEND_API_KEY")
    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": "your_email@random.com",
        "subject": subject,
        "html": html_body,
    }
    resend.Emails.send(params)
    return "Email sent successfully"

class EmailToolInput(BaseModel):
    subject: str = Field(..., description="The subject of the email")
    html_body: str = Field(..., description="The body of the email")


class EmailTool(BaseTool):
    name: str = "Email Tool"
    description: str = "Send an email to a recipient"
    args_schema: Type[BaseModel] = EmailToolInput

    def _run(self, subject: str, html_body: str) -> str:
        resend.api_key = os.getenv("RESEND_API_KEY")
        return send_email(subject, html_body)
        