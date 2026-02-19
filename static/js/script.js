function toggleHistory() {
    const historyDiv = document.getElementById("historyBox");

    if (!historyDiv) return;

    if (historyDiv.style.display === "none" || historyDiv.style.display === "") {
        historyDiv.style.display = "block";
    } else {
        historyDiv.style.display = "none";
    }
}
