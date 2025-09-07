const chat = document.getElementById('chat');
const form = document.getElementById('chatForm');
const input = document.getElementById('msg');
document.getElementById('clear').onclick = () => chat.innerHTML='';
form.onsubmit = async () => {
  const text = input.value.trim();
  if(!text) return;
  input.value='';
  add('user', text);
  // واجهة فقط: ردّ ثابت. استبدل بطلب fetch('/api/chat', {method:'POST', ...})
  setTimeout(()=> add('bot', 'سأجيبك حين تربطني بالباك-إند 🌱. اسأل عن الريّ، التسميد، أو التقويم.'), 400);
};
function add(who, text){
  const row = document.createElement('div');
  row.className = 'bubble ' + (who==='user'?'me':'bot');
  row.textContent = text;
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}
