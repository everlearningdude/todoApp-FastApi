document.addEventListener("DOMContentLoaded", function() {
    // Event delegation for "Select" button click
    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("select-button")) {
            const productName = event.target.dataset.productName;
            if (productName) {
                loadTemplateKeys(productName);
                clearTemplateInputs();
            }
        }
    });

    // Event listener for template key dropdown change
    document.getElementById("templateDropdown").addEventListener("change", function() {
        const selectedKey = this.value;
        const productName = document.getElementById("templateDropdown").dataset.productName;
        console.log(productName + " " + selectedKey);
        if (selectedKey && productName) {
            loadTemplateInputs(productName, selectedKey);
        }
    });

    // Function to load template keys into dropdown
    function loadTemplateKeys(productName) {
        fetch(`data/${productName}-templates.json`)
            .then(response => response.json())
            .then(data => {
                const templateDropdown = document.getElementById("templateDropdown");
                templateDropdown.innerHTML = ""; // Clear previous options
                templateDropdown.dataset.productName = productName;

                Object.keys(data).forEach(key => {
                    const option = document.createElement("option");
                    option.text = key;
                    option.value = key;
                    templateDropdown.appendChild(option);
                });
            })
            .catch(error => console.error("Error fetching templates for product:", error));
    }

    // Function to load template inputs for selected key
    // function loadTemplateInputs(productName, selectedKey) {
        
    //     fetch(`data/${productName}-templates.json`)
    //         .then(response => response.json())
    //         .then(data => {
    //             const templateInputs = document.getElementById("templateInputs");
    //             templateInputs.innerHTML = ""; // Clear previous inputs

    //             const keyValuePairs = data[selectedKey];
    //             Object.keys(keyValuePairs).forEach(key => {
    //                 const inputField = document.createElement("div");
    //                 inputField.classList.add("mb-3");

    //                 const label = document.createElement("label");
    //                 label.classList.add("form-label");
    //                 label.textContent = key;
    //                 inputField.appendChild(label);

    //                 const inputElement = document.createElement("input");
    //                 inputElement.classList.add("form-control");
    //                 inputElement.setAttribute("type", "text");
    //                 inputElement.setAttribute("name", key);
    //                 inputElement.value = keyValuePairs[key];
    //                 inputField.appendChild(inputElement);

    //                 templateInputs.appendChild(inputField);
    //             });
    //         })
    //         .catch(error => console.error("Error fetching templates for product:", error));
    // }


    // Function to load template inputs for selected key
function loadTemplateInputs(productName, selectedKey) {
    fetch(`data/${productName}-templates.json`)
        .then(response => response.json())
        .then(data => {
            const templateInputs = document.getElementById("templateInputs");
            templateInputs.innerHTML = ""; // Clear previous inputs

            const keyValuePairs = data[selectedKey];
            Object.keys(keyValuePairs).forEach(key => {
                const inputField = document.createElement("div");
                inputField.classList.add("mb-3");

                const label = document.createElement("label");
                label.classList.add("form-label");
                label.textContent = key;
                inputField.appendChild(label);

                const inputElement = document.createElement("input");
                inputElement.classList.add("form-control");
                inputElement.setAttribute("type", "text");
                inputElement.setAttribute("name", key);
                inputElement.setAttribute("value", keyValuePairs[key]);
                inputElement.setAttribute("required", "required"); // Add required attribute
                inputField.appendChild(inputElement);

                templateInputs.appendChild(inputField);
            });
        })
        .catch(error => console.error("Error fetching templates for product:", error));
}

// Function to load template inputs for selected key
// function loadTemplateInputs(productName, selectedKey) {
//     fetch(`data/${productName}-templates.json`)
//         .then(response => response.json())
//         .then(data => {
//             const templateInputs = document.getElementById("templateInputs");
//             templateInputs.innerHTML = ""; // Clear previous inputs

//             const keyValuePairs = data[selectedKey];
//             Object.keys(keyValuePairs).forEach(key => {
//                 const inputField = document.createElement("div");
//                 inputField.classList.add("mb-3");

//                 const label = document.createElement("label");
//                 label.classList.add("form-label");
//                 label.textContent = keyValuePairs[key].label || key; // Use label if provided, otherwise use key
//                 if (keyValuePairs[key].required) { // Check if field is required
//                     label.innerHTML += ' <span style="color: red;">*</span>'; // Add asterisk for required fields with red color
//                 }
//                 inputField.appendChild(label);

//                 const inputElement = document.createElement("input");
//                 inputElement.classList.add("form-control");
//                 inputElement.setAttribute("type", keyValuePairs[key].type || "text"); // Use type if provided, otherwise default to text
//                 inputElement.setAttribute("name", keyValuePairs[key].name || key); // Use name if provided, otherwise use key
//                 inputElement.setAttribute("value", keyValuePairs[key].value || ""); // Use default value if provided
//                 if (keyValuePairs[key].required) { // Set required attribute for required fields
//                     inputElement.setAttribute("required", "required");
//                 }
//                 inputField.appendChild(inputElement);

//                 templateInputs.appendChild(inputField);
//             });
//         })
//         .catch(error => console.error("Error fetching templates for product:", error));
// }



function clearTemplateInputs() {
    const templateInputs = document.getElementById("templateInputs");
    templateInputs.innerHTML = ""; // Clear input forms
}


// Event listener for submit button click
document.getElementById("submitBtn").addEventListener("click", function() {
    // Check for valid inputs before submission
    const inputs = document.querySelectorAll("#templateInputs input");
    let isValid = true;

    inputs.forEach(input => {
        if (!input.checkValidity()) {
            isValid = false;
            return;
        }
    });

    if (isValid) {
        // All inputs are valid, perform submission
        alert("Form submitted successfully!");
        // Here you can add code to submit the form data to your backend or perform any other action
    } else {
        alert("Please fill out all required fields correctly.");
    }
});


});
