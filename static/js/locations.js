document.addEventListener("DOMContentLoaded", function () {

    const state = document.getElementById("state");
    const district = document.getElementById("district");
    const subDistrict = document.getElementById("sub_district");


    state.addEventListener("change", function () {

        district.innerHTML =
            "<option value=''>Select District</option>";

        subDistrict.innerHTML =
            "<option value=''>Select Sub District</option>";


        fetch("/ajax/load-districts/?state_id=" + this.value)

            .then(response => response.json())

            .then(data => {

                data.forEach(function(item){

                    district.innerHTML +=

                        `<option value="${item.id}">
                            ${item.name}
                        </option>`;

                });

            });

    });


    district.addEventListener("change", function(){

        subDistrict.innerHTML =
            "<option value=''>Select Sub District</option>";

        fetch("/ajax/load-subdistricts/?district_id=" + this.value)

            .then(response => response.json())

            .then(data => {

                data.forEach(function(item){

                    subDistrict.innerHTML +=

                        `<option value="${item.id}">
                            ${item.name}
                        </option>`;

                });

            });

    });

});