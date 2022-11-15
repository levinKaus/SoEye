// Add event listener to table rows to make them clickable
document.addEventListener("DOMContentLoaded", () => {
    const tableRows = document.querySelectorAll("tr");

    // Remove whitespaces from header row
    const tableHeaders = tableRows[0].textContent.split("\n");
    for (i = 0; i < tableHeaders.length; i++) {
        tableHeaders[i] = tableHeaders[i].trim();
    }

    for (i = 1; i < tableRows.length; i++) {
        const row = tableRows[i].textContent.split('\n');
        let data = "{";

        // Remove whitespaces from rows
        for (j = 0; j < row.length; j++) {
            row[j] = row[j].trim();
        }

        // Join headers with data from a row
        for (j = 1; j < tableHeaders.length - 1; j++) {
            if (j == tableHeaders.length - 2){
                data = data + "\"" + tableHeaders[j] + "\": \"" +  row[j] + "\"}"
            }
            else {
                data = data + "\"" + tableHeaders[j] + "\": \"" + row[j] + "\", "; 
            }
        }
        tableRows[i].addEventListener("click", () => {
            $.ajax({
                type: "POST",
                contentType: "application/json; charset=utf-8",
                url: "/add_evidence",
                data: data,
                dataType: "json"
            });
        });
    }
});