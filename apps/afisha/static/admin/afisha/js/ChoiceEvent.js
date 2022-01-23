function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

jQuery(function ($) {
    $(document).ready(function () {
        $("#id_type").change(function () {
            $.ajax({
                url: "afisha/get-common-event-link/",
                type: "POST",
                data: { type: $(this).val(), },
                success: function (result) {
                    console.log(result);
                    cols = document.getElementById("id_common_event");
                    cols.options.length = 0;
                    console.log(cols);
                    cols.options.add(new Option("CommonEvent", "CommonEvent"));
                    for (var k in result) {
                        cols.options.add(new Option(k, result[k]));
                    }
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                error: function (e) {
                    console.error(JSON.stringify(e));
                },
            });
        });
    });
});
