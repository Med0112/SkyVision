// ============================================================
// إعدادات Firebase - مشتركة بين الصفحة الرئيسية والأدمن
// ============================================================

// استيراد Firebase (باستخدام الـ CDN)
// هذا الملف سيتم تحميله في كل صفحة

const firebaseConfig = {
  apiKey: "AIzaSyBz44GsJG2KReo104A3f1OXQ0y4BZAXD0E",
  authDomain: "skyvision-90042.firebaseapp.com",
  databaseURL: "https://skyvision-90042-default-rtdb.firebaseio.com",
  projectId: "skyvision-90042",
  storageBucket: "skyvision-90042.firebasestorage.app",
  messagingSenderId: "911367796900",
  appId: "1:911367796900:web:e10b8324722bbc83a08e31",
  measurementId: "G-GWXZ3HEG5V"
};

// تهيئة Firebase (باستخدام الـ compat SDK)
firebase.initializeApp(firebaseConfig);

// المصادر المستخدمة في كل مكان
const db = firebase.firestore();
const auth = firebase.auth();

// (اختياري) تفعيل الإصدارات التجريبية
// firebase.analytics();

console.log('✅ Firebase initialized successfully!');