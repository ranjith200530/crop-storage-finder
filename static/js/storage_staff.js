document.addEventListener("DOMContentLoaded", function () {

    const deleteButtons =
        document.querySelectorAll(".delete-btn");


    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const userId =
                this.dataset.userId;


            deleteStaff(userId, this);

        });

    });

});


function deleteStaff(userId, button) {

    const confirmation = confirm(
        "Are you sure you want to permanently delete this staff member?"
    );


    if (!confirmation) {

        return;

    }


    /*
     * Disable button while deletion is in progress.
     */

    button.disabled = true;

    button.innerText = "Deleting...";


    /*
     * Send POST request to Django.
     */

    fetch(`/delete-staff/${userId}/`, {

        method: "POST",

        headers: {

            "X-CSRFToken": getCookie("csrftoken"),

            "X-Requested-With": "XMLHttpRequest"

        }

    })


    .then(function (response) {

        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }

        return response.json();

    })


    .then(function (data) {

        if (data.success) {

            /*
             * Find the row containing
             * the clicked button.
             */

            const row =
                button.closest("tr");


            /*
             * Remove the row dynamically.
             */

            row.remove();


            /*
             * Check if any staff members
             * are remaining.
             */

            const remainingRows =
                document.querySelectorAll("tbody tr");


            /*
             * If no staff members remain,
             * show the empty state.
             */

            if (remainingRows.length === 0) {

                const tableSection =
                    document.querySelector(".table-section");


                tableSection.innerHTML = `

                    <section class="empty-state">

                        <div class="empty-icon">
                            👤
                        </div>

                        <h2>
                            No Staff Members
                        </h2>

                        <p>
                            No staff members are currently
                            assigned to this storage.
                        </p>

                    </section>

                `;

            }

        }


        else {

            alert(data.message);

            button.disabled = false;

            button.innerText = "Delete";

        }

    })


    .catch(function (error) {

        console.error(
            "Delete staff error:",
            error
        );


        alert(
            "Something went wrong while deleting the staff member."
        );


        button.disabled = false;

        button.innerText = "Delete";

    });

}


/*
 * Get Django CSRF token.
 */

function getCookie(name) {

    let cookieValue = null;


    if (
        document.cookie &&
        document.cookie !== ""
    ) {

        const cookies =
            document.cookie.split(";");


        for (let cookie of cookies) {

            cookie = cookie.trim();


            if (
                cookie.startsWith(
                    name + "="
                )
            ) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(
                            name.length + 1
                        )
                    );

                break;

            }

        }

    }


    return cookieValue;

}