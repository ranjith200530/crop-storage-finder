function calculateCharge(event, id) {

    event.preventDefault();

    // Find the place where charge should be displayed
    const chargeElement = document.getElementById(
        `charge-${id}`
    );

   
    fetch(`/staff/calculate-charge/${id}/`)

        .then(response => response.json())

        .then(data => {

            if (data.success) {

                // Display calculated charge
                chargeElement.innerText =
                    "₹" +
                    data.total_charge.toFixed(2);

            } else {

                chargeElement.innerText =
                    "Not calculated";

                alert(data.message);
            }
        })

        .catch(error => {

            console.error(error);

            chargeElement.innerText =
                "Error";

            alert(
                "Unable to calculate storage charge."
            );
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