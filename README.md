# 🎬 ESHMAT — Rasmiy Jonli Veb-Portali

Ushbu loyiha YouTube'dagi **Eshmat** (`@Eshmats`) kanali uchun maxsus yaratilgan to'liq va real-vaqtda jonli sinxronlanuvchi veb-saytdir.

- **Dasturchi:** [@Laziz_Abduahadov](https://t.me/Laziz_Abduahadov)
- **Kanal:** [https://www.youtube.com/@Eshmats](https://www.youtube.com/@Eshmats)
- **Rasmiy Telegram:** [https://t.me/eshmats_uz](https://t.me/eshmats_uz)

---

## 📂 Papka tarkibi

1. `index.html` — Barcha FontAwesome 6 iconlar, Kinozal Video Pleyeri, jonli hisoblagichlar va interaktiv filtrlarga ega frontend sahifa.
2. `server.py` — YouTube sahifasi va rasmiy RSS lentasidan jonli obunachilar va yangi videolarni avtomatik tortib oluvchi Python server.
3. `eshmat_avatar.jpg` — Eshmat kanalining asl 500x500 HD sifatdagi profil logotipi.
4. `run.sh` — 1 ta buyruq orqali saytni ishga tushiruvchi qulay skript.

---

## 🚀 Qanday ishga tushiriladi?

Terminalda ushbu papkaga kiring va buyruqni bering:

```bash
cd /home/abdulaziz/.gemini/antigravity/scratch/eshmat_official
./run.sh
```

Yoki to'g'ridan-to'g'ri Python orqali:

```bash
python3 server.py
```

So'ng brauzeringizda oching:
👉 **http://localhost:8000**

---

## ⚡ Asosiy imkoniyatlar

- **Jonli obunachilar:** YouTube'da obunachilar oshganda saytda avtomatik ko'payadi.
- **Avtomatik yangi videolar:** Kanalda yangi video yuklanganda saytga avtomatik "Yangi" nishoni bilan qo'shiladi.
- **Kinozal Pleyeri:** Har qanday video bosilganda butun ekranda qulay teatr rejimida ochiladi.
- **Tasodifiy video tanlash:** "Nimani ko'rishni bilmayapsizmi?" interaktiv zarlar tugmasi.
- **Toifalar bo'yicha saralash:** "30 Kunlik Sinovlar", "Zombi & Sarguzasht", "Ibratli Hikoyalar" va "Eng ommabop".
- **Dasturchi muallifligi:** `@Laziz_Abduahadov`
