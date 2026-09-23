
    
function calculateCharge(event, id) {

    event.preventDefault();

    const daysElement = document.getElementById(
        `days-${id}`
    );

    const chargeElement = document.getElementById(
        `charge-${id}`
    );

    fetch(`/staff/calculate-charge/${id}/`)

        .then(response => {

            if (!response.ok) {
                throw new Error(
                    "Server returned an error."
                );
            }

            return response.json();
        })

        .then(data => {

            if (data.success) {

                daysElement.innerText =
                    data.days + " Days";

                chargeElement.innerText =
                    "₹" +
                    Number(data.total_charge).toFixed(2);

            } else {

                daysElement.innerText =
                    "Not calculated";

                chargeElement.innerText =
                    "Not calculated";
            }
        })

        .catch(error => {

            console.error(
                "Calculate charge error:",
                error
            );

            daysElement.innerText =
                "Not calculated";

            chargeElement.innerText =
                "Not calculated";
        });
}


function getCSRFToken() {
    return document.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).value;
}


function removeBooking(event, id) {

    event.preventDefault();

    const confirmRemove = confirm(
        "Are you sure you want to remove this booking?"
    );

    if (!confirmRemove) {
        return;
    }

    fetch(`/staff/remove-booking/${id}/`, {
        method: "POST",

        headers: {
            "X-CSRFToken": getCSRFToken()
        },

        credentials: "same-origin"
    })
    .then(response => response.json())
    .then(data => {

        if (data.success) {

            // Find only this booking card
            const bookingCard =
                document.getElementById(`booking-${id}`);

            // Remove this booking card from the page
            if (bookingCard) {
                bookingCard.remove();
            }

        } else {

            alert(data.message);
        }
    })
    .catch(error => {

        console.error(error);

        alert(
            "Something went wrong while removing the booking."
        );
    });
}