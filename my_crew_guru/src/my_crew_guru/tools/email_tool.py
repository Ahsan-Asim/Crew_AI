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
        "to": "ahsan.new252@gmail.com",
        "subject": subject,
        "html": html_body,
    }
    resend.Emails.send(params)
    return "Email sent successfully"

class EmailToolInput(BaseModel):
    location: str = Field(..., description="Location for the travel plan")
    forecast: str = Field(..., description="Weather forecast for the trip")
    packing_tips: str = Field(..., description="Packing tips for the trip")

class EmailTool(BaseTool):
    name: str = "Email Tool"
    description: str = "Send a travel plan email with dynamic content"
    args_schema: Type[BaseModel] = EmailToolInput

    subject_template: str = "Travel and Weather Plan for {location} Trip"
    body_template: str = """
    <html>
    <body>
        <p>Hello traveler!</p>
        <p>Here's the plan for your <strong>{location}</strong> trip:</p>

        <h3>Weather Forecast:</h3>
        <p>{forecast}</p>

        <h3>Packing Tips:</h3>
        {packing_tips}

        <p>Have a great trip!</p>
    </body>
    </html>
    """

    def _run(self, location: str, forecast: str, packing_tips: str) -> dict:
        # Wrap packing tips in <ul><li> if it's multiline text
        if not packing_tips.strip().startswith("<ul>"):
            tips_lines = packing_tips.split("\n")
            html_tips = "<ul>\n"
            for line in tips_lines:
                if line.strip():
                    html_tips += f"<li>{line.strip()}</li>\n"
            html_tips += "</ul>"
        else:
            html_tips = packing_tips

        subject = self.subject_template.format(location=location)
        body = self.body_template.format(
            location=location,
            forecast=forecast,
            packing_tips=html_tips
        )

        confirmation_msg = send_email(subject, body)
        return {"confirmation": confirmation_msg}

