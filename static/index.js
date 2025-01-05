document.getElementById("emailForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent form submission

    const email = document.getElementById("username").value;
    const resultCont = document.getElementById("resultCont");

    // Show loading spinner
    resultCont.innerHTML = '<img src="/static/loading.svg" alt="Loading..." width="50">;'

    try {
        const response = await fetch("/validate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (response.ok) {
            if (data.valid) {
                resultCont.innerHTML = <div style="color: green;">✅ ${data.reason}</div>;
            } else {
                resultCont.innerHTML = <div style="color: red;">❌ ${data.reason}</div>;
            }
        } else {
            resultCont.innerHTML = <div style="color: red;">Error: ${data.error}</div>;
        }
    } catch (error) {
        resultCont.innerHTML = <div style="color: red;">Error: Unable to validate email. Please try again.</div>;
        console.error("Error:", error);
    }
});