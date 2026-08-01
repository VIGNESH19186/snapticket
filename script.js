// SnapTicket front-end helpers

document.addEventListener("DOMContentLoaded", () => {
    // Auto-hide flash messages after a few seconds
    const flash = document.querySelector(".flash");
    if (flash) {
        setTimeout(() => {
            flash.style.transition = "opacity 0.5s";
            flash.style.opacity = "0";
            setTimeout(() => flash.remove(), 500);
        }, 4000);
    }
});