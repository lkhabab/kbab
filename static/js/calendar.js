const data = [
  {m:'يناير', s:'شتاء', tips:['فحص ريّ خفيف + تسميد بسيط','تحضير لزراعة مبكرة حيث يلزم']},
  {m:'فبراير', s:'شتاء', tips:['عزق ومكافحة حشائش','بطاطس/بقوليات – تسميد متوازن']},
  {m:'مارس', s:'الصيف (دار وحاف)', tips:['بداية سخانة ظِل للشتلات','تجهيز أرض الصيف']},
  {m:'أبريل', s:'الصيف (دار وحاف)', tips:['مطاعم/رامية صيفية','ذرة رفيعة مبكرة']},
  {m:'مايو', s:'الصيف (دار وحاف)', tips:['استعداد للزرفة؛ صيانة مصارف','بذور مخزنة']},
  {m:'يونيو', s:'الصيف (دار وحاف)', tips:['التحضير قبل الأمطار','رشّ وقائي ذرة/سمسم/فول']},
  {m:'يوليو', s:'الخريف', tips:['بذر الزرفة: ذرة/سمسم/فول','كشف مصارف']},
  {m:'أغسطس', s:'الخريف', tips:['بطح؛ وقت مناسب','تسميد ذرة/سمسم','وقاية فطرية']},
  {m:'سبتمبر', s:'الخريف', tips:['نضج جزئي/جنيّ','ريّ خفيف']},
  {m:'أكتوبر', s:'الخريف/آخر الصيف', tips:['مطاعم/رامية؛ بداية موسم','رقابة حشائش مبكرة']},
  {m:'نوفمبر', s:'الشتاء', tips:['قمح/بقوليات','فول مصري/حمص']},
  {m:'ديسمبر', s:'الشتاء', tips:['خضروات ورقية شتوية','ريّ خفيف']},
];
const monthsEl = document.getElementById('months');
const seasonSel = document.getElementById('season');
function render(){
  const sel = seasonSel.value;
  monthsEl.innerHTML = '';
  data.filter(x => sel==='all' || x.s===sel).forEach(x => {
    const col = document.createElement('div');
    col.className = 'col-md-4 col-lg-3';
    col.innerHTML = `
      <div class="card glass p-3 h-100">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <span class="badge text-bg-info">${x.s}</span>
          <h5 class="m-0">${x.m}</h5>
        </div>
        <ul class="small text-secondary mb-0">${x.tips.map(t=>`<li>${t}</li>`).join('')}</ul>
      </div>`;
    monthsEl.appendChild(col);
  });
}
seasonSel.addEventListener('change', render);
render();
