// ==========================================
// LifeOS AI Goal Coach
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
    initProgress();
    initAchievement();
    initGoalDays();
    initMotivation();
});


// ==========================================
// Progress Calculator
// ==========================================

function initProgress() {

    const current = document.getElementById("current_value");
    const target = document.getElementById("target_value");

    const circle = document.querySelector(".progress-circle span");
    const bar = document.getElementById("goalProgress");
    const text = document.getElementById("progressText");
    const status = document.querySelector(".status");

    if (!current || !target) return;

    function calculate() {

        const c = Number(current.value) || 0;
        const t = Number(target.value) || 0;

        let percentage = 0;

        if (t > 0) {
            percentage = Math.round((c / t) * 100);
        }

        percentage = Math.max(0, Math.min(100, percentage));

        // Update progress circle
        if (circle) {
            circle.textContent = percentage + "%";
        }

        // Update progress bar
        if (bar) {
            bar.style.width = percentage + "%";
        }

        // Update progress text
        if (text) {
            text.textContent = percentage + "% Completed";
        }

        // Update status
        if (status) {

            if (t > 0 && c >= t) {
                status.textContent = "🏆 Goal Completed";
                status.style.color = "#22c55e";
            } else if (c > 0 && t > 0) {
                status.textContent = "🚀 In Progress";
                status.style.color = "#3b82f6";
            } else {
                status.textContent = "Ready to Generate";
                status.style.color = "";
            }
        }

        // Update estimated days
        calculateDays(c, t);
    }

    current.addEventListener("input", calculate);
    target.addEventListener("input", calculate);

    // Important: calculate on page load too
    calculate();
}


// ==========================================
// Estimated Days
// ==========================================

function initGoalDays() {

    const current = document.getElementById("current_value");
    const target = document.getElementById("target_value");

    if (!current || !target) return;

    function updateDays() {

        const c = Number(current.value) || 0;
        const t = Number(target.value) || 0;

        calculateDays(c, t);
    }

    current.addEventListener("input", updateDays);
    target.addEventListener("input", updateDays);
}


function calculateDays(current, target) {

    const daysElement = document.getElementById("days");

    if (!daysElement) return;

    if (target <= 0) {
        daysElement.textContent = "-- Days";
        return;
    }

    if (current >= target) {
        daysElement.textContent = "Completed";
        return;
    }

    // This is only a rough preview, not the AI estimate.
    const remaining = target - current;

    daysElement.textContent =
        remaining + (remaining === 1 ? " Unit Remaining" : " Units Remaining");
}


// ==========================================
// Achievement System
// ==========================================

function initAchievement() {

    const cards = document.querySelectorAll(".badge-card");

    cards.forEach(card => {
        card.style.opacity = "0.5";
        card.style.transform = "scale(0.95)";
    });
}


// ==========================================
// Unlock Badge
// ==========================================

function unlockBadge(index) {

    const cards = document.querySelectorAll(".badge-card");

    if (index < 0 || index >= cards.length) return;

    cards[index].style.opacity = "1";
    cards[index].style.transform = "scale(1.08)";
    cards[index].style.transition = "0.4s";

    cards[index].style.boxShadow =
        "0 0 30px rgba(255, 215, 0, 0.7)";
}


// ==========================================
// Goal Completed
// ==========================================

function goalCompleted() {

    unlockBadge(2);

    showPopup(
        "🏆 Goal Completed",
        "Congratulations! You achieved your goal."
    );

    addXP(100);

    updateStreak();
}


// ==========================================
// Motivation Quotes
// ==========================================

function initMotivation() {

    const motivation = document.getElementById("motivation");

    if (!motivation) return;

    const quotes = [
        "🔥 Every day is progress.",
        "💪 Discipline beats motivation.",
        "🚀 Small steps create big success.",
        "🏆 Never stop until you're proud.",
        "🌱 Progress is better than perfection.",
        "⚡ Success is built one task at a time."
    ];

    let index = 0;

    motivation.textContent = quotes[index];

    setInterval(() => {
        index = (index + 1) % quotes.length;
        motivation.textContent = quotes[index];
    }, 6000);
}


// ==========================================
// XP System
// ==========================================

let xp = 0;
let level = 1;

function addXP(points) {

    xp += points;

    while (xp >= level * 100) {

        xp -= level * 100;
        level++;

        showPopup(
            "🎉 Level Up!",
            "Congratulations! You reached Level " + level
        );
    }
}


// ==========================================
// Streak System
// ==========================================

let streak = Number(localStorage.getItem("goal_streak")) || 0;

function updateStreak() {

    streak++;

    localStorage.setItem("goal_streak", streak);

    console.log("🔥 Current Streak:", streak);
}


// ==========================================
// Popup
// ==========================================

function showPopup(title, message) {

    const popup = document.createElement("div");

    popup.className = "goal-popup";

    const heading = document.createElement("h2");
    heading.textContent = title;

    const paragraph = document.createElement("p");
    paragraph.textContent = message;

    popup.appendChild(heading);
    popup.appendChild(paragraph);

    document.body.appendChild(popup);

    setTimeout(() => {
        popup.classList.add("show");
    }, 100);

    setTimeout(() => {

        popup.classList.remove("show");

        setTimeout(() => {
            popup.remove();
        }, 500);

    }, 3500);
}