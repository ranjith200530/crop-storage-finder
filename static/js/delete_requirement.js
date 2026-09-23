document.addEventListener("DOMContentLoaded", function () {


    const deleteLinks = document.querySelectorAll(
        ".delete-requirement"
    );


    deleteLinks.forEach(function (deleteLink) {


        deleteLink.addEventListener("click", function (event) {


            // Stop the browser from opening the delete URL
            event.preventDefault();


            // Ask for confirmation
            const confirmDelete = confirm(
                "Are you sure you want to delete this requirement?"
            );


            // If user clicks Cancel
            if (!confirmDelete) {
                return;
            }


            // Get the delete URL from the anchor
            const deleteUrl = deleteLink.href;


            // Find the requirement card
            const requirementCard =
                deleteLink.closest(".requirement-card");


            // Get CSRF token
            const csrfToken =
                document.querySelector(
                    "[name=csrfmiddlewaretoken]"
                ).value;


            // Prevent multiple clicks
            deleteLink.style.pointerEvents = "none";


            // Change button text
            deleteLink.innerText = "Deleting...";


            // Send POST request to Django
            fetch(deleteUrl, {

                method: "POST",

                headers: {

                    "X-CSRFToken": csrfToken,

                    "X-Requested-With": "XMLHttpRequest"

                }

            })


            // Check response
            .then(function (response) {

                if (!response.ok) {

                    throw new Error(
                        "Delete request failed."
                    );

                }

                return response.json();

            })


            // Handle Django response
            .then(function (data) {


                if (data.success) {


                    // Remove requirement card
                    requirementCard.remove();


                    // Check how many cards remain
                    const remainingCards =
                        document.querySelectorAll(
                            ".requirement-card"
                        );


                    // If no cards remain
                    if (remainingCards.length === 0) {


                        const requirementsContainer =
                            document.querySelector(
                                ".requirements-container"
                            );


                        requirementsContainer.outerHTML = `

                            <div class="empty-message">

                                <p>
                                    No requirements added yet.
                                </p>

                            </div>

                        `;

                    }


                } else {


                    // Django returned success = false
                    alert(data.message);


                    // Restore delete link
                    deleteLink.style.pointerEvents = "auto";

                    deleteLink.innerText =
                        "Delete Requirement";

                }

            })


            // Handle network/server errors
            .catch(function (error) {


                console.error(
                    "Error deleting requirement:",
                    error
                );


                alert(
                    "Something went wrong while deleting the requirement."
                );


                // Restore delete link
                deleteLink.style.pointerEvents = "auto";

                deleteLink.innerText =
                    "Delete Requirement";

            });


        });

    });

});