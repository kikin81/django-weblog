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

    /**
    Initializes all the tags for autocomplete
    */
    var allTags = ['c++', 'java', 'php', 'coldfusion', 'javascript', 'asp', 'ruby', 'python', 'c', 'scala', 'groovy', 'haskell', 'perl', 'erlang', 'apl', 'cobol', 'go', 'lua'];
    //-------------------------------
    // Tag events
    //-------------------------------
    var eventTags = $('#mytags');
    eventTags.tagit({
        availableTags: allTags,
        onTagRemoved: function(evt, tag) {
            console.log(evt);
            alert('This tag is being removed: ' + eventTags.tagit('tagLabel', tag));
        },
        onTagClicked: function(evt, tag) {
            console.log(tag);
            alert('This tag was clicked: ' + eventTags.tagit('tagLabel', tag));
        }
    }).tagit('option', 'onTagAdded', function(evt, tag) {
        // Add this callbackafter we initialize the widget,
        // so that onTagAdded doesn't get called on page load.
        alert('This tag is being added: ' + eventTags.tagit('tagLabel', tag));
    });
});