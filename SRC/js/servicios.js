const trabajos = []; // 👈 aquí simulas la BD

const emptyState = document.getElementById("emptyState");
const jobList = document.getElementById("jobList");

if (trabajos.length === 0) {
    emptyState.style.display = "block";
    jobList.style.display = "none";
} else {
    emptyState.style.display = "none";
    jobList.style.display = "block";
}