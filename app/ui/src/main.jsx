import React from "react";
import { createRoot } from "react-dom/client";
import Agri3DLogin from "./Agri3DLogin.jsx";

<form method="POST" action="/auth/login">
  <input name="username" required placeholder="اسم المستخدم" />
  <input name="password" type="password" required placeholder="كلمة المرور" />
  <label>
    <input type="checkbox" name="remember" /> تذكّرني
  </label>

  {/* اختياري: لو تبغى توجه المستخدم لواجهة محددة بعد تسجيل الدخول */}
  <input type="hidden" name="next" value="/" />

  <button type="submit">دخول</button>
</form>

createRoot(document.getElementById("root")).render(<Agri3DLogin />);
