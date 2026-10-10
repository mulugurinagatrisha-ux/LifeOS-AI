const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("message");
const micBtn = document.getElementById("mic-btn");

/* ==========================
   Clean Text for Speech
========================== */

function cleanForSpeech(text) {
    return text
        .replace(/```[\s\S]*?```/g, "")
        .replace(/`/g, "")
        .replace(/#+/g, "")
        .replace(/\*\*/g, "")
        .replace(/\*/g, "")
        .replace(/__/g, "")
        .replace(/_/g, "")
        .replace(/>/g, "")
        .replace(/[-•]/g, "")
        .replace(/\[(.*?)\]\((.*?)\)/g, "$1")
        .replace(/\n+/g, ". ")
        .replace(/\s+/g, " ")
        .trim();
}

/* ==========================
   AI Voice
========================== */

function speak(text) {

    speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(
        cleanForSpeech(text)
    );

    utterance.lang = "en-US";
    utterance.rate = 1.08;
    utterance.pitch = 1;
    utterance.volume = 1;

    const voices = speechSynthesis.getVoices();

    const voice =
        voices.find(v => v.name.includes("Google US English")) ||
        voices.find(v => v.name.includes("Microsoft Aria")) ||
        voices.find(v => v.name.includes("Microsoft Jenny")) ||
        voices.find(v => v.lang === "en-US") ||
        voices.find(v => v.lang.startsWith("en"));

    if (voice) {
        utterance.voice = voice;
    }

    speechSynthesis.speak(utterance);
}

window.speechSynthesis.onvoiceschanged = () => {
    speechSynthesis.getVoices();
};

/* ==========================
   Chat UI
========================== */

function scrollBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addUserMessage(message) {

    chatBox.innerHTML += `
        <div class="user">
            <span>${message}</span>
        </div>
    `;

    scrollBottom();
}

function addBotMessage(message) {

    chatBox.innerHTML += `
        <div class="bot">
            <span>${message}</span>
        </div>
    `;

    scrollBottom();
}

/* ==========================
   Typing Effect
========================== */

async function typeMessage(message){

    const botDiv = document.createElement("div");
    botDiv.className = "bot";

    const textDiv = document.createElement("div");
    textDiv.className = "bot-text";

    const span = document.createElement("span");

    textDiv.appendChild(span);

    const copyBtn = document.createElement("button");

    copyBtn.className = "copy-btn";
    copyBtn.innerHTML = "📋 Copy";

    copyBtn.onclick = function(){
        copyMessage(copyBtn);
    };

    botDiv.appendChild(textDiv);
    botDiv.appendChild(copyBtn);

    chatBox.appendChild(botDiv);

    let text = "";

    const words = message.split(" ");

    for(let i=0;i<words.length;i++){

        text += words[i] + " ";

        span.innerHTML = text;

        scrollBottom();

        await new Promise(resolve=>setTimeout(resolve,45));

    }

    speak(message);

}

/* ==========================
   Send Message
========================== */

async function sendMessage() {

    const message = messageInput.value.trim();

    if (message === "") return;

    speechSynthesis.cancel();

    addUserMessage(message);

    messageInput.value = "";

    const loadingId = "loading-" + Date.now();

    chatBox.innerHTML += `
        <div class="bot" id="${loadingId}">
            <span>🤖 Thinking...</span>
        </div>
    `;

    scrollBottom();

    try {

        const response = await fetch("/ai/send", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                message: message,
                session_id: sessionId

            })

        });

        const data = await response.json();

        document.getElementById(loadingId).remove();

        await typeMessage(data.answer);

    }

    catch (error) {

        document.getElementById(loadingId).remove();

        addBotMessage("Sorry, AI is currently unavailable.");

    }

}

/* ==========================
   Enter Key
========================== */

messageInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();

    }

});

/* ==========================
   On Load
========================== */

window.onload = function () {

    scrollBottom();

    messageInput.focus();

    speechSynthesis.getVoices();

};

/* ==========================
   Voice Assistant
========================== */

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (SpeechRecognition && micBtn) {

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    micBtn.addEventListener("click", () => {

        recognition.start();

        micBtn.innerHTML = "🎙️ Listening...";

        micBtn.disabled = true;

    });

    recognition.onresult = function (event) {

        const text = event.results[0][0].transcript;

        messageInput.value = text;

        sendMessage();

    };

    recognition.onerror = function () {

        micBtn.innerHTML = "🎤";

        micBtn.disabled = false;

    };

    recognition.onend = function () {

        micBtn.innerHTML = "🎤";

        micBtn.disabled = false;

    };

}

else {

    console.log("Speech Recognition not supported.");

}
function copyMessage(button){

    const text = button.parentElement
        .querySelector(".bot-text")
        .innerText;

    navigator.clipboard.writeText(text);

    button.innerHTML = "✅ Copied";

    setTimeout(()=>{

        button.innerHTML="📋 Copy";

    },1500);

}