import os
import smtplib
from email.message import EmailMessage

from utils.system_messages import SYSTEM_MESSAGE_COMPARISON
import config
import openai

class SummaryComparator:
    """
    A class responsible for comparing summaries using OpenAI's ChatCompletion API
    and sending the comparison results via email.
    """

    def __init__(self, engine="gpt-4o"):
        """
        Initializes the SummaryComparator with the specified OpenAI engine.

        :param engine: The OpenAI model engine to use for comparisons (default: "gpt-4o").
        """
        self.engine = engine

    def compare_summaries(self, original_summary, neighbor_summaries):
        """
        Compares the original summary with multiple neighbor summaries using OpenAI in a single comparison.

        :param original_summary: The summary of the newly processed PDF.
        :param neighbor_summaries: A list of summaries from the nearest neighbors.
        :return: The combined differences between the original summary and all neighbor summaries.
        """

        combined_neighbor_summaries = "\n\n".join([f"Neighbor {idx+1} Summary:\n{summary}"
                                                   for idx, summary in enumerate(neighbor_summaries)])

        input_text = (
            f"Original Summary:\n{original_summary}\n\n"
            f"Combined Neighbor Summaries:\n{combined_neighbor_summaries}\n\n"
            f"Please provide the key differences between the original summary and the combined neighbor summaries."
        )

        try:
            response = openai.ChatCompletion.create(
                engine=self.engine,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGE_COMPARISON},
                    {"role": "user", "content": input_text}
                ],
                max_tokens=3000
            )
            comparison_result = response['choices'][0]['message']['content'].strip()
            self.send_email(comparison_result)
            return comparison_result
        except Exception as e:
            config.app_logger.error(f"Error comparing summaries: {str(e)}")
            return "Error comparing summaries."

    def send_email(self, comparison_result):
        """
        Sends the comparison result via email.

        :param comparison_result: The comparison result to include in the email.
        """

        sender_email = os.getenv('EMAIL_ADDRESS')
        sender_password = os.getenv('EMAIL_PASSWORD')
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT'))
        receiver_email = os.getenv('TO_EMAIL')

        subject = "Summary Comparison Results"
        body = f"Comparison Result:\n{comparison_result}"

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(body)

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                config.app_logger.info("Email sent successfully to %s", receiver_email)
        except Exception as e:
            config.app_logger.error("Failed to send email: %s", str(e))

