let riskChart = null;

function toggleTheme() {
    document.body.classList.toggle("dark");
    document.body.classList.toggle("light");
}

async function analyzeTax() {
    const payload = {
        annual_income: Number(document.getElementById("annualIncome").value),
        investment_80c: Number(document.getElementById("investment80c").value),
        hra: Number(document.getElementById("hra").value),
        previous_tax: Number(document.getElementById("previousTax").value),
        employment_type: document.getElementById("employmentType").value,
        extra_80c: Number(document.getElementById("extra80c").value)
    };

    const response = await fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const json = await response.json();
    const data = json.data;

    /* ---------------- RESULTS ---------------- */
    document.getElementById("results").innerHTML = `
        <p><b>Predicted Tax:</b> ₹${data.predicted_tax}</p>
        <p><b>Tax Range:</b> ₹${data.tax_range.min} – ₹${data.tax_range.max}</p>
        <p><b>Status:</b> ${data.status_message}</p>
    `;

    /* ---------------- TAX SUMMARY ---------------- */
    const totalDeductions = payload.investment_80c + payload.hra;
    const taxableIncome = payload.annual_income - totalDeductions;

    document.getElementById("summary").innerHTML = `
        <p>Annual Income: ₹${payload.annual_income}</p>
        <p>Total Deductions: ₹${totalDeductions}</p>
        <p>Taxable Income (est.): ₹${taxableIncome}</p>
    `;

    /* ---------------- WHAT IF ---------------- */
    document.getElementById("whatIf").innerHTML = `
        <p>Remaining 80C Limit: ₹${data.what_if.extra_80c}</p>
        <p>New Estimated Tax: ₹${data.what_if.new_tax}</p>
        <p>Potential Tax Saving: ₹${data.what_if.tax_saving}</p>
    `;

    /* ---------------- INSIGHTS ---------------- */
    const insightsList = document.getElementById("insights");
    insightsList.innerHTML = "";
    data.suggestions.forEach(s => {
        const li = document.createElement("li");
        li.textContent = s;
        insightsList.appendChild(li);
    });

    /* ---------------- CHART ---------------- */
    drawRiskChart(data.predicted_tax, payload.previous_tax);
}

function drawRiskChart(predicted, paid) {
    const ctx = document.getElementById("riskChart");

    if (riskChart) {
        riskChart.destroy();
    }

    riskChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Predicted Tax", "Tax Paid"],
            datasets: [{
                label: "₹ Amount",
                data: [predicted, paid]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

