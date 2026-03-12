const chatbox = document.getElementById("chatbox")
const input = document.getElementById("userInput")

function addUserMessage(text){

const row = document.createElement("div")
row.className = "message user-row"

row.innerHTML = `
<div class="avatar user-avatar">👤</div>
<div class="bubble user-bubble">${text}</div>
`

chatbox.appendChild(row)

}

function addBotMessage(text){

const row = document.createElement("div")
row.className = "message bot-row"

row.innerHTML = `
<div class="avatar bot-avatar">🤖</div>
<div class="bubble bot-bubble">${text}</div>
`

chatbox.appendChild(row)

}

function addTyping(){

const row = document.createElement("div")
row.className = "message bot-row"
row.id = "typing"

row.innerHTML = `
<div class="avatar bot-avatar">🤖</div>
<div class="bubble bot-bubble">Thinking...</div>
`

chatbox.appendChild(row)

}

function removeTyping(){

const typing = document.getElementById("typing")
if(typing) typing.remove()

}

async function sendMessage(){

const message = input.value.trim()
if(!message) return

addUserMessage(message)

input.value = ""

addTyping()

chatbox.scrollTop = chatbox.scrollHeight

try{

const response = await fetch("/chat",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({query:message})

})

const data = await response.json()

removeTyping()

if(data.answer){

addBotMessage(data.answer)

}else{

addBotMessage("No response received.")

}

}catch(error){

removeTyping()

addBotMessage("Server error. Please try again.")

console.error(error)

}

chatbox.scrollTop = chatbox.scrollHeight

input.focus()

}

input.addEventListener("keypress",function(e){

if(e.key==="Enter") sendMessage()

})
