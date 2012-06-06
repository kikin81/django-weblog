$(function() {
    /**
    Initializes tinyMCE to run on all textareas with the simple theme.
    */
    tinyMCE.init({
        mode: "textareas",
        theme: "simple"
    });

    /**
    JQuery datepicker assigned to the publication date
    */
    $("#id_pub_date").datepicker();
});