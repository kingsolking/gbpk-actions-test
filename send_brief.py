import psycopg2
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Connect to Supabase Postgres
conn = psycopg2.connect("YOUR_SUPABASE_DATABASE_URL")
cur = conn.cursor()

# Example: Pull latest 12 company updates
cur.execute("""
SELECT company, headline, amount, category, source_url
FROM briefs
ORDER BY created_at DESC
LIMIT 12
""")
rows = cur.fetchall()

# Format email content
today = datetime.now().strftime("%b %d, %Y")
body_lines = [f"🔥 **Daily GBPK Brief — {today}**\n"]
for r in rows:
    company, headline, amount, category, source_url = r
    body_lines.append(f"• **{company}** {headline} ({category}) — [{amount}]({source_url})")
body = "\n".join(body_lines)

# Send the email
msg = MIMEText(body, "plain")
msg["Subject"] = f"Daily GBPK Brief — {today}"
msg["From"] = "YOUR_EMAIL@gmail.com"
msg["To"] = "YOUR_EMAIL@gmail.com"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("YOUR_EMAIL@gmail.com", "YOUR_APP_PASSWORD")
server.send_message(msg)
server.quit()

cur.close()
conn.close()
print("✅ Email sent successfully!")
