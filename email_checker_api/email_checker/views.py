from rest_framework.decorators import api_view
from rest_framework.response import Response
from concurrent.futures import ThreadPoolExecutor
import smtplib
import dns.resolver
import dns.exception


def check_email(email):
    username, domain = email.split("@")

    try:
        records = dns.resolver.resolve(domain, "MX")
        mx_records = [record.exchange.to_text() for record in records]
        cox_mx_records = [
            mx_record for mx_record in mx_records
        ]
        if not cox_mx_records:
            return {"email": email, "exists": 'Mx_Not_Found'}
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(cox_mx_records[0])
        server.helo(server.local_hostname)
        server.mail("")
        response = server.rcpt(email)
        if response[0] == 250:
            return {"email": email, "exists": True}
        else:
            return {"email": email, "exists": False}
        server.quit()

    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.exception.DNSException,
        smtplib.SMTPConnectError,
        smtplib.SMTPServerDisconnected,
    ):
        return {"email": email, "exists": 'Recheck'}


@api_view(["POST"])
def check_emails(request):
    email_list = request.data.get("email_list",[])
    results = check_email(email_list)
    

    return Response(results)
