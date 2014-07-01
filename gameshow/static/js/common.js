jQuery(function ($) {
    $('.dropdown-toggle').dropdown();

    var $teamName = $('.team-name');
    var $teamNameLink = $('.set-team-name');
    var $teamNameInput = $('.team-name-input');
    $teamNameLink.on('click', function (e) {
        e.preventDefault();
        $teamNameInput.show().focus();
        $teamNameLink.hide();
        $teamName.hide();
    });
});
