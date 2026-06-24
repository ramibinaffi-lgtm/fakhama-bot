import telebot
from telebot import types
import requests

# --- إعدادات التوكن والمفاتيح الخاصة بك الحقيقية ---
TOKEN = "8488546821:AAEwiOGIJHwkBqmsdZY4-xRpK9bKoIS3vRk"
SMM_API_KEY = "db14745b8c4060339f1e912d2f712f70"
SMM_API_URL = "https://secsers.com/api/v2"

bot = telebot.TeleBot(TOKEN)

# قاموس لتخزين مراحل الطلب لكل مستخدم
# الهيكل سيكون: { chat_id: {"service_id": "xxx", "quantity": "xxx", "state": "xxx"} }
user_status = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"🎯 أهلاً بك يا {user_name} في بوت الفخامة لرشق وتزويد المتابعين! 🔥\n\n"
        "🚀 نوفر لك أفضل وأسرع خدمات زيادة المتابعين والتفاعلات تلقائياً وبأقل الأسعار!"
    )

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📸 متابعين إنستغرام")
    btn2 = types.KeyboardButton("🎵 متابعين تيك توك")
    btn3 = types.KeyboardButton("👤 متابعين تليجرام")
    btn4 = types.KeyboardButton("💳 طرق الدفع وشحن الرصيد")
    btn5 = types.KeyboardButton("📞 التواصل مع الدعم")

    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4, btn5)

    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    # 🛑 1. استقبال رابط الحساب (الخطوة الأخيرة للطلب)
    if chat_id in user_status and user_status[chat_id].get("state") == "waiting_link":
        service_id = user_status[chat_id]["service_id"]
        quantity = user_status[chat_id]["quantity"]
        target_link = text  # الرابط المرسل من الزبون

        # مسح الحالة المؤقتة بعد أخذ البيانات
        del user_status[chat_id]

        bot.send_message(chat_id, "⏳ جاري إرسال طلبك تلقائياً إلى سيرفر الرشق... انتظر ثواني.")

        # تجهيز الطلب المحترف لموقع الـ SMM
        payload = {
            'key': SMM_API_KEY,
            'action': 'add',
            'service': service_id,
            'link': target_link,
            'quantity': quantity
        }

        try:
            response = requests.post(SMM_API_URL, data=payload)
            result = response.json()

            if "order" in result:
                order_id = result["order"]
                success_text = (
                    "✅ تم تنفيذ وتفعيل طلبك بنجاح!\n\n"
                    f"🆔 رقم الطلب بالسيرفر: {order_id}\n"
                    f"🔗 الرابط المستهدف: {target_link}\n"
                    f"📦 رقم الخدمة: {service_id}\n"
                    f"🔢 الكمية المطلوبة: {quantity}\n\n"
                    "⚡ يبدأ الرشق الآن تلقائياً خلال دقائق!"
                )
                bot.send_message(chat_id, success_text, parse_mode="Markdown")
            elif "error" in result:
                bot.send_message(chat_id, f"❌ حدث خطأ من سيرفر SMM الأساسي:\n`{result['error']}`", parse_mode="Markdown")
            else:
                bot.send_message(chat_id, "⚠️ تواصل مع الإدارة، السيرفر استلم الطلب بوضع غير معروف.")
        except Exception as e:
            bot.send_message(chat_id, f"❌ فشل الاتصال التلقائي بالسيرفر.\nالخطأ: {str(e)}")
        return

    # 🛑 2. استقبال الكمية المكتوبة يدوياً
    if chat_id in user_status and user_status[chat_id].get("state") == "waiting_quantity_text":
        if not text.isdigit():
            bot.send_message(chat_id, "❌ عذراً، يرجى إدخال كمية صحيحة (أرقام فقط):")
            return

        user_status[chat_id]["quantity"] = text
        user_status[chat_id]["state"] = "waiting_link"
        bot.send_message(chat_id, "🔗 ممتاز! أرسل الآن رابط الحساب أو القناة المستهدفة لبدء الرشق:")
        return

    # 🛑 3. قوائم الخدمات الرئيسية وأزرار الكيبورد العادي
    if text == "📸 متابعين إنستغرام":
        instagram_text = "⚡ اختر خدمة إنستغرام المطلوبة من السيرفر:"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("1️⃣ 1000 متابع (بدون ضمان) [2$]", callback_data="select_9961"))
        bot.send_message(chat_id, instagram_text, reply_markup=markup, parse_mode="Markdown")

    elif text == "🎵 متابعين تيك توك":
        tiktok_text = "⚡ اختر خدمة تيك توك المطلوبة من السيرفر:"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("1️⃣ 1000 متابع (حقيقي) [5$]", callback_data="select_9765"))
        bot.send_message(chat_id, tiktok_text, reply_markup=markup, parse_mode="Markdown")

    elif text == "👤 متابعين تليجرام":
        telegram_text = "⚡ اختر خدمة تليجرام المطلوبة من السيرفر:"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("1️⃣ 1000 عضو قنوات/مجموعات [3$]", callback_data="select_301"))
        bot.send_message(chat_id, telegram_text, reply_markup=markup, parse_mode="Markdown")

    elif text == "💳 طرق الدفع وشحن الرصيد":
        payment_text = (
            "💰 طرق الدفع المتوفرة لشحن رصيدك داخل البوت:\n\n"
            "🔹 محفظة باير (Payeer)\n"
            "🔹 عملات رقمية (USDT / TRON)\n\n"
            "يرجى التواصل مع الدعم لشحن حسابك يدوياً وتفعيل الرصيد تلقائياً."
        )
        bot.send_message(chat_id, payment_text, parse_mode="Markdown")

    elif text == "📞 التواصل مع الدعم":
        support_text = "🙋‍♂️ يسعدنا خدمتك في أي وقت! للتواصل مع إدارة البوت والشراء أو الشحن المباشر، راسلنا عبر الحساب التالي: @r78mi"
        bot.send_message(chat_id, support_text)
    
    else:
        bot.send_message(chat_id, "❌ عذراً، يرجى اختيار خدمة من الأزرار المتاحة بالأسفل.")


