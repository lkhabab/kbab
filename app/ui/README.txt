# Agri 3D Login — UI (Vite + React)

## تشغيل محلياً
1) افتح Terminal داخل هذا المجلد (agri3d_login_ui)
2) ثبّت الحزم:
   npm i
3) شغّل التطوير:
   npm run dev
   ثم افتح:  http://localhost:5173/

## بناء نسخة إنتاجية (اختياري)
npm run build
ستجد الملفات الجاهزة داخل مجلد dist/

---
ملاحظات:
- لو المتصفح لا يدعم WebGL، ستظهر خلفية CSS متحركة كبديل.
- المكوّن الرئيسي موجود في: src/Agri3DLogin.jsx
- نقطة الدخول: src/main.jsx
- لو أردت الربط مع Flask لاحقاً، غيّر outDir في vite.config.js
  إلى المسار الذي تريده داخل static/ ثم استخدم الروابط في القالب.
