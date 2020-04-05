$(function() {
    var is_captain = {{ is_captain|safe }};
    if (is_captain) {
        $(".member").append(function(index) {
            var username = $(".member")[index].id;
            var button = '&nbsp;&nbsp;&nbsp;<button type="button" class="remove" id=remove_' + username + '>-</button>'
            if (index != 0) return button;
        })
    };

    $(".remove").click(function(event) {
        var buttonId = event.target.id;
        var username = buttonId.substring(7);
        var csrf_token = $('{% csrf_token %}')[0].value;
        $.post("{% url 'remove_member' %}", {'username': username, 'csrfmiddlewaretoken': csrf_token}, function() {
            $("#" + buttonId).remove();
            $("#" + username).remove();
        });
    });
});
