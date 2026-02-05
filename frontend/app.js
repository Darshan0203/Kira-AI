const chat = document.getElementById("chat")
const input = document.getElementById("input")
const historyDiv = document.getElementById("history")

// -------- UI helpers --------

function addBubble(text, side){
  const wrap = document.createElement("div")
  wrap.className = side === "user" ? "text-right" : "text-left"

  wrap.innerHTML = `
    <span class="inline-block bg-zinc-800 p-2 rounded max-w-[70%]">
      ${text}
    </span>
  `

  chat.appendChild(wrap)
  chat.scrollTop = chat.scrollHeight
}

// -------- New Chat --------

function newChat(){
  chat.innerHTML = ""
}

// -------- Send Message --------

async function send(){
  const msg = input.value.trim()
  if(!msg) return
  input.value = ""

  // USER bubble (append only)
  addBubble(msg,"user")

  try{
    const res = await fetch("http://localhost:8000/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:msg})
    })

    const data = await res.json()

    // AI bubble (append only)
    addBubble(data.answer || "No response","ai")

    // refresh sidebar ONLY
    loadHistory()

  }catch{
    addBubble("Backend not running.","ai")
  }
}

// -------- Sidebar History --------

async function loadHistory(){
  const res = await fetch("http://localhost:8000/history")
  const data = await res.json()

  historyDiv.innerHTML=""

  data.slice().reverse().forEach(h=>{
    const btn = document.createElement("button")
    btn.className="block w-full text-left text-sm p-2 hover:bg-zinc-800 rounded"
    btn.innerText = h.user.slice(0,30)

    // Load ONLY when clicked
    btn.onclick = ()=>{
      chat.innerHTML=""
      addBubble(h.user,"user")
      addBubble(h.ai,"ai")
    }

    historyDiv.appendChild(btn)
  })
}

// Initial sidebar load
loadHistory()
