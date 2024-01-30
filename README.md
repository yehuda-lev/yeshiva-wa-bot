# השטייגעניסט המעופף ✈️


## הקוד הבא הוא בוט ב-WhatsApp שבניתי עם ספריית [PyWa](https://pywa.readthedocs.io/) ל-WhatsApp Cloud API

## הבוט נבנה בכדי לסמן בחורים שהיו בסדרי הישיבה ולהוסיף להם נקודות למבצע חו"ל שהישיבה עושה.

### הבוט עושה שימוש עיקרי בפיצ'ר ה-[Flows](https://pywa.readthedocs.io/en/latest/content/flows/overview.html)

[![לצפייה בסרטוון ביוטיוב](http://img.youtube.com/vi/OAinkmA9hZU/0.jpg)](https://youtu.be/OAinkmA9hZU?si=CdNNLuFLHsq7VWqB "בוט בווצאפ  - השטייגעניסט המעופף")



# התקנה:
```bash
# 1. clone the repository
git clone https://github.com/yehuda-lev/yeshiva-wa-bot.git
# 2. Enter the project:
cd yeshiva-wa-bot
# 3. Create a virtual environment named `venv`:
python3 venv -m venv venv
# 4. Activate the virtual environment:
source venv/bin/activate
# 5. Install the required dependencies by running the command: 
pip3 install -r requirements.txt
# 6. Copy the env example to env file:
cp env.example .env
# 7. Edit the .env file :
nano .env
# 8. Install and run ngrok on port 8080
ngrok http http://localhost:8080
# 10. run the code: 
python3 main.py
```
### בקובץ ה .env יש להזין את הפרטים הבאים:

> ניתן ליצור אפליקצייה ב facebook developers ע"פ המדריך [הבא](https://pywa.readthedocs.io/en/latest/content/getting-started.html#create-a-whatsapp-application)
- `WA_PHONE_ID` `WA_BUSINESS_ID` `WA_VERIFY_TOKEN` `WA_TOKEN` `WA_PHONE_NUMBER`
- `APP_ID` ו- `APP_SECRET` ניתן להשיג ב > app settings > Basic
- `CALLBACK_URL` ו- `WEBHOOK_ENDPOINT` שנוצרו במערכת
- `WA_ADMINS` - משתמשים שיוגדרו כמנהלים
- `FLOW_ID` - ראה את [create_flows.py](create_flows.py)
- כעת עליכם ליצור את הקבצים `private.pem` ו `public.pem` עם סיסמה שלכם. פרטים נוספים ניתן לראות
- יצירת קבצי private.pem ו- public.pem - [פרטים נוספים כאן](https://pywa.readthedocs.io/en/latest/content/flows/overview.html#handling-flow-requests-and-responding-to-them)
- `PASSWORD_PRIVATE_KEY` - סיסמה לקובץ `private.pem`
- `PATH_DATA_BASE` - נתיב לקובץ ה-database

## קרדיט
הקוד נכתב ע"י [@yehudalev](https://t.me/yehudalev)
