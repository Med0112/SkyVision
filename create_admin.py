import requests
import json
import getpass
import sys
import datetime

# ===================================================================
# إعدادات Firebase (من config الخاص بك)
# ===================================================================
API_KEY = "AIzaSyBz44GsJG2KReo104A3f1OXQ0y4BZAXD0E"
PROJECT_ID = "skyvision-90042"

# ===================================================================
# دوال مساعدة للـ REST API
# ===================================================================

def create_user(email, password):
    """
    إنشاء مستخدم جديد في Firebase Authentication عبر REST API.
    تُرجع (user_id, id_token, error_message)
    """
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    response = requests.post(url, json=payload)
    data = response.json()
    
    if response.status_code == 200:
        user_id = data.get("localId")
        id_token = data.get("idToken")
        return user_id, id_token, None
    else:
        error = data.get("error", {}).get("message", "خطأ غير معروف")
        return None, None, error

def set_user_role_in_firestore(uid, email, id_token):
    """
    إضافة وثيقة في مجموعة 'users' مع دور 'admin' باستخدام Firestore REST API.
    نستخدم id_token للمصادقة.
    """
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/users/{uid}"
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json"
    }
    user_data = {
        "fields": {
            "email": {"stringValue": email},
            "role": {"stringValue": "admin"},
            "displayName": {"stringValue": "مدير النظام"},
            "active": {"booleanValue": True},
            "createdAt": {"timestampValue": datetime.datetime.utcnow().isoformat() + "Z"}
        }
    }
    response = requests.patch(url, headers=headers, json=user_data)
    return response.status_code in (200, 201)

# ===================================================================
# البرنامج الرئيسي
# ===================================================================
def main():
    print("=" * 50)
    print("🔐 إنشاء حساب أدمن جديد في Sky Vision (عبر REST API)")
    print("=" * 50)
    
    email = input("📧 أدخل البريد الإلكتروني للأدمن: ").strip()
    password = getpass.getpass("🔑 أدخل كلمة المرور (على الأقل 6 أحرف): ").strip()
    confirm = getpass.getpass("🔄 أعد إدخال كلمة المرور للتأكيد: ").strip()
    
    if not email or "@" not in email:
        print("❌ البريد الإلكتروني غير صحيح.")
        return
    
    if len(password) < 6:
        print("❌ كلمة المرور يجب أن تكون 6 أحرف أو أكثر.")
        return
    
    if password != confirm:
        print("❌ كلمتا المرور غير متطابقتين.")
        return
    
    print("\n⏳ جاري إنشاء المستخدم ...")
    
    # 1. إنشاء المستخدم في Authentication
    uid, id_token, error = create_user(email, password)
    if error:
        if "EMAIL_EXISTS" in error:
            print("❌ هذا البريد الإلكتروني مستخدم بالفعل.")
        elif "WEAK_PASSWORD" in error:
            print("❌ كلمة المرور ضعيفة جداً.")
        else:
            print(f"❌ فشل إنشاء المستخدم: {error}")
        return
    
    print(f"✅ تم إنشاء المستخدم في Authentication (UID: {uid})")
    
    # 2. إضافة دور 'admin' في Firestore
    if set_user_role_in_firestore(uid, email, id_token):
        print("✅ تم تسجيل دور 'admin' في Firestore بنجاح.")
    else:
        print("⚠️ تم إنشاء المستخدم لكن فشل إضافة الدور في Firestore. حاول يدوياً.")
    
    print("\n🎉 اكتمل الإعداد!")
    print(f"📧 البريد: {email}")
    print(f"🔑 كلمة المرور: (التي أدخلتها)")
    print("\n💡 استخدم هذه البيانات لتسجيل الدخول إلى لوحة الإدارة (admin.html).")

if __name__ == "__main__":
    main()