document.addEventListener("DOMContentLoaded", function () {

    const deleteLinks = document.querySelectorAll(
        ".delete-listing"
    );


    deleteLinks.forEach(function (deleteLink) {

        deleteLink.addEventListener("click", function (event) {

            event.preventDefault();


            const confirmDelete = confirm(
                "Are you sure you want to delete this crop listing?"
            );


            if (!confirmDelete) {
                return;
            }


            const deleteUrl = deleteLink.href;


            const cropCard = deleteLink.closest(".crop-card");


            const csrfToken = document.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;


            deleteLink.style.pointerEvents = "none";
            deleteLink.innerText = "Deleting...";


            fetch(deleteUrl, {

                method: "POST",

                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest"
                }

            })


            .then(function (response) {

                if (!response.ok) {
                    throw new Error("Delete request failed.");
                }

                return response.json();

            })


            .then(function (data) {

                if (data.success) {

                    cropCard.remove();


                    const remainingCards =
                        document.querySelectorAll(".crop-card");


                    if (remainingCards.length === 0) {

                        const cropGrid =
                            document.querySelector(".crop-grid");


                        cropGrid.outerHTML = `
                            <section class="empty-state">

                                <div class="empty-icon">
                                    +
                                </div>

                                <h2>
                                    No Crop Listings Yet
                                </h2>

                                <p>
                                    You haven't added any crops for sale yet.
                                </p>

                            </section>
                        `;

                    }

                } else {

                    alert(data.message);

                    deleteLink.style.pointerEvents = "auto";

                    deleteLink.innerText = "Delete Listing";

                }

            })


            .catch(function (error) {

                console.error(
                    "Error deleting crop:",
                    error
                );


                alert(
                    "Something went wrong while deleting the listing."
                );


                deleteLink.style.pointerEvents = "auto";

                deleteLink.innerText = "Delete Listing";

            });

        });

    });

});




