$(function() {
    /**
    Initializes tinyMCE to run on all textareas with the simple theme.
    */
    tinyMCE.init({
        mode: "textareas",
        theme: "advanced",
        height: "380",
        width: "400",
        body_id : "elm1=my_id,elm2=my_id2"
    });

    /**
    JQuery datepicker assigned to the publication date
    */
    $("#id_pub_date").datepicker();
});