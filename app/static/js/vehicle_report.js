$(document).ready(function() {
    $(".export-btn").on("click", function () {
        let button = $(this);
        let format = button.data("format");
        let buttonText = button.find(".button-text");
        let spinner = button.find(".spinner-border");

        // Loading
        buttonText.addClass("d-none");
        spinner.removeClass("d-none");

        $.ajax({
            url: `/vehicle_report?format=${format}`,
            method: "GET",
            xhrFields: {
                responseType: "blob"  // Expect a file
            },
            success: function (blob) {
                // Download File
                let url = window.URL.createObjectURL(blob);
                let a = $("<a>")
                    .attr("href", url)
                    .attr("download", `vehicle_report.${format}`)
                    .appendTo("body");
                a[0].click();
                window.URL.revokeObjectURL(url);
                a.remove();

            },
            error: function (msg) {
                msg = msg.responseJSON ? msg.responseJSON : `An error occurred during export. (.${format}) Try again!`
                addToast(msg, 'Info', 'bg-danger')
            },
            complete: function () {
                // Restore
                spinner.addClass("d-none");
                buttonText.removeClass("d-none");
            }
        });
    });
  });
