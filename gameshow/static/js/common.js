jQuery(function ($) {
    $('.dropdown-toggle').dropdown();

    var $teamName = $('.team-name');
    var $teamNameLink = $('.set-team-name');
    var $teamNameInput = $('.team-name-input');
    $teamNameInput.hide();
    $teamNameInput.on('keyup', function (e) {
        var teamName = $teamNameInput.val();
        if (e.key === 'Enter' || e.keyCode === 13 && teamName) {
            $.ajax({
                url: $teamNameLink.data('api-url'),
                type: 'patch',
                data: {name: teamName},
                headers: {'X-CSRFToken': $teamNameInput.data('csrf-token')},
            }).done(function (data) {
                $teamName.text(data['name']);
                $teamNameInput.hide();
                $teamNameLink.show();
                $teamName.show();
            }).fail(function () {
                alert('uh oh');
            });
        }
    });
    $teamNameLink.on('click', function (e) {
        e.preventDefault();
        $teamNameInput.show().focus();
        $teamNameLink.hide();
        $teamName.hide();
    });
});
