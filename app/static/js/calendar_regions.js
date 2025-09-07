(function(){
  const pills = document.querySelectorAll(".season-pill");
  const cols  = document.querySelectorAll(".month-col");
  const cmpA  = document.getElementById("cmpA");
  const cmpB  = document.getElementById("cmpB");
  const cmpBtn= document.getElementById("cmpBtn");
  const cmpResult = document.getElementById("cmpResult");
  const regionSel = document.getElementById("regionSel");

  const first = document.querySelector('.season-pill[data-sel="all"]');
  if(first){ first.classList.add("active"); }

  pills.forEach(p=>{
    p.addEventListener("click", ()=>{
      pills.forEach(x=>x.classList.remove("active"));
      p.classList.add("active");
      const sel = p.dataset.sel;
      cols.forEach(col=>{
        if(sel==="all"){ col.style.display = ""; return; }
        col.style.display = (col.dataset.season===sel) ? "" : "none";
      });
    });
  });

  cmpBtn && cmpBtn.addEventListener("click", ()=>{
    const a = cmpA.value, b = cmpB.value;
    if(!a || !b){ cmpResult.textContent = "اختار شهرين للمقارنة."; return; }
    cmpResult.textContent = `مقارنة سريعة بين ${a} و ${b}: راجع المحاصيل والنصائح المناسبة لكل واحد.`;
  });

  const modalEl = document.getElementById('detailsModal');
  const titleEl = document.getElementById('detailsTitle');
  const bodyEl  = document.getElementById('detailsBody');
  const modal = modalEl ? new bootstrap.Modal(modalEl) : null;

  document.querySelectorAll(".more-btn").forEach(btn=>{
    btn.addEventListener("click", ()=>{
      const m = btn.dataset.month;
      const s = btn.dataset.season;
      const d = btn.dataset.details || "";
      const regData = JSON.parse(btn.dataset.regions || "{}");
      const region = regionSel.value;
      titleEl.textContent = `تفاصيل شهر ${m}`;
      let regionHtml = "";
      if(region && regData[region]){
        regionHtml = "<hr><div><strong>نصائح لمنطقة "+region+" :</strong><ul>";
        regData[region].forEach(line=> regionHtml += "<li>• "+escapeHtml(line)+"</li>");
        regionHtml += "</ul></div>";
      }else if(region){
        regionHtml = "<hr><div class='text-muted small'>ما في نصائح مخصصة للمنطقة المحددة — بنعرض النصائح العامة.</div>";
      }
      bodyEl.innerHTML = `
        <div class="mb-2"><span class="badge bg-info">${seasonLabel(s)}</span></div>
        <div style="white-space:pre-wrap; line-height:1.8">${escapeHtml(d)}</div>
        ${regionHtml}
      `;
      modal && modal.show();
    });
  });

  function seasonLabel(s){
    switch(s){
      case "winter": return "الشتاء";
      case "hotdry": return "الصيف (حار وجاف)";
      case "rainy":  return "الخريف";
      default:       return "الخريف المتأخر/الربيع";
    }
  }
  function escapeHtml(t){
    return t.replace(/[&<>"']/g, (c)=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;', "'":'&#39;'}[c]));
  }
})();