# 🛑 4. استقبال اختيار الخدمة وعرض أزرار الكمية للزبون
@bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
def callback_select_service(call):
    chat_id = call.message.chat.id
    service_id = call.data.split("_")[1]  # استخراج رقم الخدمة

    # حفظ رقم الخدمة في ذاكرة المستخدم المؤقتة
    user_status[chat_id] = {
        "service_id": service_id,
        "state": "waiting_quantity_select"
    }

    # إنشاء أزرار شفافة لاختيار الكمية
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("100", callback_data="qty_100"),
        types.InlineKeyboardButton("500", callback_data="qty_500")
    )
    markup.add(
        types.InlineKeyboardButton("1000", callback_data="qty_1000"),
        types.InlineKeyboardButton("2500", callback_data="qty_2500")
    )
    markup.add(types.InlineKeyboardButton("✏️ كتابة كمية مخصصة", callback_data="qty_custom"))

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, f"🔢 رقم الخدمة المختار هو ({service_id}).\n\nيرجى تحديد أو اختيار الكمية المطلوبة للرشق الآن:", reply_markup=markup, parse_mode="Markdown")


# 🛑 5. استقبال تحديد الكمية والانتقال لطلب رابط الحساب
@bot.callback_query_handler(func=lambda call: call.data.startswith("qty_"))
def callback_select_quantity(call):
    chat_id = call.message.chat.id
    qty_type = call.data.split("_")[1]

    if chat_id not in user_status:
        bot.send_message(chat_id, "❌ انتهت الجلسة، يرجى الضغط على /start والبدء من جديد.")
        return

    if qty_type == "custom":
        # إذا اختار كتابة كمية بنفسه
        user_status[chat_id]["state"] = "waiting_quantity_text"
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, "✍️ قم بكتابة الكمية المطلوبة برقم واضح الآن (مثال: 350):")
    else:
        # إذا اختار كمية جاهزة من الأزرار
        user_status[chat_id]["quantity"] = qty_type
        user_status[chat_id]["state"] = "waiting_link"
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, "🔗 ممتاز! أرسل الآن رابط الحساب أو القناة المستهدفة لبدء الرشق التلقائي:")


print("بوت الفخامة الاحترافي المطور يعمل الآن ومستعد لاستقبال الطلبات...")
bot.infinity_polling(timeout=10, long_polling_timeout=5)