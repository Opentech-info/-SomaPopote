# 🎓 SomaPopote - Elimu kwa Simu Yako

**SomaPopote** ni jukwaa la kielimu linalotumia teknolojia ya simu ya mkononi kutoa elimu bora kwa wanafunzi Tanzania. Mradi huu unawawezesha wanafunzi kupata elimu kupitia USSD, SMS, sauti, na wavuti bila hitaji la mtandao wa internet.

## 🌟 Vipengele Vikuu

### 1. **USSD Learning**
- Piga `*384*200#` kuanza kujifunza
- Menyu rahisi ya kusoma na kujibu maswali
- Hakuna hitaji la mtandao wa internet
- Inafanya kazi kwenye simu yoyote ya mkononi

### 2. **Gamification & Rewards**
- Shinda pointi kwa kujibu maswali sahihi
- Pokea airtime kama zawadi ya kujifunza
- Michuano ya kila siku na wiki
- Mfumo wa "streak" kwa ajili ya kujifunza kwa muda mrefu

### 3. **Mawasiliano ya Wazazi na Walimu**
- Wazazi wanaweza kuona maendeleo ya mtoto kupitia USSD
- Walimu wanatuma ujumbe kwa wingi kwa wazazi
- Ripoti za mahudhurio na matokeo
- Mawasiliano ya moja kwa moja kati ya shule na nyumbani

### 4. **Somo kwa Sauti (IVR)**
- Kwa watu wanaopenda kusikiliza au walemavu
- Piga simu na usikilize somo kwa sauti
- Masomo kwa lugha ya Kiswahili na English
- Inafanya kazi bila hitaji la kusoma

### 5. **Dashboard ya Wavuti**
- Walimu wanatengeneza na kusimamia masomo
- Ufuatiliaji wa maendeleo ya wanafunzi
 Takwimu na ripoti za kielimu
- Mawasiliano na wazazi

## 🛠️ Teknolojia Zilizotumika

### Backend
- **Python 3.8+** - Lugha kuu ya programu
- **Flask** - Web framework
- **SQLite** - Hifadhidata (inaweza kubadilishwa na PostgreSQL)
- **Africa's Talking API** - USSD, SMS, Voice, na Airtime

### Frontend
- **HTML5, CSS3, JavaScript** - Tehama za wavuti
- **Bootstrap 5** - CSS framework
- **Font Awesome** - Icons

### Deployment
- **Heroku/Render** - Hosting (kwa ajili ya demo)
- **Docker** - Containerization (hiari)

## 📂 Muundo wa Mradi

```
somapopote/
│
├── app.py                 # Flask entry point
├── requirements.txt       # Dependencies
├── database.py           # SQLite/PostgreSQL handler
├── README.md             # Hati hii
│
├── services/
│   ├── ussd.py           # USSD logic na menu navigation
│   ├── sms.py            # SMS notifications na quizzes
│   ├── voice.py          # Voice lessons (IVR)
│   └── gamification.py   # Airtime rewards logic
│
├── templates/
│   ├── index.html        # Landing page
│   └── dashboard.html    # Teacher/parent dashboard
│
└── static/
    ├── css/              # Styles
    ├── js/               # Scripts
    └── images/           # Branding (logo, icons)
```

## 🚀 Kuanzisha Mradi

### 1. Weka Dependencies
```bash
pip install -r requirements.txt
```

### 2. Sanidi Mazingira
```bash
# Weka vitu vya mazingira (kwa ajili ya uzalishaji)
export AFRICASTALKING_USERNAME='your_username'
export AFRICASTALKING_API_KEY='your_api_key'
export FLASK_ENV='development'
```

### 3. Anzisha App
```bash
python app.py
```

App itaanza kwenye `http://localhost:5000`

## 📱 Jinsi ya Kuitumia

### Kwa Wanafunzi:
1. **Piga USSD**: `*384*200#`
2. **Chagua somo** kutoka kwenye menyu
3. **Soma maelezo** ya somo
4. **Jaribu maswali** na ushinde pointi
5. **Pokea airtime** kama zawadi

### Kwa Wazazi:
1. **Piga USSD**: `*384*200#`
2. **Chagua "Wazazi & Walimu"**
3. **Angalia maendeleo** ya mtoto
4. **Pokea ripoti** za mahudhurio

### Kwa Walimu:
1. **Fungua dashboard**: `http://localhost:5000/dashboard`
2. **Tengeneza masomo** mapya
3. **Tuma ujumbe** kwa wazazi
4. **Fuatilia maendeleo** ya wanafunzi

## 🔧 Sanidi Africa's Talking API

### 1. Jisajili kwenye [Africa's Talking](https://africastalking.com/)
2. Pata username na API key
3. Weka credentials kwenye mazingira:
```python
# services/sms.py na services/voice.py
USERNAME = 'your_username'
API_KEY = 'your_api_key'
```

### 4. Weka USSD callback URL:
- Kwenye dashboard ya Africa's Talking, weka:
  `http://your-domain.com/ussd` kama callback URL

## 📊 Hifadhidata

Mradi unatumia SQLite kwa ajili ya demo, lakini unaweza kubadilisha kuwa PostgreSQL kwa ajili ya uzalishaji:

### Mfumo wa Hifadhidata:
- **users** - Maelezo ya wanafunzi
- **user_progress** - Maendeleo ya kujifunza
- **quiz_results** - Matokeo ya majaribio
- **lessons** - Masomo yaliyotengenezwa
- **rewards** - Pointi na zawadi
- **attendance** - Mahudhurio
- **teachers** - Walimu
- **bulk_messages** - Ujumbe kwa wingi

## 🏆 Gamification System

### Aina za Tuzo:
- **Quiz Correct**: 10 points + Tsh 100 airtime
- **Lesson Completed**: 5 points + Tsh 50 airtime
- **Daily Streak**: 20 points + Tsh 200 airtime
- **Weekly Top**: 50 points + Tsh 500 airtime

### Mfumo wa Pointi:
- Pointi zinakusanywa kwa kila somo
- Wanafunzi wanaweza kubadilisha pointi kwa tuzo
- Leaderboard ya kila wiki
- Badges na achievements

## 🔒 Usalama

- **Data Encryption**: Mawasiliano yanasimbwa kwa HTTPS
- **Input Validation**: Kila input inathibitishwa
- **Rate Limiting**: Kuzuia matumizi mabaya
- **Secure API**: Credentials zinahifadhiwa kama environment variables

## 📈 Scalability

### Kwa ajili ya uzalishaji:
1. **Badilisha database** kutoka SQLite kwenda PostgreSQL
2. **Tumia Redis** kwa ajili ya cache
3. **Load balancing** kwa ajili ya traffic nyingi
4. **Monitoring** na logging

## 🤝 Michango
