const BACKEND = "http://127.0.0.1:5000";

// ✅ Submit address
function submitAddress() {
  const name = document.getElementById("name").value;
  const address = document.getElementById("address").value;

  fetch(BACKEND + "/submit_address", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, address})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("submitMsg").innerText = data.message;

    if (data.total_submitted === data.total_required) {
      document.getElementById("generate").style.display = "block";
    }
  });
}

// ✅ Generate pairs
function generatePairs() {
  fetch(BACKEND + "/generate", {method: "POST"})
    .then(res => res.json())
    .then(data => {
      document.getElementById("generateMsg").innerText = data.message;
      if (data.message.includes("generated")) {
        // ✅ Redirect to spin page
        setTimeout(() => {
          window.location.href = "spin.html";
        }, 1000);
      }
    });
}
