// ================================
// BUSINESS INSIGHTS DASHBOARD
// ================================

// Revenue Chart
new Chart(
    document.getElementById("revenueChart"),
    {
        type: "line",

        data: {
            labels: revenueLabels,

            datasets: [
                {
                    label: "Revenue",

                    data: revenueValues,

                    borderWidth: 3,

                    fill: true,

                    tension: 0.4
                }
            ]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    }
);


// ================================
// PROJECT STATUS
// ================================

new Chart(
    document.getElementById("projectChart"),
    {

        type: "doughnut",

        data: {

            labels: [

                "Completed",
                "Running",
                "Pending"

            ],

            datasets: [

                {

                    data: projectData,

                    borderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    }
);


// ================================
// INVOICE STATUS
// ================================

new Chart(
    document.getElementById("invoiceChart"),
    {

        type: "pie",

        data: {

            labels: [

                "Paid",
                "Pending"

            ],

            datasets: [

                {

                    data: invoiceData,

                    borderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    }
)


// ================================
// COMPLAINT STATUS
// ================================

new Chart(
    document.getElementById("complaintChart"),
    {

        type: "bar",

        data: {

            labels: [

                "Open",
                "In Progress",
                "Resolved"

            ],

            datasets: [

                {

                    label: "Complaints",

                    data: complaintData,

                    borderWidth: 2

                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {

                    beginAtZero: true

                }

            },

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    }
);


// ================================
// KPI COUNTER
// ================================

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    const target = Number(counter.innerText);

    let count = 0;

    const increment = Math.max(1, target / 80);

    function updateCounter() {

        if (count < target) {

            count += increment;

            counter.innerText = Math.ceil(count);

            requestAnimationFrame(updateCounter);

        }

        else {

            counter.innerText = target;

        }

    }

    updateCounter();

});


// ================================
// LAST UPDATED
// ================================

const lastUpdated =
    document.getElementById("lastUpdated");

if(lastUpdated){

    lastUpdated.innerHTML =
        new Date().toLocaleString();

}


// ================================
// BUSINESS HEALTH
// ================================

const complaintElement =
    document.getElementById("complaintValue");

const health =
    document.getElementById("businessHealth");

if(complaintElement && health){

    const complaints =
        Number(complaintElement.innerText);

    if(complaints===0){

        health.innerHTML="🟢 Excellent";

    }

    else if(complaints<=5){

        health.innerHTML="🟡 Good";

    }

    else{

        health.innerHTML="🔴 Needs Attention";

    }

}


console.log("Business Insights Loaded");